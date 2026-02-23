from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from services import UserService
from bot.keyboards import Keyboards

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, session: AsyncSession):
    await UserService.get_or_create_user(
        session,
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    
    text = (
        "👋 Assalomu alaykum!\n\n"
        "Men Telegram kanallarni kuzatuvchi botman.\n\n"
        "🎯 Nima qila olaman:\n"
        "• Siz tanlagan kanallarni kuzataman\n"
        "• Yangi postlarni sizga yoki guruhga yuboraman\n"
        "• Postlarni filtrlayman\n"
        "• Statistika ko'rsataman\n\n"
        "Boshlash uchun quyidagi tugmalardan foydalaning:"
    )
    
    await message.answer(text, reply_markup=Keyboards.main_menu())

@router.callback_query(F.data == "main_menu")
async def show_main_menu(callback: CallbackQuery):
    text = "Asosiy menyu. Kerakli bo'limni tanlang:"
    await callback.message.edit_text(text, reply_markup=Keyboards.main_menu())
    await callback.answer()

@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    text = (
        "📖 Yordam\n\n"
        "1️⃣ Kanal qo'shish:\n"
        "• 'Kanal qo'shish' tugmasini bosing\n"
        "• Kanal username yoki linkini yuboring\n"
        "• Bot kanalga admin bo'lishi kerak\n\n"
        "2️⃣ Sozlamalar:\n"
        "• Har bir kanal uchun alohida sozlash mumkin\n"
        "• Qayerga yuborilishini tanlang\n"
        "• Filtrlar o'rnating\n\n"
        "3️⃣ Guruh:\n"
        "• Botni guruhga qo'shing\n"
        "• Admin qiling\n"
        "• Sozlamalarda guruhni tanlang\n\n"
        "❓ Savollar bo'lsa: @support"
    )
    await callback.message.edit_text(text, reply_markup=Keyboards.main_menu())
    await callback.answer()

@router.callback_query(F.data == "cancel")
async def cancel_action(callback: CallbackQuery):
    await callback.message.edit_text(
        "❌ Bekor qilindi",
        reply_markup=Keyboards.main_menu()
    )
    await callback.answer()
