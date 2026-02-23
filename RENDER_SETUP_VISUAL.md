# Render.com Deploy - Vizual Qo'llanma

## 1️⃣ Web Service Yaratish

```
Render Dashboard
    ↓
[New +] tugmasi
    ↓
[Web Service] tanlash
    ↓
GitHub repo ulash
```

### Sozlamalar:
```
Name: channel-monitor-bot
Region: Oregon (US West)
Branch: main
Runtime: Python 3

Build Command: pip install -r requirements.txt
Start Command: python start.py
```

## 2️⃣ PostgreSQL Database Yaratish

```
Render Dashboard
    ↓
[New +] tugmasi
    ↓
[PostgreSQL] tanlash
    ↓
Database yaratish
```

### Database sozlamalari:
```
Name: channel-monitor-db
Region: Oregon (US West) - Web service bilan bir xil!
Plan: Free
```

### Database URL olish:
1. Database yaratilgandan keyin
2. "Info" tabiga o'ting
3. "Internal Database URL" ni nusxalang
4. Format: `postgresql://user:password@host/database`

## 3️⃣ Environment Variables Qo'shish

Web Service da "Environment" tabiga o'ting va quyidagilarni qo'shing:

```
BOT_TOKEN = 8473209623:AAEIXdzqzivVUeG7B6u07T9hknQ4MjkBdDA
API_ID = 38334951
API_HASH = 1a1c37b3594a0767bb88b957dd5bb10f
DATABASE_URL = [PostgreSQL dan olgan Internal URL]
REDIS_URL = [bo'sh qoldiring yoki o'chiring]
```

### Environment Variables qo'shish:
```
1. Web Service > Environment tab
2. [Add Environment Variable] tugmasi
3. Key va Value kiriting
4. [Save Changes]
```

## 4️⃣ Redis haqida (Optional)

### Free Plan:
- ❌ Redis/Key Value Store mavjud emas
- ✅ Bot Redis siz ham ishlaydi
- ℹ️ REDIS_URL ni bo'sh qoldiring

### Paid Plan ($7/oy):
- ✅ "New +" > "Key Value Store" (bu Redis)
- ✅ Internal URL ni REDIS_URL ga qo'shing

## 5️⃣ Deploy Jarayoni

```
[Create Web Service] tugmasi
    ↓
Building... (3-5 daqiqa)
    ↓
Deploying...
    ↓
Live! ✅
```

### Deploy logs:
```
==> Building...
==> Installing dependencies from requirements.txt
==> Build successful!
==> Starting service with 'python start.py'
==> 🌐 Web server started on port 10000
==> ✅ Message handlers registered for userbot
==> Event-based monitoring started
==> Your service is live at https://your-app.onrender.com
```

## 6️⃣ Tekshirish

### Bot test:
1. Telegram da botni oching: @take_newsbot
2. `/start` yuboring
3. Bot javob berishi kerak

### Web test:
1. Browser da oching: `https://your-app.onrender.com`
2. Landing page ko'rinishi kerak

## 7️⃣ Xatolarni Tuzatish

### "Application failed to respond"
```
Sabab: Environment variables noto'g'ri
Yechim: 
  1. Environment tab ga o'ting
  2. Barcha variables to'g'ri kiritilganini tekshiring
  3. Manual Deploy > Deploy latest commit
```

### "Database connection failed"
```
Sabab: DATABASE_URL noto'g'ri
Yechim:
  1. PostgreSQL > Info > Internal Database URL
  2. URL ni to'liq nusxalang (postgresql://... bilan boshlanadi)
  3. Environment Variables da DATABASE_URL ni yangilang
```

### "Bot not responding"
```
Sabab: BOT_TOKEN, API_ID, API_HASH noto'g'ri
Yechim:
  1. .env faylingizdan to'g'ri qiymatlarni nusxalang
  2. Environment Variables da yangilang
  3. Redeploy qiling
```

### "Session file not found"
```
Sabab: newsbot_session.session fayli yo'q
Yechim:
  1. Local da session yarating: python create_session.py
  2. Session faylni repository ga commit qiling
  3. Git push qiling
  4. Render avtomatik redeploy qiladi
```

## 8️⃣ Free Plan Limitations

```
✅ 750 soat/oy (1 service uchun)
⚠️ 15 daqiqa inactivity → sleep mode
⏱️ Sleep mode → 30 soniya wake up
❌ Redis/Key Value Store yo'q
```

### Sleep mode oldini olish:
1. UptimeRobot.com ga kiring
2. Monitor qo'shing: `https://your-app.onrender.com`
3. Har 5 daqiqada ping qiladi
4. Bot doim active bo'ladi

## 9️⃣ Logs Ko'rish

```
Render Dashboard
    ↓
Your Web Service
    ↓
[Logs] tab
    ↓
Real-time logs
```

### Foydali log qatorlari:
```
✅ "Web server started on port 10000" - Web server ishlayapti
✅ "Message handlers registered" - Userbot tayyor
✅ "Event-based monitoring started" - Monitoring ishlayapti
✅ "Forwarded message X to Y" - Xabar yuborildi
❌ "Error" - Xatolik bor, o'qing
```

## 🔟 Yangilash

Kod o'zgartirganda:
```bash
git add .
git commit -m "Update"
git push origin main
```

Render avtomatik:
1. Yangi kodni detect qiladi
2. Rebuild qiladi
3. Redeploy qiladi
4. 3-5 daqiqa

## ✅ Tayyor!

Bot ishlayapti:
- 🤖 Telegram: @take_newsbot
- 🌐 Web: https://your-app.onrender.com
- 📊 Logs: Render Dashboard > Logs
- 🔄 Auto-deploy: Git push = auto update

## Qo'shimcha Yordam

- Render Docs: https://render.com/docs
- Telegram Bot API: https://core.telegram.org/bots/api
- GitHub Repo: https://github.com/lobarrustamova494-art/monitoring-bot

## Muhim Eslatmalar

1. ⚠️ Session file (`newsbot_session.session`) repository da bo'lishi kerak
2. ⚠️ DATABASE_URL - Internal URL ishlatish (External emas!)
3. ⚠️ Region - Database va Web Service bir xil region da bo'lishi kerak
4. ⚠️ Free plan - 15 daqiqa inactivity dan keyin sleep mode
5. ✅ Redis optional - bot Redis siz ham ishlaydi
