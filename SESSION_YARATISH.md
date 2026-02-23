# Pyrogram Session Yaratish - Qadamma-qadam

## ⚠️ MUHIM!

Session yaratish **ALBATTA** kerak! Aks holda bot kanallarni kuzata olmaydi.

## 📋 Tayyorgarlik

1. ✅ .env faylida API_ID va API_HASH to'g'ri kiritilgan
2. ✅ Telefon raqamingiz tayyor
3. ✅ Telegram ochiq (SMS kod uchun)

## 🚀 Qadamlar

### 1. Terminal ochish

Windows PowerShell yoki CMD ni oching.

### 2. Virtual environment aktivlashtirish

```bash
cd "D:\Bots\News bot"
.\venv\Scripts\activate
```

### 3. Session yaratish

```bash
python create_session.py
```

### 4. Telefon raqam kiriting

```
Enter phone number or bot token: +998901234567
```

**Format**: `+` belgisi bilan, probelsiz
- ✅ To'g'ri: `+998901234567`
- ❌ Noto'g'ri: `998901234567`
- ❌ Noto'g'ri: `+998 90 123 45 67`

### 5. SMS kod kiriting

Telegram dan SMS kod keladi:

```
Enter phone code: 12345
```

5 raqamli kod kiriting.

### 6. 2FA parol (agar bor bo'lsa)

Agar Telegram da 2FA (Two-Factor Authentication) o'rnatgan bo'lsangiz:

```
Enter password: sizning_parolingiz
```

Agar yo'q bo'lsa, bu qadam o'tkazib yuboriladi.

### 7. Muvaffaqiyat!

```
✅ Session muvaffaqiyatli yaratildi!
📁 Fayl: newsbot_session.session
```

## 📁 Natija

Loyiha papkasida `newsbot_session.session` fayli paydo bo'ladi.

```
D:\Bots\News bot\
├── newsbot_session.session  ← Yangi fayl!
├── main.py
├── .env
└── ...
```

## 🎯 Keyingi qadam

Endi botni ishga tushiring:

```bash
python main.py
```

Bot endi:
- ✅ Kanallarni real-time kuzatadi
- ✅ Yangi postlarni avtomatik yuboradi
- ✅ Event-based monitoring ishlaydi

## ❓ Muammolar

### "Invalid phone number"

**Sabab**: Telefon raqam formati noto'g'ri

**Yechim**: `+` belgisi bilan boshlang, probelsiz
```
+998901234567
```

### "Phone code invalid"

**Sabab**: SMS kod noto'g'ri yoki eski

**Yechim**: 
1. Yangi kod so'rang
2. Tezroq kiriting (kod 5 daqiqa amal qiladi)

### "Password invalid"

**Sabab**: 2FA parol noto'g'ri

**Yechim**:
1. Telegram sozlamalarida 2FA parolni tekshiring
2. Agar unutgan bo'lsangiz, Telegram orqali reset qiling

### "API_ID invalid"

**Sabab**: .env faylida API_ID yoki API_HASH noto'g'ri

**Yechim**:
1. https://my.telegram.org ga kiring
2. API credentials ni qayta tekshiring
3. .env faylida to'g'rilang

### Session fayli yo'q

**Sabab**: Session yaratish muvaffaqiyatsiz bo'lgan

**Yechim**:
1. Barcha qadamlarni qaytadan bajaring
2. Xatolarni diqqat bilan o'qing
3. .env faylini tekshiring

## 🔒 Xavfsizlik

- `newsbot_session.session` fayli **maxfiy**!
- Hech kimga bermang
- Git ga commit qilmang (.gitignore da bor)
- Backup oling

## ✅ Tekshirish

Session to'g'ri yaratilganini tekshirish:

```bash
# Fayl borligini tekshirish
dir newsbot_session.session

# Botni ishga tushirish
python main.py
```

Agar session to'g'ri bo'lsa, logda ko'rasiz:
```
✅ Database and userbot initialized
✅ Event-based monitoring service started
```

## 📞 Yordam

Agar muammo hal bo'lmasa:

1. .env faylini tekshiring
2. API credentials ni qayta oling
3. Session faylini o'chiring va qaytadan yarating:
   ```bash
   del newsbot_session.session
   python create_session.py
   ```

Omad! 🚀
