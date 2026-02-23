Men Telegram uchun kanal kuzatuvchi bot yaratmoqchiman.

Bot quyidagi logika asosida ishlashi kerak:

🎯 ASOSIY VAZIFA

User botga kanal username yoki link beradi (masalan: @kunuz).

Bot:

Kanal mavjudligini tekshiradi

Bot kanalga admin ekanligini tekshiradi

Agar hammasi to‘g‘ri bo‘lsa:

Bot quyidagicha ishlashi kerak:

🔄 POST YUBORISH LOGIKASI
1️⃣ Birinchi ulanish payti

Agar user kanalni birinchi marta qo‘shayotgan bo‘lsa:

Bot o‘sha kanaldagi ENG OXIRGI POSTNI aniqlaydi

O‘sha oxirgi postni userga (yoki tanlangan guruhga) yuboradi

O‘sha postning message_id sini database ga saqlaydi

Shundan keyin monitoring boshlanadi

2️⃣ Keyingi postlar

Kanalga yangi post kelganda:

Bot yangi postning message_id sini oladi

Uni database dagi oxirgi saqlangan message_id bilan solishtiradi

Agar yangi bo‘lsa:

Postni forward qiladi (media bilan birga)

message_id ni yangilaydi

Duplicate yubormaydi

📥 Qayerga yuborish

User tanlay oladi:

Faqat o‘ziga

Faqat guruhga

Ikkalasiga

Har bir kanal uchun alohida target saqlanishi kerak.

🧠 DATABASE TALABI

Database quyidagilarni saqlashi kerak:

users
channels
subscriptions
groups
last_sent_message_id (har user + har kanal uchun alohida)

Structure:

subscription:

id

user_id

channel_id

target_type (private / group / both)

group_id (agar mavjud bo‘lsa)

last_message_id

⚙️ TEXNIK TALABLAR

Python

Telethon (kanallarni monitoring qilish uchun)

aiogram yoki pyrogram (bot interfeysi uchun)

PostgreSQL

Async architecture

Event-based channel monitoring

High performance

🔄 MONITORING USULI

Bot polling emas, event-based ishlashi kerak.

Telethon NewMessage event orqali:

Faqat qo‘shilgan kanallarni kuzatadi

Har kelgan postda:

subscription mavjudligini tekshiradi

last_message_id dan katta bo‘lsa yuboradi

📊 Qo‘shimcha talablar

Media bilan birga forward qilish

Captionni saqlash

Error handling

Rate limit protection

Agar bot guruhdan chiqarilsa log yozish

Restart bo‘lsa ham last_message_id saqlanib qolishi

🏗 Menga quyidagilarni ber:

To‘liq arxitektura

Database diagram

Papkalar strukturasi

Ishlash algoritmi

Monitoring kod skeleton

Production deployment (Docker + VPS)

10,000+ user scale qilish strategiyasi

Kod professional va kengaytiriladigan bo‘lishi kerak.

Agar user kanalni o‘chirsa, monitoring to‘xtashi kerak. Agar 100 ta user bir xil kanalni qo‘shsa, kanal faqat bitta marta monitoring qilinsin.