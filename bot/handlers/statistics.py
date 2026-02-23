from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from database.models import User, Subscription, ForwardedMessage
from bot.keyboards import Keyboards

router = Router()

@router.callback_query(F.data == "statistics")
async def show_statistics(callback: CallbackQuery, session: AsyncSession):
    user = await session.execute(
        select(User).where(User.telegram_id == callback.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        await callback.answer("Xatolik", show_alert=True)
        return
    
    # Get subscriptions count
    subs_count = await session.execute(
        select(func.count(Subscription.id))
        .where(Subscription.user_id == user.id, Subscription.is_active == True)
    )
    subs_count = subs_count.scalar()
    
    # Get total forwarded messages
    total_forwarded = await session.execute(
        select(func.sum(Subscription.posts_forwarded))
        .where(Subscription.user_id == user.id)
    )
    total_forwarded = total_forwarded.scalar() or 0
    
    # Get top channels with eager loading
    top_channels = await session.execute(
        select(Subscription)
        .options(joinedload(Subscription.channel))
        .where(Subscription.user_id == user.id)
        .order_by(Subscription.posts_forwarded.desc())
        .limit(5)
    )
    top_channels = top_channels.scalars().all()
    
    premium_status = "Ha" if user.is_premium else "Yo'q"
    
    text = (
        f"📊 Statistika\n\n"
        f"👤 Foydalanuvchi: {callback.from_user.first_name}\n"
        f"📌 Kanallar: {subs_count}\n"
        f"📨 Jami yuborilgan: {total_forwarded} ta post\n"
        f"⭐ Premium: {premium_status}\n\n"
    )
    
    if top_channels:
        text += "🔝 Top kanallar:\n"
        for i, sub in enumerate(top_channels, 1):
            channel_name = sub.channel.title or sub.channel.username
            text += f"{i}. {channel_name}: {sub.posts_forwarded} ta\n"
    
    await callback.message.edit_text(text, reply_markup=Keyboards.main_menu())
    await callback.answer()
