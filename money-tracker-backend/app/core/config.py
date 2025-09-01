import os
from typing import Optional

class Settings:
    """Application settings and configuration."""
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql+psycopg2://postgres:postgres@localhost:5433/money_tracker"
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: list = ["http://localhost:3000"]
    
    # App settings
    APP_TITLE: str = "Money Tracker API"
    APP_VERSION: str = "1.0.0"

settings = Settings()
