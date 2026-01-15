from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Zent API"
    API_VERSION: str = "v1"
    DEBUG: bool = True

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Supabase
    SUPABASE_URL: str = "https://likxkrjtwdtsqqpwbleu.supabase.co"
    SUPABASE_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxpa3hrcmp0d2R0c3FxcHdibGV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0NTMzNjgsImV4cCI6MjA4NDAyOTM2OH0.DMGfW7HtKYv0bK2BITpyXQSM6R5CMaqUOhcYv1Xblz0"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # <-- ignores unknown .env keys


# Create settings instance at the bottom
settings = Settings()
