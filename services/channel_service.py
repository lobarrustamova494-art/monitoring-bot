from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models import Channel, Subscription, User, UserGroup, ForwardMode
from typing import Optional, List
from config import settings

class ChannelService:
    @staticmethod
    async def add_channel(
        session: AsyncSession,
        channel_id: int,
        username: Optional[str],
        title: str
    ) -> Channel:
        result = await session.execute(
            select(Channel).where(Channel.channel_id == channel_id)
        )
        channel = result.scalar_one_or_none()
        
        if not channel:
            channel = Channel(
                channel_id=channel_id,
                username=username,
                title=title
            )
            session.add(channel)
            await session.commit()
            await session.refresh(channel)
        
        return channel
    
    @staticmethod
    async def subscribe_user(
        session: AsyncSession,
        user_id: int,
        channel_id: int,
        forward_mode: ForwardMode = ForwardMode.PRIVATE,
        group_id: Optional[int] = None
    ) -> Optional[Subscription]:
        # Check user limits
        user = await session.get(User, user_id)
        if not user:
            return None
        
        result = await session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.is_active == True
                )
            )
        )
        active_subs = result.scalars().all()
        
        max_channels = settings.MAX_CHANNELS_PREMIUM if user.is_premium else settings.MAX_CHANNELS_PER_USER
        if len(active_subs) >= max_channels:
            return None
        
        # Check if already subscribed
        result = await session.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.channel_id == channel_id
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.is_active = True
            existing.forward_mode = forward_mode
            existing.group_id = group_id
        else:
            existing = Subscription(
                user_id=user_id,
                channel_id=channel_id,
                forward_mode=forward_mode,
                group_id=group_id
            )
            session.add(existing)
        
        await session.commit()
        await session.refresh(existing)
        return existing
    
    @staticmethod
    async def get_user_subscriptions(
        session: AsyncSession,
        user_id: int
    ) -> List[Subscription]:
        from sqlalchemy.orm import joinedload
        
        result = await session.execute(
            select(Subscription)
            .options(
                joinedload(Subscription.channel),
                joinedload(Subscription.user),
                joinedload(Subscription.group)
            )
            .where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.is_active == True
                )
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def unsubscribe(
        session: AsyncSession,
        subscription_id: int
    ) -> bool:
        subscription = await session.get(Subscription, subscription_id)
        if subscription:
            subscription.is_active = False
            await session.commit()
            return True
        return False
