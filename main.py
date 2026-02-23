import asyncio
import sys
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from pyrogram import Client
from config import settings
from database import db_manager
from bot.handlers import start, channels, groups, statistics, admin
from services import MonitoringService
from services.event_monitoring_service import EventMonitoringService

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL
)
logger.add(
    "logs/bot.log",
    rotation="100 MB",
    retention="30 days",
    level=settings.LOG_LEVEL
)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Initialize Pyrogram userbot
userbot = Client(
    "newsbot_session",
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    workdir="."
)

# Global monitoring service
monitoring_service = None

# Register routers
dp.include_router(start.router)
dp.include_router(channels.router)
dp.include_router(groups.router)
dp.include_router(statistics.router)
dp.include_router(admin.router)

# Middleware to inject dependencies
@dp.update.outer_middleware()
async def db_session_middleware(handler, event, data):
    async with db_manager.async_session() as session:
        data["session"] = session
        data["userbot"] = userbot
        return await handler(event, data)

async def on_startup():
    global monitoring_service
    
    logger.info("Starting bot...")
    await db_manager.init_db()
    
    # Try to start userbot if credentials are valid
    try:
        if settings.API_ID != 12345678 and settings.API_HASH != "0123456789abcdef0123456789abcdef":
            await userbot.start()
            logger.info("Database and userbot initialized")
            
            # Start event-based monitoring service
            monitoring_service = EventMonitoringService(userbot, bot)
            await monitoring_service.init_redis()
            
            # Register handlers BEFORE starting monitoring
            monitoring_service.register_handlers()
            
            # Start monitoring without passing session
            asyncio.create_task(monitoring_service.start_monitoring(None))
            
            logger.info("Event-based monitoring service started")
        else:
            logger.warning("Using test API credentials - userbot disabled")
            logger.warning("Get real credentials from https://my.telegram.org")
            logger.info("Database initialized (without userbot)")
    except Exception as e:
        logger.error(f"Failed to start userbot: {e}")
        logger.warning("Bot will work without monitoring")
        logger.info("Database initialized (without userbot)")
    
    logger.info("Bot started successfully")

async def on_shutdown():
    global monitoring_service
    
    logger.info("Shutting down bot...")
    
    # Stop monitoring service
    if monitoring_service:
        await monitoring_service.stop_monitoring()
    
    # Stop userbot
    try:
        if userbot.is_connected:
            await userbot.stop()
    except:
        pass
    
    await db_manager.close()
    await bot.session.close()
    logger.info("Bot stopped")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    
    try:
        # Run aiogram polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        await on_shutdown()

if __name__ == "__main__":
    try:
        # Run both aiogram and pyrogram together
        loop = asyncio.get_event_loop()
        
        # Start pyrogram in background
        async def run_both():
            # Start aiogram
            aiogram_task = asyncio.create_task(main())
            
            # Give aiogram time to start
            await asyncio.sleep(15)
            
            # Start pyrogram (this will keep running)
            if userbot.is_connected:
                logger.info("Pyrogram userbot is running and listening for updates...")
            
            await aiogram_task
        
        loop.run_until_complete(run_both())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
