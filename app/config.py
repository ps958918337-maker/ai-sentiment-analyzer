"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    SECRET_KEY: str = "sentimentiq-dev-secret-key"
    DATABASE_URL: str = "sqlite:///./sentimentiq.db"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
