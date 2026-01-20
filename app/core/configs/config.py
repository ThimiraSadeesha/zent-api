from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Zent API"
    API_VERSION: str = "v1"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # # Supabase
    # SUPABASE_URL: str = "https://adefcefrfrf.supabase.co"
    # SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"
settings = Settings()
