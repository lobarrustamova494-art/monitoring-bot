from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from config import settings
from .models import Base

class DatabaseManager:
    def __init__(self):
        # Check if using SQLite (for testing)
        is_sqlite = settings.DATABASE_URL.startswith('sqlite')
        
        if is_sqlite:
            self.engine = create_async_engine(
                settings.DATABASE_URL,
                poolclass=NullPool,
                echo=False
            )
        else:
            self.engine = create_async_engine(
                settings.DATABASE_URL,
                pool_size=settings.DATABASE_POOL_SIZE,
                max_overflow=settings.DATABASE_MAX_OVERFLOW,
                pool_pre_ping=True,
                echo=False
            )
        
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
    
    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def close(self):
        await self.engine.dispose()

db_manager = DatabaseManager()

async def get_db() -> AsyncSession:
    async with db_manager.async_session() as session:
        yield session
