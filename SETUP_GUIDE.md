# Botni ishga tushirish yo'riqnomasi

## ✅ Bajarilgan ishlar

1. ✅ Virtual environment yaratildi
2. ✅ Barcha dependencies o'rnatildi
3. ✅ 37 ta test muvaffaqiyatli o'tdi
4. ✅ Kod tayyor

## 🔧 Keyingi qadamlar

### 1. Telegram API credentials olish

#### API_ID va API_HASH olish:

1. https://my.telegram.org ga kiring
2. "API development tools" ga o'ting
3. Yangi app yarating:
   - App title: News Bot
   - Short name: newsbot
   - Platform: Other
4. API_ID va API_HASH ni nusxalang

#### Bot Token olish:

1. Telegram da @BotFather ni toping
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Bot username kiriting (masalan: mynewsbot)
5. Token ni nusxalang

### 2. .env faylini to'ldirish

`.env` faylini oching va quyidagilarni to'ldiring:

```env
# Bot Configuration
BOT_TOKEN=sizning_bot_tokeningiz
API_ID=sizning_api_id
API_HASH=sizning_api_hash

# Database (hozircha Supabase ishlatilmoqda)
DATABASE_URL=postgresql://postgres:R4jm%7+beY8VW7t@db.ynvyucybibavubdaivgr.supabase.co:5432/postgres

# Redis (Docker bilan ishlatiladi)
REDIS_URL=redis://localhost:6379/0

# Bot Settings
MAX_CHANNELS_PER_USER=50
MAX_CHANNELS_PREMIUM=200
ADMIN_IDS=sizning_telegram_id  # @userinfobot dan olishingiz mumkin

# Monitoring
CHECK_INTERVAL=30
BATCH_SIZE=100

# Logging
LOG_LEVEL=INFO
```

### 3. Pyrogram session yaratish

Botni birinchi marta ishga tushirishdan oldin Pyrogram session yaratish kerak:

```bash
# Virtual environment ni aktivlashtiring
.\venv\Scripts\activate

# Session yaratish
python -c "from pyrogram import Client; from config import settings; app = Client('newsbot_session', api_id=settings.API_ID, api_hash=settings.API_HASH); app.start(); app.stop()"
```

Telefon raqamingizni kiriting va SMS kodini tasdiqlang.

### 4. Redis o'rnatish (Windows uchun)

#### Variant 1: Docker bilan (tavsiya etiladi)

```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

#### Variant 2: WSL bilan

```bash
wsl --install
# WSL ichida:
sudo apt update
sudo apt install redis-server
redis-server
```

#### Variant 3: Memurai (Windows native)

https://www.memurai.com/ dan yuklab oling va o'rnating.

### 5. Botni ishga tushirish

```bash
# Virtual environment ni aktivlashtiring
.\venv\Scripts\activate

# Botni ishga tushiring
python main.py
```

## 🐳 Docker bilan ishga tushirish (Production)

Agar Docker bilan ishlatmoqchi bo'lsangiz:

```bash
# Docker Compose bilan ishga tushirish
docker-compose up -d

# Loglarni ko'rish
docker-compose logs -f bot

# To'xtatish
docker-compose down
```

## 📝 Muhim eslatmalar

1. **API_ID va API_HASH** - Bu sizning shaxsiy ma'lumotlaringiz, hech kimga bermang
2. **BOT_TOKEN** - Bot tokenini ham maxfiy saqlang
3. **ADMIN_IDS** - O'z Telegram ID ingizni kiriting (@userinfobot dan olishingiz mumkin)
4. **Redis** - Bot ishlashi uchun Redis kerak
5. **Database** - Hozirda Supabase PostgreSQL ishlatilmoqda

## 🧪 Testlar

Barcha testlar muvaffaqiyatli o'tdi:

```bash
# Barcha testlarni ishga tushirish
pytest tests/ -v

# Faqat helper testlar
pytest tests/test_helpers.py -v

# Faqat service testlar
pytest tests/test_services.py -v

# Coverage bilan
pytest tests/ --cov=. --cov-report=html
```

## ❓ Muammolar

### Bot ishlamayapti?

1. `.env` faylini tekshiring
2. Redis ishlab turganini tekshiring: `redis-cli ping` (javob: PONG)
3. Loglarni ko'ring: `logs/bot.log`
4. Virtual environment aktivmi?

### Pyrogram session xatosi?

1. API_ID va API_HASH to'g'ri kiritilganini tekshiring
2. Session faylini o'chiring: `del newsbot_session.session`
3. Qaytadan session yarating

### Database xatosi?

1. DATABASE_URL to'g'ri kiritilganini tekshiring
2. Internet ulanishini tekshiring
3. Supabase database faolmi?

## 🎉 Tayyor!

Barcha sozlamalar to'g'ri bo'lsa, bot ishga tushadi va siz:

1. `/start` buyrug'i bilan botni ishga tushirishingiz
2. Kanal qo'shishingiz
3. Sozlamalarni o'zgartirishingiz
4. Guruh qo'shishingiz mumkin

Omad! 🚀
