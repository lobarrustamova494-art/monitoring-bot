# Quick Start Guide

## 5 daqiqada botni ishga tushiring!

### 1. Talablar

- Docker va Docker Compose o'rnatilgan bo'lishi kerak
- Telegram bot token (@BotFather dan)
- Telegram API credentials (https://my.telegram.org dan)

### 2. Loyihani clone qiling

```bash
git clone <your-repo-url>
cd telegram-news-bot
```

### 3. Environment sozlang

```bash
# .env faylini yarating
cp .env.example .env

# .env faylini tahrirlang
nano .env
```

Quyidagi qiymatlarni to'ldiring:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz  # @BotFather dan
API_ID=12345678                                    # my.telegram.org dan
API_HASH=abcdef1234567890abcdef1234567890         # my.telegram.org dan
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/newsbot
REDIS_URL=redis://redis:6379/0
```

### 4. Docker bilan ishga tushiring

```bash
# Build va run
docker-compose up -d

# Loglarni ko'ring
docker-compose logs -f bot
```

### 5. Pyrogram session yarating

Birinchi marta ishga tushirganda:

```bash
docker-compose exec -it bot python -c "from pyrogram import Client; from config import settings; app = Client('newsbot_session', api_id=settings.API_ID, api_hash=settings.API_HASH); app.start(); app.stop()"
```

Telefon raqamingizni kiriting va SMS kodini tasdiqlang.

### 6. Database migratsiya

```bash
docker-compose exec bot alembic upgrade head
```

### 7. Botni test qiling

Telegram da botingizni toping va `/start` buyrug'ini yuboring!

## Tez-tez so'raladigan savollar

### Bot ishlamayapti?

```bash
# Loglarni tekshiring
docker-compose logs bot

# Container statusini ko'ring
docker-compose ps

# Restart qiling
docker-compose restart bot
```

### Database xatosi?

```bash
# Database container tekshiring
docker-compose logs db

# Database ga ulanib ko'ring
docker-compose exec db psql -U postgres -d newsbot
```

### Pyrogram session xatosi?

```bash
# Session faylini o'chiring va qaytadan yarating
rm newsbot_session.session
docker-compose restart bot
# Qaytadan session yarating (5-qadam)
```

## Keyingi qadamlar

- [ARCHITECTURE.md](ARCHITECTURE.md) - Arxitektura haqida
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [WORKFLOW.md](WORKFLOW.md) - Ishlash algoritmi
- [PERFORMANCE.md](PERFORMANCE.md) - Performance optimizatsiyasi

## Yordam kerakmi?

- GitHub Issues: <repo-url>/issues
- Telegram: @support
- Email: support@example.com

## Makefile commands

```bash
make build      # Build Docker images
make up         # Start services
make down       # Stop services
make logs       # Show logs
make restart    # Restart bot
make clean      # Clean everything
make test       # Run tests
make migrate    # Run migrations
```

## Development mode

Local development uchun:

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependencies
pip install -r requirements.txt

# Run
python main.py
```

## Production checklist

- [ ] `.env` faylini to'ldiring
- [ ] Strong parollar o'rnating
- [ ] Firewall sozlang
- [ ] SSL sertifikat o'rnating
- [ ] Backup strategiyasini sozlang
- [ ] Monitoring o'rnating
- [ ] Log rotation sozlang
- [ ] Admin IDs ni to'ldiring

## Muvaffaqiyat!

Bot ishga tushdi! Endi siz:

1. Kanal qo'shishingiz
2. Sozlamalarni o'zgartirishingiz
3. Guruh qo'shishingiz
4. Statistikani ko'rishingiz mumkin

Omad! 🚀
