import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # Bot
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    API_ID: int = int(os.getenv("API_ID", "0"))
    API_HASH: str = os.getenv("API_HASH", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    DATABASE_POOL_SIZE: int = int(os.getenv("DATABASE_POOL_SIZE", "20"))
    DATABASE_MAX_OVERFLOW: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "40"))
    
    # Redis (Optional)
    REDIS_URL: str = os.getenv("REDIS_URL", "")
    
    # Limits
    MAX_CHANNELS_PER_USER: int = int(os.getenv("MAX_CHANNELS_PER_USER", "50"))
    MAX_CHANNELS_PREMIUM: int = int(os.getenv("MAX_CHANNELS_PREMIUM", "200"))
    ADMIN_IDS: str = os.getenv("ADMIN_IDS", "")
    
    # Monitoring
    CHECK_INTERVAL: int = int(os.getenv("CHECK_INTERVAL", "30"))
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "100"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    @property
    def admin_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]

settings = Settings()
