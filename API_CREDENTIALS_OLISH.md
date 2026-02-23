# API Credentials olish (5 daqiqa)

Real-time monitoring ishlashi uchun **ALBATTA** kerak!

## 1-qadam: Telegram API credentials olish

### https://my.telegram.org ga kiring

1. Brauzerda oching: https://my.telegram.org
2. Telefon raqamingizni kiriting (masalan: +998901234567)
3. SMS kod keladi, uni kiriting
4. Telegram parolingizni kiriting (agar o'rnatgan bo'lsangiz)

### API development tools

1. "API development tools" ga o'ting
2. Agar birinchi marta bo'lsa, forma to'ldiring:
   - **App title**: News Bot (yoki istalgan nom)
   - **Short name**: newsbot (yoki istalgan)
   - **Platform**: Other
   - **Description**: Telegram news forwarding bot
3. "Create application" tugmasini bosing

### Credentials ni nusxalang

Sizga 2 ta qiymat beriladi:

```
api_id: 12345678
api_hash: 0123456789abcdef0123456789abcdef
```

**MUHIM**: Bu ma'lumotlarni hech kimga bermang!

## 2-qadam: .env faylini yangilash

`.env` faylini oching va quyidagilarni almashtiring:

```env
API_ID=12345678
API_HASH=0123456789abcdef0123456789abcdef
```

Haqiqiy qiymatlaringizni kiriting!

## 3-qadam: Pyrogram session yaratish

Terminal da:

```bash
# Virtual environment ni aktivlashtiring
.\venv\Scripts\activate

# Session yaratish
python -c "from pyrogram import Client; from config import settings; app = Client('newsbot_session', api_id=settings.API_ID, api_hash=settings.API_HASH); app.start(); app.stop()"
```

Sizdan so'raladi:
1. **Telefon raqam**: +998901234567 formatida
2. **SMS kod**: Telegram dan kelgan kod
3. **2FA parol**: Agar o'rnatgan bo'lsangiz

Muvaffaqiyatli bo'lsa, `newsbot_session.session` fayli yaratiladi.

## 4-qadam: Botni ishga tushirish

```bash
python main.py
```

Endi bot:
- ✅ Kanallarni real-time kuzatadi
- ✅ Yangi postlarni darhol yuboradi
- ✅ Barcha media turlarini qo'llab-quvvatlaydi
- ✅ Filtrlar ishlaydi

## Nima uchun kerak?

### Bot API (BOT_TOKEN) - cheklangan
```
❌ Kanallarni kuzata olmaydi
❌ Kanal postlarini ololmaydi
✅ Faqat foydalanuvchilarga xabar yuboradi
```

### MTProto API (API_ID/HASH) - to'liq
```
✅ Kanallarni real-time kuzatadi
✅ Kanal postlarini oladi
✅ Oddiy user kabi ishlaydi
✅ Private kanallarga ham kirishi mumkin
```

## Xavfsizlik

- API_ID va API_HASH sizning shaxsiy ma'lumotlaringiz
- Session fayli (.session) ham maxfiy
- .gitignore da bor, Git ga commit bo'lmaydi
- Hech kimga bermang!

## Muammolar?

### "Invalid phone number"
- To'g'ri formatda kiriting: +998901234567
- Probel va boshqa belgilar bo'lmasin

### "Phone code invalid"
- SMS kodni to'g'ri kiriting
- Eski kod bo'lsa, yangi kod so'rang

### "Session file not found"
- Session yaratish buyrug'ini qayta bajaring
- .session fayli loyiha papkasida bo'lishi kerak

## Tayyor!

API credentials olgandan keyin bot to'liq ishlaydi! 🚀
