# Deploy Checklist ✅

Render.com ga deploy qilish uchun qadamma-qadam checklist.

## Tayyorgarlik

- [x] Kod GitHub ga yuklangan: https://github.com/lobarrustamova494-art/monitoring-bot.git
- [ ] Render.com account yaratilgan
- [ ] Session file mavjud (`newsbot_session.session`)

## 1. PostgreSQL Database

- [ ] Render.com ga kirish
- [ ] "New +" > "PostgreSQL" bosish
- [ ] Sozlamalar:
  - Name: `channel-monitor-db`
  - Region: `Oregon (US West)`
  - Plan: `Free`
- [ ] "Create Database" bosish
- [ ] Database yaratilishini kutish (2-3 daqiqa)
- [ ] "Info" tab > "Internal Database URL" ni nusxalash
- [ ] URL ni xavfsiz joyga saqlash

**Internal Database URL formati:**
```
postgresql://user:password@hostname/database
```

## 2. Web Service

- [ ] "New +" > "Web Service" bosish
- [ ] "Connect a repository" > GitHub ulash
- [ ] Repository tanlash: `monitoring-bot`
- [ ] Sozlamalar:
  - Name: `channel-monitor-bot`
  - Region: `Oregon (US West)` ⚠️ Database bilan bir xil!
  - Branch: `main`
  - Runtime: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python start.py`
  - Plan: `Free`

## 3. Environment Variables

"Environment" tabiga o'tish va quyidagilarni qo'shish:

- [ ] `BOT_TOKEN` = `8473209623:AAEIXdzqzivVUeG7B6u07T9hknQ4MjkBdDA`
- [ ] `API_ID` = `38334951`
- [ ] `API_HASH` = `1a1c37b3594a0767bb88b957dd5bb10f`
- [ ] `DATABASE_URL` = [PostgreSQL dan olgan Internal URL]
- [ ] `REDIS_URL` = `` (bo'sh qoldiring yoki butunlay o'chiring)

**Qo'shish usuli:**
1. "Add Environment Variable" tugmasi
2. Key kiriting (masalan: BOT_TOKEN)
3. Value kiriting (masalan: 8473209623:AAE...)
4. "Add" bosing
5. Barcha variables uchun takrorlang
6. "Save Changes" bosing

## 4. Deploy

- [ ] "Create Web Service" tugmasi bosish
- [ ] Build jarayonini kuzatish (3-5 daqiqa)
- [ ] "Your service is live" xabarini kutish

## 5. Tekshirish

### Bot test:
- [ ] Telegram da @take_newsbot ni ochish
- [ ] `/start` yuborish
- [ ] Bot javob berishini tekshirish
- [ ] Kanal qo'shib ko'rish

### Web test:
- [ ] Browser da `https://your-app.onrender.com` ochish
- [ ] Landing page ko'rinishini tekshirish
- [ ] "Botni Ishga Tushirish" tugmasi ishlashini tekshirish

### Logs test:
- [ ] Render Dashboard > Logs tabiga o'tish
- [ ] Quyidagi loglar ko'rinishini tekshirish:
  - ✅ "Web server started on port 10000"
  - ✅ "Message handlers registered for userbot"
  - ✅ "Event-based monitoring started"

## 6. Session File (Agar xato bo'lsa)

Agar "Session file not found" xatosi chiqsa:

- [ ] Local da terminal ochish
- [ ] `python create_session.py` ishga tushirish
- [ ] Phone number va code kiritish
- [ ] `newsbot_session.session` fayli yaratilishini tekshirish
- [ ] Git commit va push:
  ```bash
  git add newsbot_session.session
  git commit -m "Add session file"
  git push origin main
  ```
- [ ] Render avtomatik redeploy qilishini kutish

## 7. Sleep Mode Oldini Olish (Optional)

Free plan 15 daqiqa inactivity dan keyin sleep mode ga o'tadi.

- [ ] UptimeRobot.com ga kirish
- [ ] "Add New Monitor" bosish
- [ ] Sozlamalar:
  - Monitor Type: `HTTP(s)`
  - Friendly Name: `Channel Monitor Bot`
  - URL: `https://your-app.onrender.com`
  - Monitoring Interval: `5 minutes`
- [ ] "Create Monitor" bosish

## Xatolarni Tuzatish

### Agar bot ishlamasa:

1. **Logs ni tekshiring:**
   - [ ] Render Dashboard > Logs
   - [ ] Qizil "Error" qatorlarni qidiring

2. **Environment Variables ni tekshiring:**
   - [ ] Barcha 5 ta variable kiritilganini tekshiring
   - [ ] Qiymatlar to'g'ri ekanligini tekshiring
   - [ ] DATABASE_URL `postgresql://` bilan boshlanishini tekshiring

3. **Database connection:**
   - [ ] PostgreSQL service "Available" statusida ekanligini tekshiring
   - [ ] Web Service va Database bir xil region da ekanligini tekshiring

4. **Manual redeploy:**
   - [ ] Web Service > "Manual Deploy" > "Deploy latest commit"

## Tayyor! 🎉

Agar barcha checkboxlar belgilangan bo'lsa, botingiz ishlayapti!

- 🤖 Bot: @take_newsbot
- 🌐 Web: https://your-app.onrender.com
- 📊 Logs: Render Dashboard > Logs tab

## Keyingi Qadamlar

- [ ] Botni test qilish (kanal qo'shish, filtr sozlash)
- [ ] Landing page ni do'stlarga ulashish
- [ ] Uptime monitoring sozlash
- [ ] Backup strategiyasini o'ylash

## Yordam Kerakmi?

- 📖 Batafsil qo'llanma: `RENDER_SETUP_VISUAL.md`
- 🚀 Tezkor qo'llanma: `DEPLOY_QUICK.md`
- 📚 To'liq qo'llanma: `RENDER_DEPLOY.md`
- 🐛 Xatolar: `XATOLARNI_TUZATISH.md`

## Muhim Eslatmalar

⚠️ **Redis/Key Value Store:**
- Free plan da mavjud emas
- Bot Redis siz ham ishlaydi
- REDIS_URL ni bo'sh qoldiring

⚠️ **Region:**
- Database va Web Service bir xil region da bo'lishi kerak
- Tavsiya: Oregon (US West)

⚠️ **Database URL:**
- Internal Database URL ishlatish (External emas!)
- Format: `postgresql://user:password@hostname/database`

⚠️ **Session File:**
- Repository da bo'lishi kerak
- `.gitignore` da yo'q ekanligini tekshiring

✅ **Free Plan:**
- 750 soat/oy
- 15 daqiqa inactivity → sleep mode
- 30 soniya wake up time
- Uptime monitoring bilan doim active
