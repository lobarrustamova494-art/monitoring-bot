"""Admin panel handlers"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import User, Channel, Subscription, ForwardedMessage
from config import settings
from bot.keyboards import Keyboards

router = Router()

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id in settings.admin_list

@router.message(Command("admin"))
async def admin_panel(message: Message, session: AsyncSession):
    """Show admin panel"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda admin huquqlari yo'q")
        return
    
    # Get statistics
    total_users = await session.execute(select(func.count(User.id)))
    total_users = total_users.scalar()
    
    active_users = await session.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    active_users = active_users.scalar()
    
    total_channels = await session.execute(select(func.count(Channel.id)))
    total_channels = total_channels.scalar()
    
    active_channels = await session.execute(
        select(func.count(Channel.id)).where(Channel.is_active == True)
    )
    active_channels = active_channels.scalar()
    
    total_subscriptions = await session.execute(select(func.count(Subscription.id)))
    total_subscriptions = total_subscriptions.scalar()
    
    total_forwarded = await session.execute(select(func.count(ForwardedMessage.id)))
    total_forwarded = total_forwarded.scalar()
    
    text = (
        "👨‍💼 Admin Panel\n\n"
        f"👥 Jami foydalanuvchilar: {total_users}\n"
        f"✅ Faol foydalanuvchilar: {active_users}\n\n"
        f"📺 Jami kanallar: {total_channels}\n"
        f"✅ Faol kanallar: {active_channels}\n\n"
        f"📌 Jami obunalar: {total_subscriptions}\n"
        f"📨 Jami yuborilgan: {total_forwarded}\n\n"
        "Buyruqlar:\n"
        "/broadcast - Xabar yuborish\n"
        "/stats - Batafsil statistika\n"
        "/users - Foydalanuvchilar ro'yxati"
    )
    
    await message.answer(text)

@router.message(Command("stats"))
async def detailed_stats(message: Message, session: AsyncSession):
    """Show detailed statistics"""
    if not is_admin(message.from_user.id):
        return
    
    # Top users by subscriptions
    top_users = await session.execute(
        select(User, func.count(Subscription.id).label('sub_count'))
        .join(Subscription)
        .group_by(User.id)
        .order_by(func.count(Subscription.id).desc())
        .limit(10)
    )
    top_users = top_users.all()
    
    # Top channels by subscribers
    top_channels = await session.execute(
        select(Channel, func.count(Subscription.id).label('sub_count'))
        .join(Subscription)
        .group_by(Channel.id)
        .order_by(func.count(Subscription.id).desc())
        .limit(10)
    )
    top_channels = top_channels.all()
    
    text = "📊 Batafsil statistika\n\n"
    
    text += "🔝 Top 10 foydalanuvchilar:\n"
    for i, (user, count) in enumerate(top_users, 1):
        text += f"{i}. {user.first_name} (@{user.username}): {count} ta kanal\n"
    
    text += "\n🔝 Top 10 kanallar:\n"
    for i, (channel, count) in enumerate(top_channels, 1):
        text += f"{i}. {channel.title}: {count} ta obunachi\n"
    
    await message.answer(text)

@router.message(Command("broadcast"))
async def broadcast_command(message: Message):
    """Broadcast message to all users"""
    if not is_admin(message.from_user.id):
        return
    
    await message.answer(
        "📢 Broadcast\n\n"
        "Barcha foydalanuvchilarga yuborish uchun xabar yuboring.\n"
        "Bekor qilish: /cancel"
    )

@router.message(Command("users"))
async def list_users(message: Message, session: AsyncSession):
    """List recent users"""
    if not is_admin(message.from_user.id):
        return
    
    users = await session.execute(
        select(User)
        .order_by(User.created_at.desc())
        .limit(20)
    )
    users = users.scalars().all()
    
    text = "👥 Oxirgi 20 foydalanuvchi:\n\n"
    for user in users:
        premium = "⭐" if user.is_premium else ""
        text += f"{premium} {user.first_name} (@{user.username}) - {user.created_at.strftime('%Y-%m-%d')}\n"
    
    await message.answer(text)
