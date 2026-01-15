from fastapi.middleware.cors import CORSMiddleware
from app.core.configs.config import settings

def setup_cors(app):
    allowed_origins = settings.ALLOWED_ORIGINS

    if isinstance(allowed_origins, str):
        allowed_origins = [
            origin.strip()
            for origin in allowed_origins.split(",")
            if origin.strip()
        ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
