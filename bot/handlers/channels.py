from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models import Subscription, ForwardMode, FilterType, UserGroup
from services import UserService, ChannelService
from bot.keyboards import Keyboards
from pyrogram import Client
from pyrogram.errors import UsernameNotOccupied, ChannelPrivate
from utils import parse_channel_username
from loguru import logger

router = Router()

class ChannelStates(StatesGroup):
    waiting_channel = State()
    waiting_keywords = State()
    waiting_prefix = State()

@router.callback_query(F.data == "my_channels")
async def show_my_channels(callback: CallbackQuery, session: AsyncSession):
    user = await UserService.get_user_by_telegram_id(session, callback.from_user.id)
    if not user:
        await callback.answer("Xatolik yuz berdi", show_alert=True)
        return
    
    subscriptions = await ChannelService.get_user_subscriptions(session, user.id)
    
    if not subscriptions:
        text = "❌ Sizda hali kanallar yo'q.\n\n➕ Kanal qo'shish uchun tugmani bosing."
    else:
        text = f"📌 Sizning kanallaringiz ({len(subscriptions)}):\n\nTanlang:"
    
    await callback.message.edit_text(
        text,
        reply_markup=Keyboards.channel_list(subscriptions)
    )
    await callback.answer()

@router.callback_query(F.data == "add_channel")
async def add_channel_start(callback: CallbackQuery, state: FSMContext):
    text = (
        "➕ Kanal qo'shish\n\n"
        "Kanal username yoki linkini yuboring:\n\n"
        "Masalan:\n"
        "• @channelname\n"
        "• https://t.me/channelname\n\n"
        "⚠️ Bot kanalga admin bo'lishi kerak!"
    )
    await callback.message.edit_text(text, reply_markup=Keyboards.cancel_button())
    await state.set_state(ChannelStates.waiting_channel)
    await callback.answer()

@router.message(ChannelStates.waiting_channel)
async def process_channel_input(message: Message, state: FSMContext, session: AsyncSession, userbot: Client):
    from aiogram import Bot
    from aiogram.exceptions import TelegramBadRequest
    from pyrogram.enums import ChatType
    
    channel_input = message.text.strip()
    
    # Parse channel username
    channel_username = parse_channel_username(channel_input)
    
    if not channel_username:
        await message.answer(
            "❌ Noto'g'ri format. Qaytadan urinib ko'ring.\n\n"
            "Masalan: @channelname yoki https://t.me/channelname",
            reply_markup=Keyboards.cancel_button()
        )
        return
    
    await message.answer("🔍 Kanal tekshirilmoqda...")
    
    try:
        # Get bot instance from message
        bot = message.bot
        
        # Try with userbot first (if available)
        if userbot is not None:
            try:
                chat = await userbot.get_chat(channel_username)
                chat_id = chat.id
                chat_title = chat.title
                chat_username = chat.username
                chat_type = chat.type
            except Exception as e:
                # Fallback to Bot API
                try:
                    chat = await bot.get_chat(f"@{channel_username}")
                    chat_id = chat.id
                    chat_title = chat.title
                    chat_username = chat.username
                    chat_type = chat.type
                except TelegramBadRequest:
                    await message.answer(
                        "❌ Kanal topilmadi yoki private kanal.\n\n"
                        "Public kanallarni qo'shish mumkin.",
                        reply_markup=Keyboards.main_menu()
                    )
                    await state.clear()
                    return
        else:
            # Use Bot API only
            try:
                chat = await bot.get_chat(f"@{channel_username}")
                chat_id = chat.id
                chat_title = chat.title
                chat_username = chat.username
                chat_type = chat.type
            except TelegramBadRequest:
                await message.answer(
                    "❌ Kanal topilmadi yoki private kanal.\n\n"
                    "Public kanallarni qo'shish mumkin.",
                    reply_markup=Keyboards.main_menu()
                )
                await state.clear()
                return
        
        # Check if it's a channel or supergroup
        # Pyrogram uses ChatType enum
        if hasattr(chat_type, 'value'):
            # Pyrogram ChatType enum
            is_channel = chat_type in [ChatType.CHANNEL, ChatType.SUPERGROUP]
        else:
            # Aiogram string type
            is_channel = str(chat_type).lower() in ["channel", "supergroup"]
        
        if not is_channel:
            await message.answer(
                "❌ Bu kanal emas. Faqat kanallarni qo'shish mumkin.",
                reply_markup=Keyboards.main_menu()
            )
            await state.clear()
            return
        
        # Add channel to database
        channel = await ChannelService.add_channel(
            session,
            chat_id,
            chat_username,
            chat_title
        )
        
        # Get user
        user = await UserService.get_user_by_telegram_id(session, message.from_user.id)
        
        # Subscribe user
        subscription = await ChannelService.subscribe_user(
            session,
            user.id,
            channel.id
        )
        
        if not subscription:
            await message.answer(
                "❌ Kanal qo'shib bo'lmadi. Limitga yetgansiz.",
                reply_markup=Keyboards.main_menu()
            )
        else:
            # Try to get and send the last post from channel
            last_post_sent = False
            if userbot is not None:
                try:
                    # Get the last message from channel
                    async for msg in userbot.get_chat_history(chat_id, limit=1):
                        # Forward the last post to user using userbot
                        try:
                            # Use userbot to forward (this preserves media)
                            await userbot.forward_messages(
                                chat_id=message.from_user.id,
                                from_chat_id=chat_id,
                                message_ids=msg.id
                            )
                            
                            # Update last_message_id
                            channel.last_message_id = msg.id
                            await session.commit()
                            last_post_sent = True
                        except Exception as e:
                            logger.error(f"Error forwarding last post: {e}")
                            # Fallback: try sending text only
                            try:
                                text = msg.text or msg.caption
                                if text:
                                    await bot.send_message(message.from_user.id, text)
                                    channel.last_message_id = msg.id
                                    await session.commit()
                                    last_post_sent = True
                            except Exception as e2:
                                logger.error(f"Error sending text: {e2}")
                        break
                except Exception as e:
                    logger.error(f"Error getting last post: {e}")
            
            success_msg = f"✅ Kanal qo'shildi: {chat_title}\n\n"
            if last_post_sent:
                success_msg += "📨 Oxirgi post yuborildi.\n"
            success_msg += "📝 Eslatma: Public kanallar qo'shildi.\n"
            if userbot is None:
                success_msg += "⚠️ Monitoring ishlashi uchun haqiqiy API credentials kerak.\n\n"
            else:
                success_msg += "✅ Monitoring faol. Yangi postlar avtomatik yuboriladi.\n\n"
            success_msg += "Sozlamalarni o'zgartirish uchun 'Mening kanallarim' bo'limiga o'ting."
            
            await message.answer(success_msg, reply_markup=Keyboards.main_menu())
        
    except Exception as e:
        await message.answer(
            f"❌ Xatolik: {str(e)}",
            reply_markup=Keyboards.main_menu()
        )
    
    await state.clear()

@router.callback_query(F.data.startswith("channel:"))
async def show_channel_settings(callback: CallbackQuery, session: AsyncSession):
    from sqlalchemy.orm import joinedload
    
    subscription_id = int(callback.data.split(":")[1])
    
    result = await session.execute(
        select(Subscription)
        .options(
            joinedload(Subscription.channel),
            joinedload(Subscription.user),
            joinedload(Subscription.group)
        )
        .where(Subscription.id == subscription_id)
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        await callback.answer("Kanal topilmadi", show_alert=True)
        return
    
    mode_text = {
        ForwardMode.PRIVATE: "📩 Shaxsiy chat",
        ForwardMode.GROUP: "👥 Guruh",
        ForwardMode.BOTH: "🔁 Ikkalasi"
    }
    
    mode_display = mode_text.get(subscription.forward_mode, "Noma'lum")
    status_display = "Faol" if subscription.is_active else "Nofaol"
    
    text = (
        f"⚙️ Kanal sozlamalari\n\n"
        f"📌 Kanal: {subscription.channel.title}\n"
        f"📍 Yuborish: {mode_display}\n"
        f"📊 Yuborilgan: {subscription.posts_forwarded} ta post\n"
        f"✅ Holat: {status_display}"
    )
    
    await callback.message.edit_text(
        text,
        reply_markup=Keyboards.channel_settings(subscription_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_mode:"))
async def set_forward_mode(callback: CallbackQuery):
    subscription_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "📍 Postlar qayerga yuborilsin?",
        reply_markup=Keyboards.forward_mode_selector(subscription_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("mode:"))
async def update_forward_mode(callback: CallbackQuery, session: AsyncSession):
    parts = callback.data.split(":")
    subscription_id = int(parts[1])
    mode = parts[2]
    
    subscription = await session.get(Subscription, subscription_id)
    if subscription:
        subscription.forward_mode = ForwardMode(mode)
        await session.commit()
        await callback.answer("✅ Saqlandi", show_alert=True)
        await show_channel_settings(callback, session)
    else:
        await callback.answer("❌ Xatolik", show_alert=True)

@router.callback_query(F.data.startswith("filters:"))
async def show_filters(callback: CallbackQuery):
    subscription_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "🔍 Filtrlar",
        reply_markup=Keyboards.filter_type_selector(subscription_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("filter:"))
async def update_filter(callback: CallbackQuery, session: AsyncSession):
    parts = callback.data.split(":")
    subscription_id = int(parts[1])
    filter_type = parts[2]
    
    subscription = await session.get(Subscription, subscription_id)
    if subscription:
        if filter_type == "all":
            subscription.filter_type = FilterType.ALL
        elif filter_type == "text":
            subscription.filter_type = FilterType.TEXT_ONLY
        elif filter_type == "media":
            subscription.filter_type = FilterType.MEDIA_ONLY
        
        await session.commit()
        await callback.answer("✅ Saqlandi", show_alert=True)
        await show_channel_settings(callback, session)

@router.callback_query(F.data.startswith("keywords:"))
async def set_keywords(callback: CallbackQuery, state: FSMContext):
    subscription_id = int(callback.data.split(":")[1])
    await state.update_data(subscription_id=subscription_id)
    await callback.message.edit_text(
        "🔑 Kalit so'zlarni kiriting\n\n"
        "Bir nechta so'z bo'lsa, vergul bilan ajrating.\n"
        "Masalan: sport, futbol, yangilik\n\n"
        "Agar filtrni o'chirmoqchi bo'lsangiz, 'yo'q' deb yozing.",
        reply_markup=Keyboards.cancel_button()
    )
    await state.set_state(ChannelStates.waiting_keywords)
    await callback.answer()

@router.message(ChannelStates.waiting_keywords)
async def process_keywords(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    subscription_id = data.get("subscription_id")
    
    subscription = await session.get(Subscription, subscription_id)
    if not subscription:
        await message.answer("❌ Xatolik", reply_markup=Keyboards.main_menu())
        await state.clear()
        return
    
    keywords = message.text.strip()
    if keywords.lower() in ["yo'q", "yoq", "no", "bekor"]:
        subscription.keyword_filter = None
        await message.answer("✅ Filtr o'chirildi", reply_markup=Keyboards.main_menu())
    else:
        subscription.keyword_filter = keywords
        await message.answer(
            f"✅ Kalit so'zlar saqlandi:\n{keywords}",
            reply_markup=Keyboards.main_menu()
        )
    
    await session.commit()
    await state.clear()

@router.callback_query(F.data.startswith("prefix:"))
async def set_prefix(callback: CallbackQuery, state: FSMContext):
    subscription_id = int(callback.data.split(":")[1])
    await state.update_data(subscription_id=subscription_id)
    await callback.message.edit_text(
        "✏️ Prefix matnini kiriting\n\n"
        "Bu matn har bir postning boshiga qo'shiladi.\n"
        "Masalan: 📰 Yangi post:\n\n"
        "Agar prefixni o'chirmoqchi bo'lsangiz, 'yo'q' deb yozing.",
        reply_markup=Keyboards.cancel_button()
    )
    await state.set_state(ChannelStates.waiting_prefix)
    await callback.answer()

@router.message(ChannelStates.waiting_prefix)
async def process_prefix(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    subscription_id = data.get("subscription_id")
    
    subscription = await session.get(Subscription, subscription_id)
    if not subscription:
        await message.answer("❌ Xatolik", reply_markup=Keyboards.main_menu())
        await state.clear()
        return
    
    prefix = message.text.strip()
    if prefix.lower() in ["yo'q", "yoq", "no", "bekor"]:
        subscription.add_prefix = None
        await message.answer("✅ Prefix o'chirildi", reply_markup=Keyboards.main_menu())
    else:
        subscription.add_prefix = prefix
        await message.answer(
            f"✅ Prefix saqlandi:\n{prefix}",
            reply_markup=Keyboards.main_menu()
        )
    
    await session.commit()
    await state.clear()

@router.callback_query(F.data.startswith("select_group:"))
async def select_group(callback: CallbackQuery, session: AsyncSession):
    subscription_id = int(callback.data.split(":")[1])
    subscription = await session.get(Subscription, subscription_id)
    
    if not subscription:
        await callback.answer("❌ Xatolik", show_alert=True)
        return
    
    # Get user's groups
    result = await session.execute(
        select(UserGroup).where(
            UserGroup.user_id == subscription.user_id,
            UserGroup.is_active == True
        )
    )
    groups = result.scalars().all()
    
    if not groups:
        await callback.message.edit_text(
            "❌ Sizda guruhlar yo'q.\n\n"
            "Avval botni guruhga qo'shing va admin qiling.",
            reply_markup=Keyboards.channel_settings(subscription_id)
        )
    else:
        await callback.message.edit_text(
            "👥 Guruhni tanlang:",
            reply_markup=Keyboards.group_selector(subscription_id, groups)
        )
    await callback.answer()

@router.callback_query(F.data.startswith("assign_group:"))
async def assign_group(callback: CallbackQuery, session: AsyncSession):
    parts = callback.data.split(":")
    subscription_id = int(parts[1])
    group_id = int(parts[2])
    
    subscription = await session.get(Subscription, subscription_id)
    if subscription:
        subscription.group_id = group_id
        await session.commit()
        await callback.answer("✅ Guruh tanlandi", show_alert=True)
        await show_channel_settings(callback, session)
    else:
        await callback.answer("❌ Xatolik", show_alert=True)

@router.callback_query(F.data.startswith("remove_group:"))
async def remove_group(callback: CallbackQuery, session: AsyncSession):
    subscription_id = int(callback.data.split(":")[1])
    subscription = await session.get(Subscription, subscription_id)
    
    if subscription:
        subscription.group_id = None
        await session.commit()
        await callback.answer("✅ Guruh olib tashlandi", show_alert=True)
        await show_channel_settings(callback, session)
    else:
        await callback.answer("❌ Xatolik", show_alert=True)

@router.callback_query(F.data.startswith("delete:"))
async def confirm_delete_channel(callback: CallbackQuery):
    subscription_id = int(callback.data.split(":")[1])
    await callback.message.edit_text(
        "⚠️ Kanalni o'chirishni xohlaysizmi?",
        reply_markup=Keyboards.confirm_delete(subscription_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete:"))
async def delete_channel(callback: CallbackQuery, session: AsyncSession):
    subscription_id = int(callback.data.split(":")[1])
    success = await ChannelService.unsubscribe(session, subscription_id)
    
    if success:
        await callback.answer("✅ Kanal o'chirildi", show_alert=True)
    else:
        await callback.answer("❌ Xatolik", show_alert=True)
    
    await show_my_channels(callback, session)
