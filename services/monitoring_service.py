import asyncio
from pyrogram import Client
from pyrogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models import Channel, Subscription, ForwardedMessage, ForwardMode, FilterType
from typing import List, Optional
from loguru import logger
import redis.asyncio as redis
from config import settings

class MonitoringService:
    def __init__(self, userbot: Client, bot_client):
        self.userbot = userbot
        self.bot = bot_client
        self.redis = None
        self.running = False
    
    async def init_redis(self):
        self.redis = await redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    async def start_monitoring(self, session: AsyncSession):
        self.running = True
        logger.info("Monitoring service started")
        
        while self.running:
            try:
                await self._check_channels(session)
                await asyncio.sleep(settings.CHECK_INTERVAL)
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                await asyncio.sleep(5)
    
    async def stop_monitoring(self):
        self.running = False
        if self.redis:
            await self.redis.close()
        logger.info("Monitoring service stopped")
    
    async def _check_channels(self, session: AsyncSession):
        result = await session.execute(
            select(Channel).where(Channel.is_active == True)
        )
        channels = result.scalars().all()
        
        tasks = []
        for channel in channels:
            tasks.append(self._process_channel(session, channel))
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _process_channel(self, session: AsyncSession, channel: Channel):
        try:
            # Check if userbot is available
            if not self.userbot:
                logger.warning(f"Userbot not available, skipping channel {channel.channel_id}")
                return
            
            # Get new messages
            messages = []
            async for message in self.userbot.get_chat_history(
                channel.channel_id,
                limit=10
            ):
                if message.id > channel.last_message_id:
                    messages.append(message)
            
            if not messages:
                return
            
            messages.reverse()
            
            # Get subscriptions
            result = await session.execute(
                select(Subscription)
                .where(
                    and_(
                        Subscription.channel_id == channel.id,
                        Subscription.is_active == True
                    )
                )
            )
            subscriptions = result.scalars().all()
            
            for message in messages:
                for subscription in subscriptions:
                    await self._forward_message(session, subscription, message)
                
                channel.last_message_id = max(channel.last_message_id, message.id)
            
            await session.commit()
            
        except Exception as e:
            logger.error(f"Error processing channel {channel.channel_id}: {e}")
    
    async def _forward_message(
        self,
        session: AsyncSession,
        subscription: Subscription,
        message: Message
    ):
        try:
            # Check if already forwarded
            cache_key = f"fwd:{subscription.id}:{message.id}"
            if await self.redis.exists(cache_key):
                return
            
            # Apply filters
            if not self._apply_filters(subscription, message):
                return
            
            # Prepare message text
            text = message.text or message.caption or ""
            if subscription.add_prefix:
                text = f"{subscription.add_prefix}\n\n{text}"
            
            # Forward based on mode
            destinations = []
            if subscription.forward_mode in [ForwardMode.PRIVATE, ForwardMode.BOTH]:
                destinations.append(subscription.user.telegram_id)
            
            if subscription.forward_mode in [ForwardMode.GROUP, ForwardMode.BOTH]:
                if subscription.group:
                    destinations.append(subscription.group.group_id)
            
            for dest_id in destinations:
                try:
                    if message.media:
                        await self._forward_media_message(message, dest_id, text)
                    else:
                        await self.bot.send_message(dest_id, text)
                    
                    # Log forwarded message
                    fwd_msg = ForwardedMessage(
                        subscription_id=subscription.id,
                        channel_message_id=message.id,
                        destination_chat_id=dest_id
                    )
                    session.add(fwd_msg)
                    
                    subscription.posts_forwarded += 1
                    
                except Exception as e:
                    logger.error(f"Error forwarding to {dest_id}: {e}")
            
            await session.commit()
            await self.redis.setex(cache_key, 86400, "1")
            
        except Exception as e:
            logger.error(f"Forward error: {e}")
    
    def _apply_filters(self, subscription: Subscription, message: Message) -> bool:
        # Filter by type
        if subscription.filter_type == FilterType.TEXT_ONLY and message.media:
            return False
        if subscription.filter_type == FilterType.MEDIA_ONLY and not message.media:
            return False
        
        # Keyword filter
        if subscription.keyword_filter:
            text = (message.text or message.caption or "").lower()
            keywords = subscription.keyword_filter.lower().split(",")
            if not any(kw.strip() in text for kw in keywords):
                return False
        
        return True
    
    async def _forward_media_message(self, message: Message, dest_id: int, caption: str):
        if message.photo:
            await self.bot.send_photo(dest_id, message.photo.file_id, caption=caption)
        elif message.video:
            await self.bot.send_video(dest_id, message.video.file_id, caption=caption)
        elif message.document:
            await self.bot.send_document(dest_id, message.document.file_id, caption=caption)
        elif message.audio:
            await self.bot.send_audio(dest_id, message.audio.file_id, caption=caption)
        elif message.voice:
            await self.bot.send_voice(dest_id, message.voice.file_id, caption=caption)
