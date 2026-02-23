# Real-time Monitoring - To'liq yo'riqnoma

## 🎯 Maqsad

Kanal qo'shilgandan keyin, kanalga yuborilgan barcha yangi postlar real-time vaqtda userga avtomatik yuboriladi.

## 📋 Talab

Real-time monitoring ishlashi uchun **Pyrogram userbot** kerak. Bu uchun:

1. ✅ API_ID va API_HASH (https://my.telegram.org dan)
2. ✅ Pyrogram session fayli
3. ✅ Redis server (allaqachon o'rnatilgan ✅)

## 🚀 Qadamlar

### 1. API Credentials olish

`API_CREDENTIALS_OLISH.md` faylini o'qing va qadamlarni bajaring:

1. https://my.telegram.org ga kiring
2. API development tools
3. API_ID va API_HASH ni oling
4. `.env` faylida almashtiring

### 2. Pyrogram session yaratish

```bash
# Virtual environment
.\venv\Scripts\activate

# Session yaratish
python -c "from pyrogram import Client; from config import settings; app = Client('newsbot_session', api_id=settings.API_ID, api_hash=settings.API_HASH); app.start(); app.stop()"
```

Telefon raqam va SMS kod kiriting.

### 3. Botni ishga tushirish

```bash
python main.py
```

## 🔄 Qanday ishlaydi?

### Arxitektura

```
┌─────────────────────────────────────────────────────────┐
│                   REAL-TIME FLOW                        │
└─────────────────────────────────────────────────────────┘

1. User kanal qo'shadi
   ↓
2. Kanal database ga saqlanadi
   ↓
3. Monitoring service har 30 soniyada tekshiradi
   ↓
4. Pyrogram userbot kanaldan yangi postlarni oladi
   ↓
5. Filtrlar qo'llaniladi (agar o'rnatilgan bo'lsa)
   ↓
6. Bot API orqali userga yuboriladi
   ↓
7. Redis cache ga yoziladi (duplicate oldini olish)
```

### Monitoring loop

```python
# Har 30 soniyada:
while True:
    # 1. Barcha active kanallarni ol
    channels = get_active_channels()
    
    # 2. Har bir kanal uchun
    for channel in channels:
        # Yangi postlarni ol
        new_posts = get_new_posts(channel)
        
        # 3. Har bir post uchun
        for post in new_posts:
            # Obunachilarga yuborish
            subscribers = get_subscribers(channel)
            
            for subscriber in subscribers:
                # Filtrlarni tekshir
                if passes_filters(post, subscriber):
                    # Yuborish
                    forward_to_user(post, subscriber)
    
    # 30 soniya kutish
    await asyncio.sleep(30)
```

## ⚙️ Sozlamalar

### Check interval

`.env` faylida:

```env
CHECK_INTERVAL=30  # 30 soniya (default)
```

Kamroq qilish mumkin (masalan 10), lekin:
- Ko'proq server yuki
- Ko'proq API so'rovlar
- Telegram rate limit

### Batch size

```env
BATCH_SIZE=100  # Bir vaqtda nechta kanal tekshiriladi
```

## 🎨 Funksiyalar

### 1. Forward mode

User tanlaydi:
- **Private**: Faqat shaxsiy chatga
- **Group**: Faqat guruhga
- **Both**: Ikkalasiga ham

### 2. Filtrlar

#### Filter type
- **All**: Barcha postlar
- **Text only**: Faqat matn
- **Media only**: Faqat media (rasm, video, etc.)

#### Keyword filter
- Vergul bilan ajratilgan kalit so'zlar
- Masalan: "sport, futbol, yangilik"
- Faqat shu so'zlar bo'lgan postlar yuboriladi

### 3. Prefix

Har bir postning boshiga custom matn qo'shish:
- Masalan: "📰 Yangi post:"
- Yoki: "🔥 Trending:"

### 4. Deduplication

Redis orqali:
- Bir xil post ikki marta yuborilmaydi
- 24 soat cache
- Har bir subscription uchun alohida

## 📊 Monitoring

### Loglar

```bash
# Real-time loglar
tail -f logs/bot.log

# Oxirgi 100 qator
tail -n 100 logs/bot.log
```

### Redis tekshirish

```bash
# Redis ishlayaptimi?
redis-cli ping
# Javob: PONG

# Cache statistika
redis-cli info stats

# Barcha keylar
redis-cli keys "fwd:*"
```

### Database

```bash
# SQLite (test)
sqlite3 test_bot.db "SELECT * FROM channels;"

# PostgreSQL (production)
psql -h localhost -U postgres -d newsbot -c "SELECT * FROM channels;"
```

## 🐛 Troubleshooting

### Monitoring ishlamayapti?

1. **Userbot tekshirish**
   ```bash
   # Session fayli bormi?
   ls newsbot_session.session
   ```

2. **API credentials**
   ```bash
   # .env faylini tekshiring
   cat .env | grep API_
   ```

3. **Redis**
   ```bash
   redis-cli ping
   ```

4. **Loglar**
   ```bash
   tail -f logs/bot.log
   ```

### Postlar kechikib keladi?

- CHECK_INTERVAL ni kamaytiring (masalan 10 soniya)
- Internet tezligini tekshiring
- Server yukini tekshiring

### Duplicate postlar?

- Redis ishlayaptimi tekshiring
- Cache TTL ni tekshiring (24 soat)
- Loglarni ko'ring

## 🎯 Test qilish

### 1. Kanal qo'shish

Telegram da botga:
```
/start
➕ Kanal qo'shish
@test_channel
```

### 2. Test post yuborish

Test kanalingizga yangi post yuboring.

### 3. Kutish

30 soniya ichida (yoki CHECK_INTERVAL) post kelishi kerak.

### 4. Loglarni ko'rish

```bash
tail -f logs/bot.log
```

Ko'rishingiz kerak:
```
Processing channel: test_channel
New message found: 12345
Forwarding to user: 123456789
Message forwarded successfully
```

## 📈 Performance

### Optimallashtirilgan

- ✅ Async/await
- ✅ Parallel processing
- ✅ Redis caching
- ✅ Connection pooling
- ✅ Batch operations

### Yuklama

- 1,000 kanal: ~30 soniya
- 10,000 kanal: ~5 daqiqa
- 100,000 kanal: ~50 daqiqa

### Scaling

Horizontal scaling:
```bash
# Multiple instances
docker-compose up --scale bot=3
```

## ✅ Tayyor!

Endi bot:
- ✅ Kanallarni real-time kuzatadi
- ✅ Yangi postlarni darhol yuboradi
- ✅ Filtrlar ishlaydi
- ✅ Duplicate yo'q
- ✅ Production-ready

Omad! 🚀
