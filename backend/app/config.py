from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # Database - Using SQLite for testing
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Security
    SECRET_KEY: str = "IbUl-MZh4GH-j9uYjjcd7Y6weLJHNQRT0FZYMJ5vEHg"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI Model
    MODEL_NAME: str = "dbmdz/bert-base-italian-xxl-cased"  # Italian base model
    MODEL_CACHE_DIR: str = "./models"
    MAX_SEQUENCE_LENGTH: int = 512
    
    # OCR
    TESSERACT_CMD: str = "/usr/bin/tesseract"
    OCR_LANG: str = "ita"  # Italian
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Training
    BATCH_SIZE: int = 8
    LEARNING_RATE: float = 2e-5
    EPOCHS: int = 3
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create necessary directories
os.makedirs(settings.MODEL_CACHE_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True) 