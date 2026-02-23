from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    API_ID: int
    API_HASH: str
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    
    # Redis (Optional)
    REDIS_URL: str = ""
    
    # Limits
    MAX_CHANNELS_PER_USER: int = 50
    MAX_CHANNELS_PREMIUM: int = 200
    ADMIN_IDS: str = ""
    
    # Monitoring
    CHECK_INTERVAL: int = 30
    BATCH_SIZE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @property
    def admin_list(self) -> List[int]:
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip()]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
