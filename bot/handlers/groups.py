from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import ChatMemberUpdatedFilter, MEMBER, ADMINISTRATOR
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models import User, UserGroup
from services import UserService
from bot.keyboards import Keyboards

router = Router()

@router.callback_query(F.data == "my_groups")
async def show_my_groups(callback: CallbackQuery, session: AsyncSession):
    user = await UserService.get_user_by_telegram_id(session, callback.from_user.id)
    
    if not user:
        await callback.answer("Xatolik", show_alert=True)
        return
    
    result = await session.execute(
        select(UserGroup)
        .where(and_(UserGroup.user_id == user.id, UserGroup.is_active == True))
    )
    groups = result.scalars().all()
    
    if not groups:
        text = (
            "👥 Guruhlar\n\n"
            "Sizda hali guruhlar yo'q.\n\n"
            "Guruh qo'shish uchun:\n"
            "1. Botni guruhga qo'shing\n"
            "2. Botni admin qiling\n"
            "3. Guruh avtomatik saqlanadi"
        )
    else:
        text = f"👥 Sizning guruhlaringiz ({len(groups)}):\n\n"
        for group in groups:
            text += f"• {group.group_title}\n"
    
    await callback.message.edit_text(text, reply_markup=Keyboards.main_menu())
    await callback.answer()

@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR))
async def bot_added_as_admin(event: Message, session: AsyncSession):
    """Bot guruhga admin qilib qo'shilganda"""
    chat = event.chat
    user_id = event.from_user.id
    
    user = await UserService.get_user_by_telegram_id(session, user_id)
    if not user:
        user = await UserService.get_or_create_user(
            session,
            user_id,
            event.from_user.username,
            event.from_user.first_name
        )
    
    # Check if group already exists
    result = await session.execute(
        select(UserGroup).where(
            and_(
                UserGroup.user_id == user.id,
                UserGroup.group_id == chat.id
            )
        )
    )
    existing_group = result.scalar_one_or_none()
    
    if existing_group:
        existing_group.is_active = True
        existing_group.group_title = chat.title
    else:
        new_group = UserGroup(
            user_id=user.id,
            group_id=chat.id,
            group_title=chat.title
        )
        session.add(new_group)
    
    await session.commit()
    
    await event.answer(
        f"✅ Guruh saqlandi: {chat.title}\n\n"
        "Endi kanal sozlamalarida bu guruhni tanlashingiz mumkin."
    )
