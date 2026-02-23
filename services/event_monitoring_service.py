"""Event-based monitoring service using Pyrogram"""
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models import Channel, Subscription, ForwardedMessage, ForwardMode, FilterType
from typing import List, Optional, Set
from loguru import logger
import redis.asyncio as redis
from config import settings


class EventMonitoringService:
    """Event-based real-time monitoring using Pyrogram handlers"""
    
    def __init__(self, userbot: Client, bot_client):
        self.userbot = userbot
        self.bot = bot_client
        self.redis = None
        self.monitored_channels: Set[int] = set()
        self.running = False
        self._handler_registered = False
    
    async def init_redis(self):
        """Initialize Redis connection"""
        try:
            if not settings.REDIS_URL:
                logger.warning("REDIS_URL not set, caching disabled")
                self.redis = None
                return
            
            self.redis = await redis.from_url(settings.REDIS_URL, decode_responses=True)
            logger.info("Redis initialized for event monitoring")
        except Exception as e:
            logger.warning(f"Redis initialization failed: {e}. Continuing without cache.")
            self.redis = None
    
    def register_handlers(self):
        """Register message handlers - must be called before start_monitoring"""
        if not self.userbot or self._handler_registered:
            if self._handler_registered:
                logger.warning("Handlers already registered")
            else:
                logger.warning("Userbot not available, cannot register handlers")
            return
        
        # Create handler function
        async def handle_channel_message(client: Client, message: Message):
            """Handle new messages from channels"""
            logger.debug(f"🔔 Received message from channel {message.chat.id} (msg_id: {message.id})")
            if message.chat.id in self.monitored_channels:
                logger.debug(f"✅ Channel {message.chat.id} is monitored, processing...")
                await self._process_new_message(message)
            else:
                logger.debug(f"⏭️ Channel {message.chat.id} not in monitored list: {self.monitored_channels}")
        
        # Register handler
        self.userbot.add_handler(MessageHandler(handle_channel_message, filters.channel))
        self._handler_registered = True
        logger.info(f"✅ Message handlers registered for userbot")
    
    async def start_monitoring(self, session=None):
        """Start event-based monitoring"""
        if not self.userbot:
            logger.warning("Userbot not available, event monitoring disabled")
            return
        
        self.running = True
        logger.info("Event-based monitoring started")
        
        # Get all active channels (without transaction)
        await self._update_monitored_channels()
        
        # Periodically update monitored channels list
        while self.running:
            try:
                await self._update_monitored_channels()
                await asyncio.sleep(60)  # Update every minute
            except Exception as e:
                logger.error(f"Error updating monitored channels: {e}")
                await asyncio.sleep(5)
    
    async def _update_monitored_channels(self):
        """Update the list of channels to monitor"""
        try:
            from database import db_manager
            
            # Create new session for each update
            async with db_manager.async_session() as session:
                # Get all active channels that have at least one active subscription
                result = await session.execute(
                    select(Channel.channel_id)
                    .join(Subscription)
                    .where(
                        and_(
                            Channel.is_active == True,
                            Subscription.is_active == True
                        )
                    )
                    .distinct()
                )
                channel_ids = {row[0] for row in result.all()}
                
                # Update monitored channels
                added = channel_ids - self.monitored_channels
                removed = self.monitored_channels - channel_ids
                
                if added:
                    logger.info(f"Added {len(added)} channels to monitoring")
                if removed:
                    logger.info(f"Removed {len(removed)} channels from monitoring")
                
                self.monitored_channels = channel_ids
            
        except Exception as e:
            logger.error(f"Error updating monitored channels: {e}")
    
    async def _process_new_message(self, message: Message):
        """Process new message from channel"""
        try:
            from database import db_manager
            from sqlalchemy.orm import joinedload
            
            logger.debug(f"Processing message from channel {message.chat.id}, message_id: {message.id}")
            
            async with db_manager.async_session() as session:
                # Get channel from database
                result = await session.execute(
                    select(Channel).where(Channel.channel_id == message.chat.id)
                )
                channel = result.scalar_one_or_none()
                
                if not channel:
                    logger.warning(f"Channel {message.chat.id} not found in database")
                    return
                
                logger.debug(f"Channel found: {channel.title}, last_message_id: {channel.last_message_id}")
                
                # Check if message is newer than last processed
                if message.id <= channel.last_message_id:
                    logger.debug(f"Message {message.id} already processed (last: {channel.last_message_id})")
                    return
                
                logger.info(f"New message in channel {channel.title}: {message.id}")
                
                # Get all active subscriptions for this channel with eager loading
                result = await session.execute(
                    select(Subscription)
                    .options(
                        joinedload(Subscription.user),
                        joinedload(Subscription.channel),
                        joinedload(Subscription.group)
                    )
                    .where(
                        and_(
                            Subscription.channel_id == channel.id,
                            Subscription.is_active == True
                        )
                    )
                )
                subscriptions = result.scalars().all()
                
                # Forward to all subscribers
                for subscription in subscriptions:
                    await self._forward_message(session, subscription, message)
                
                # Update last_message_id
                channel.last_message_id = message.id
                await session.commit()
                
        except Exception as e:
            logger.error(f"Error processing new message: {e}")
    
    async def _forward_message(
        self,
        session: AsyncSession,
        subscription: Subscription,
        message: Message
    ):
        """Forward message to subscriber"""
        try:
            logger.debug(f"Attempting to forward message {message.id} for subscription {subscription.id}")
            
            # Check Redis cache for deduplication
            if self.redis:
                cache_key = f"fwd:{subscription.id}:{message.id}"
                if await self.redis.exists(cache_key):
                    logger.debug(f"Message {message.id} already forwarded (Redis cache)")
                    return
            
            # Apply filters
            filter_result = self._apply_filters(subscription, message)
            logger.debug(f"Filter result for subscription {subscription.id}: {filter_result}")
            if not filter_result:
                logger.info(f"Message {message.id} filtered out for subscription {subscription.id}")
                return
            
            # Prepare message text
            text = message.text or message.caption or ""
            if subscription.add_prefix:
                text = f"{subscription.add_prefix}\n\n{text}"
            
            # Determine destinations
            destinations = []
            if subscription.forward_mode in [ForwardMode.PRIVATE, ForwardMode.BOTH]:
                destinations.append(subscription.user.telegram_id)
            
            if subscription.forward_mode in [ForwardMode.GROUP, ForwardMode.BOTH]:
                if subscription.group:
                    destinations.append(subscription.group.group_id)
            
            # Forward to each destination
            for dest_id in destinations:
                try:
                    # Use userbot to forward message (preserves formatting and media)
                    await self.userbot.forward_messages(
                        chat_id=dest_id,
                        from_chat_id=message.chat.id,
                        message_ids=message.id
                    )
                    
                    # Log forwarded message
                    fwd_msg = ForwardedMessage(
                        subscription_id=subscription.id,
                        channel_message_id=message.id,
                        destination_chat_id=dest_id
                    )
                    session.add(fwd_msg)
                    
                    subscription.posts_forwarded += 1
                    
                    logger.info(f"Forwarded message {message.id} to {dest_id}")
                    
                except Exception as e:
                    logger.error(f"Error forwarding to {dest_id}: {e}")
                    # Fallback: try sending text only
                    try:
                        if text:
                            await self.bot.send_message(dest_id, text)
                            logger.info(f"Sent text fallback to {dest_id}")
                    except Exception as e2:
                        logger.error(f"Error sending text fallback: {e2}")
            
            await session.commit()
            
            # Cache in Redis
            if self.redis:
                cache_key = f"fwd:{subscription.id}:{message.id}"
                await self.redis.setex(cache_key, 86400, "1")
            
        except Exception as e:
            logger.error(f"Forward error: {e}")
    
    def _apply_filters(self, subscription: Subscription, message: Message) -> bool:
        """Apply filters to message"""
        logger.debug(f"Applying filters - Type: {subscription.filter_type}, Has media: {bool(message.media)}, Keywords: {subscription.keyword_filter}")
        
        # Filter by type
        if subscription.filter_type == FilterType.TEXT_ONLY and message.media:
            logger.debug("Filtered: TEXT_ONLY but message has media")
            return False
        if subscription.filter_type == FilterType.MEDIA_ONLY and not message.media:
            logger.debug("Filtered: MEDIA_ONLY but message has no media")
            return False
        
        # Keyword filter
        if subscription.keyword_filter:
            text = (message.text or message.caption or "").lower()
            keywords = subscription.keyword_filter.lower().split(",")
            if not any(kw.strip() in text for kw in keywords):
                logger.debug(f"Filtered: Keywords not found. Text: '{text[:50]}...', Keywords: {keywords}")
                return False
        
        logger.debug("Filter passed")
        return True
    
    async def _forward_media_message(self, message: Message, dest_id: int, caption: str):
        """Forward media message using userbot"""
        try:
            # Use userbot to forward message (preserves all media types)
            await self.userbot.forward_messages(
                chat_id=dest_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
        except Exception as e:
            logger.error(f"Error forwarding media with userbot: {e}")
            # Fallback: try sending text only via bot
            try:
                if caption:
                    await self.bot.send_message(dest_id, caption)
            except Exception as e2:
                logger.error(f"Error sending text fallback: {e2}")
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.running = False
        if self.redis:
            await self.redis.close()
        logger.info("Event monitoring stopped")
