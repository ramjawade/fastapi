from pydantic import BaseModel, Field
from typing import List
import os

class Settings(BaseModel):
    # Database settings
    DATABASE_URL: str = "postgresql://postgres:Adminrole@localhost:5432/postgres demo"
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Task API - Full CRUD Operations"
    VERSION: str = "1.0.0"
    DEBUG: bool = True  # Changed to True for debug mode
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database pool settings
    DB_POOL_MIN_SIZE: int = 5
    DB_POOL_MAX_SIZE: int = 20
    DB_COMMAND_TIMEOUT: int = 60
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Pagination defaults
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    
    # Batch operation limits
    MAX_BATCH_SIZE: int = 100
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

# Create settings instance
settings = Settings()

# Environment-specific overrides
if os.getenv("ENVIRONMENT") == "production":
    settings.DEBUG = False
    settings.BACKEND_CORS_ORIGINS = ["https://yourdomain.com"]
elif os.getenv("ENVIRONMENT") == "development":
    settings.DEBUG = True
    settings.BACKEND_CORS_ORIGINS = ["http://localhost:3000", "http://localhost:8080"]
