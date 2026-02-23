# Kanal qo'shishda xato - Debug

## Muammo

Kanal linkini berganda: "❌ Bu kanal emas. Faqat kanallarni qo'shish mumkin."

## Sabab

Pyrogram va Aiogram da `chat.type` turlicha ishlaydi:

### Pyrogram (userbot)
```python
from pyrogram.enums import ChatType

chat.type = ChatType.CHANNEL  # Enum
chat.type = ChatType.SUPERGROUP  # Enum
```

### Aiogram (bot)
```python
chat.type = "channel"  # String
chat.type = "supergroup"  # String
```

## Yechim

Kod yangilandi - ikkala variantni ham qo'llab-quvvatlaydi:

```python
# Check if it's a channel or supergroup
if hasattr(chat_type, 'value'):
    # Pyrogram ChatType enum
    is_channel = chat_type in [ChatType.CHANNEL, ChatType.SUPERGROUP]
else:
    # Aiogram string type
    is_channel = str(chat_type).lower() in ["channel", "supergroup"]
```

## Test qilish

1. Bot ishga tushganini tekshiring
2. Telegram da botga `/start` yuboring
3. "Kanal qo'shish" tugmasini bosing
4. Kanal linkini yuboring:
   - `@channelname`
   - `https://t.me/channelname`

## Qo'llab-quvvatlanadigan formatlar

✅ `@channelname`
✅ `https://t.me/channelname`
✅ `http://t.me/channelname`
✅ `t.me/channelname`
✅ `channelname` (5+ belgi)

## Agar yana xato chiqsa

Loglarni ko'ring:

```bash
# Oxirgi 50 qator
Get-Content logs/bot.log -Tail 50

# Real-time
Get-Content logs/bot.log -Wait
```

Yoki terminalda:
```bash
python main.py
```

Xato haqida ma'lumot logda bo'ladi.

## Umumiy xatolar

### "Kanal topilmadi"
- Kanal username noto'g'ri
- Kanal private
- Kanal mavjud emas

### "Bu kanal emas"
- Guruh yuborilgan (kanal emas)
- Bot yoki user

### "Bot kanalga admin emas"
- Bot kanalga admin qilinmagan
- Faqat public kanallar uchun admin bo'lish shart emas

## Muvaffaqiyatli natija

Agar hammasi to'g'ri bo'lsa:

```
✅ Kanal qo'shildi: Kanal nomi
📨 Oxirgi post yuborildi.
✅ Monitoring faol. Yangi postlar avtomatik yuboriladi.
```

Keyin kanalga yangi post yuboring - bot avtomatik sizga yuboradi!
