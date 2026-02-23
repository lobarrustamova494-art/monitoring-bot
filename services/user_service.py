from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import User
from typing import Optional

class UserService:
    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None
    ) -> User:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        
        return user
    
    @staticmethod
    async def get_user_by_telegram_id(
        session: AsyncSession,
        telegram_id: int
    ) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def update_premium_status(
        session: AsyncSession,
        telegram_id: int,
        is_premium: bool
    ) -> bool:
        user = await UserService.get_user_by_telegram_id(session, telegram_id)
        if user:
            user.is_premium = is_premium
            await session.commit()
            return True
        return False
