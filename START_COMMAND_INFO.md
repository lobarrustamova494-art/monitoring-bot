# ✅ Bitta Command - Ikki Service!

## start.py - Hammasi Tayyor!

`start.py` fayli allaqachon tayyor va bitta command bilan ikkalasini ham ishga tushiradi:

```bash
python start.py
```

---

## 🚀 Qanday Ishlaydi?

### 1. Web Server (Background Thread)
```python
# Port: 10000 (yoki PORT environment variable)
# Directory: web/
# Files: index.html, style.css, script.js
```

Web server background thread da ishga tushadi va landing page ni serve qiladi.

### 2. Bot (Main Thread)
```python
# Aiogram + Pyrogram
# Real-time monitoring
# Event-based forwarding
```

Bot main thread da ishga tushadi va Telegram xabarlarini qayta ishlaydi.

---

## 📋 Render da

### Docker Deploy:
```
CMD ["python", "start.py"]
```

Dockerfile allaqachon to'g'ri sozlangan. Bitta command ikkalasini ham ishga tushiradi.

### Environment Variables:
```
PORT = 10000
```

Web server shu portda ishga tushadi.

---

## 🔍 Logs

Muvaffaqiyatli ishga tushganda:

```
✅ 🌐 Web server started on port 10000
✅ Message handlers registered for userbot
✅ Event-based monitoring started
```

---

## ✅ Test Qilish

### Local:
```bash
python start.py
```

### Tekshirish:
1. Bot: Telegram da @take_newsbot → /start
2. Web: Browser da http://localhost:10000

---

## 🎉 Tayyor!

Bitta `python start.py` command:
- ✅ Web server ishga tushadi
- ✅ Bot ishga tushadi
- ✅ Ikkalasi parallel ishlaydi

Render da Docker bilan deploy qilganda avtomatik ishga tushadi!
