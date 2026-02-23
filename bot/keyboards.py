from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from database.models import Subscription, ForwardMode, UserGroup

class Keyboards:
    @staticmethod
    def main_menu() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📌 Mening kanallarim", callback_data="my_channels")],
            [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="add_channel")],
            [InlineKeyboardButton(text="👥 Guruhlarim", callback_data="my_groups")],
            [InlineKeyboardButton(text="📊 Statistika", callback_data="statistics")],
            [InlineKeyboardButton(text="ℹ️ Yordam", callback_data="help")]
        ])
    
    @staticmethod
    def channel_list(subscriptions: List[Subscription]) -> InlineKeyboardMarkup:
        keyboard = []
        for sub in subscriptions:
            channel_name = sub.channel.title or sub.channel.username or f"ID: {sub.channel.channel_id}"
            keyboard.append([
                InlineKeyboardButton(
                    text=f"{'✅' if sub.is_active else '❌'} {channel_name}",
                    callback_data=f"channel:{sub.id}"
                )
            ])
        keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def channel_settings(subscription_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📍 Qayerga yuborilsin", callback_data=f"set_mode:{subscription_id}")],
            [InlineKeyboardButton(text="👥 Guruh tanlash", callback_data=f"select_group:{subscription_id}")],
            [InlineKeyboardButton(text="🔍 Filtrlar", callback_data=f"filters:{subscription_id}")],
            [InlineKeyboardButton(text="✏️ Prefix qo'shish", callback_data=f"prefix:{subscription_id}")],
            [InlineKeyboardButton(text="🗑 O'chirish", callback_data=f"delete:{subscription_id}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data="my_channels")]
        ])
    
    @staticmethod
    def forward_mode_selector(subscription_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📩 Shaxsiy chatga", callback_data=f"mode:{subscription_id}:private")],
            [InlineKeyboardButton(text="👥 Guruhga", callback_data=f"mode:{subscription_id}:group")],
            [InlineKeyboardButton(text="🔁 Ikkalasiga", callback_data=f"mode:{subscription_id}:both")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"channel:{subscription_id}")]
        ])
    
    @staticmethod
    def filter_type_selector(subscription_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Hammasi", callback_data=f"filter:{subscription_id}:all")],
            [InlineKeyboardButton(text="📄 Faqat matn", callback_data=f"filter:{subscription_id}:text")],
            [InlineKeyboardButton(text="🖼 Faqat media", callback_data=f"filter:{subscription_id}:media")],
            [InlineKeyboardButton(text="🔑 Kalit so'zlar", callback_data=f"keywords:{subscription_id}")],
            [InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"channel:{subscription_id}")]
        ])
    
    @staticmethod
    def group_selector(subscription_id: int, groups: List[UserGroup]) -> InlineKeyboardMarkup:
        keyboard = []
        for group in groups:
            keyboard.append([
                InlineKeyboardButton(
                    text=f"👥 {group.group_title}",
                    callback_data=f"assign_group:{subscription_id}:{group.id}"
                )
            ])
        keyboard.append([
            InlineKeyboardButton(text="❌ Guruhni olib tashlash", callback_data=f"remove_group:{subscription_id}")
        ])
        keyboard.append([
            InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"channel:{subscription_id}")
        ])
        return InlineKeyboardMarkup(inline_keyboard=keyboard)
    
    @staticmethod
    def cancel_button() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel")]
        ])
    
    @staticmethod
    def confirm_delete(subscription_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ha, o'chirish", callback_data=f"confirm_delete:{subscription_id}")],
            [InlineKeyboardButton(text="❌ Yo'q", callback_data=f"channel:{subscription_id}")]
        ])
