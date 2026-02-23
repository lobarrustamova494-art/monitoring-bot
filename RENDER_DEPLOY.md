# Render.com ga Deploy Qilish

## 1. Tayyorgarlik

### Kerakli fayllar:
- ✅ `start.py` - Bot va web serverni parallel ishga tushiradi
- ✅ `render.yaml` - Render konfiguratsiyasi
- ✅ `runtime.txt` - Python versiyasi
- ✅ `Procfile` - Start command
- ✅ `requirements.txt` - Dependencies

## 2. Render.com da Sozlash

### 2.1. Repository yarating
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2.2. Render.com ga kiring
1. https://render.com ga kiring
2. "New +" tugmasini bosing
3. "Web Service" ni tanlang

### 2.3. Repository ulang
1. GitHub repository ni ulang
2. Repository ni tanlang

### 2.4. Sozlamalar
- **Name:** `channel-monitor-bot`
- **Region:** Oregon (US West)
- **Branch:** `main`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python start.py`

### 2.5. Environment Variables
Quyidagi environment variables ni qo'shing:

```
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id_here
API_HASH=your_api_hash_here
DATABASE_URL=postgresql://user:password@host:5432/dbname
REDIS_URL=redis://host:6379/0
```

**Muhim:** 
- `DATABASE_URL` - Render PostgreSQL database yarating va URL ni oling
- `REDIS_URL` - Render Redis instance yarating va URL ni oling

## 3. Database Setup

### 3.1. PostgreSQL yarating
1. Render dashboard da "New +" > "PostgreSQL"
2. Database yarating
3. Internal Database URL ni nusxalang
4. Environment Variables ga `DATABASE_URL` sifatida qo'shing

### 3.2. Redis yarating
1. Render dashboard da "New +" > "Redis"
2. Redis instance yarating
3. Internal Redis URL ni nusxalang
4. Environment Variables ga `REDIS_URL` sifatida qo'shing

## 4. Session File

Pyrogram session file (`newsbot_session.session`) ni local da yarating:

```bash
python create_session.py
```

Keyin session file ni Render ga yuklash uchun:
1. Session file ni base64 ga encode qiling
2. Environment variable sifatida qo'shing
3. `start.py` da decode qilib faylga yozing

Yoki oddiyroq: Session file ni repository ga commit qiling (xavfsiz bo'lsa)

## 5. Deploy

1. "Create Web Service" tugmasini bosing
2. Render avtomatik build va deploy qiladi
3. 5-10 daqiqa kutib turing

## 6. Tekshirish

Deploy tugagandan keyin:
- Bot ishlayotganini tekshiring: Telegram da `/start` yuboring
- Web sahifa ochilishini tekshiring: `https://your-app.onrender.com`

## 7. Logs

Loglarni ko'rish uchun:
1. Render dashboard ga kiring
2. Service ni tanlang
3. "Logs" tabini oching

## 8. Xatolarni Tuzatish

### Bot ishlamayapti:
- Environment variables to'g'ri kiritilganini tekshiring
- Logs ni ko'ring
- Database va Redis ulanganini tekshiring

### Web sahifa ochilmayapti:
- PORT environment variable avtomatik o'rnatiladi
- `start.py` da port to'g'ri o'qilayotganini tekshiring

### Session xatosi:
- Session file mavjudligini tekshiring
- API_ID va API_HASH to'g'ri ekanligini tekshiring

## 9. Free Plan Limitations

Render free plan:
- 750 soat/oy (1 service uchun)
- 15 daqiqa inactivity dan keyin sleep mode
- Sleep mode dan 30 soniyada wake up

**Yechim:** Uptime monitoring service ishlatish (UptimeRobot, cron-job.org)

## 10. Production Optimizatsiya

### 10.1. Gunicorn ishlatish (optional)
```bash
pip install gunicorn
```

`start.py` ni yangilang:
```python
# Web server uchun gunicorn ishlatish
```

### 10.2. Logging
Render logs avtomatik yig'iladi, lekin qo'shimcha:
- Sentry.io integratsiyasi
- Custom logging service

### 10.3. Monitoring
- Render metrics
- Custom health check endpoint
- Uptime monitoring

## 11. Yangilash

Yangi kod push qilganda avtomatik deploy bo'ladi:
```bash
git add .
git commit -m "Update"
git push origin main
```

## 12. Backup

Database backup:
1. Render dashboard > Database > Backups
2. Manual backup olish
3. Automatic backup sozlash

## Qo'shimcha Ma'lumot

- Render docs: https://render.com/docs
- Telegram Bot API: https://core.telegram.org/bots/api
- Pyrogram docs: https://docs.pyrogram.org

## Support

Muammo bo'lsa:
- Render support: https://render.com/support
- GitHub Issues: YOUR_REPO_URL/issues
