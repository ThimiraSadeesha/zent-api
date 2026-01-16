import logging
import os
from logging.handlers import RotatingFileHandler
from app.core.configs.config import settings

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    # 1️⃣ Root logger for your app
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                "logs/app.log",
                maxBytes=10_485_760,
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("hpack.hpack").setLevel(logging.WARNING)
    return logging.getLogger(settings.PROJECT_NAME)
