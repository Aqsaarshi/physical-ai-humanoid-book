from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    gemini_api_key: str
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    database_url: str
    cohere_api_key: Optional[str] = None
    neon_db_url: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()