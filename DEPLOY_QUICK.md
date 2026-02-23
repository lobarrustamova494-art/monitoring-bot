# Quick Deploy Guide

## 1. GitHub ga yuklash
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

## 2. Render.com Setup
1. https://render.com ga kiring
2. "New +" > "Web Service"
3. GitHub repo ni ulang
4. Sozlamalar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python start.py`

## 3. Environment Variables
```
BOT_TOKEN=your_token
API_ID=your_id
API_HASH=your_hash
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

## 4. Database & Redis
- "New +" > "PostgreSQL" - Database yarating
- "New +" > "Key Value Store" - Redis yarating (Optional, free plan da yo'q)
- URL larni Environment Variables ga qo'shing

**Eslatma:** Free plan da Redis (Key Value Store) mavjud emas. REDIS_URL ni bo'sh qoldiring yoki o'chirmasangiz ham bo'ladi - bot Redis siz ham ishlaydi.

## 5. Deploy
"Create Web Service" > Kutish > Tayyor! ✅

## URLs
- Bot: `@take_newsbot`
- Web: `https://your-app.onrender.com`

## Test
```bash
# Bot test
Telegram: /start

# Web test
Browser: https://your-app.onrender.com
```

Batafsil: `RENDER_DEPLOY.md` ni o'qing
