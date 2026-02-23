"""Create Pyrogram session file"""
import asyncio
from pyrogram import Client
from config import settings

async def create_session():
    print("=" * 50)
    print("Pyrogram Session yaratish")
    print("=" * 50)
    print(f"\nAPI_ID: {settings.API_ID}")
    print(f"API_HASH: {settings.API_HASH[:10]}...")
    print("\nTelefon raqamingizni kiriting (masalan: +998901234567)")
    print("SMS kod keladi, uni kiriting")
    print("Agar 2FA o'rnatgan bo'lsangiz, parolni kiriting")
    print("=" * 50)
    
    app = Client(
        "newsbot_session",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        workdir="."
    )
    
    try:
        await app.start()
        print("\n✅ Session muvaffaqiyatli yaratildi!")
        print("📁 Fayl: newsbot_session.session")
        print("\nEndi botni ishga tushirishingiz mumkin:")
        print("python main.py")
        await app.stop()
    except Exception as e:
        print(f"\n❌ Xato: {e}")
        print("\nIltimos, .env faylida API_ID va API_HASH to'g'riligini tekshiring")

if __name__ == "__main__":
    asyncio.run(create_session())
