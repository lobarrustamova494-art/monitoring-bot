# Telegram News Forwarding Bot

Professional darajadagi yangiliklarni kuzatuvchi Telegram bot.

## Xususiyatlar

- ✅ Telegram kanallarni real-time monitoring
- ✅ Shaxsiy chat yoki guruhga avtomatik forward
- ✅ Media (rasm, video, fayl) bilan ishlash
- ✅ Post filterlash (matn, media, kalit so'zlar)
- ✅ Duplicate xabarlarni oldini olish
- ✅ 10,000+ user va 1,000+ kanal uchun optimallashtirilgan
- ✅ PostgreSQL database
- ✅ Docker bilan deploy

## Texnologiyalar

- Python 3.11+
- Pyrogram (Telegram MTProto API)
- Aiogram 3.x (Bot API)
- PostgreSQL
- SQLAlchemy (async)
- Redis (caching)
- Docker & Docker Compose

## Tezkor boshlash

```bash
# 1. Repository clone qiling
git clone <repo-url>
cd telegram-news-bot

# 2. Environment o'zgaruvchilarni sozlang
cp .env.example .env
# .env faylini tahrirlang

# 3. Docker bilan ishga tushiring
docker-compose up -d

# 4. Database migratsiyalarni bajaring
docker-compose exec bot alembic upgrade head
```

## Arxitektura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Telegram  │─────▶│  Monitoring  │─────▶│  Forwarding │
│   Channels  │      │    Service   │      │   Service   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      ▼
                     ┌──────────────┐      ┌─────────────┐
                     │  PostgreSQL  │      │    Redis    │
                     │   Database   │      │    Cache    │
                     └──────────────┘      └─────────────┘
```

## Deployment

Batafsil deployment yo'riqnomasi uchun [DEPLOYMENT.md](DEPLOYMENT.md) ga qarang.

## Litsenziya

MIT
