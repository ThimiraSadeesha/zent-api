
from fastapi import FastAPI
from app.core.configs.config import settings
from app.core.logging.logger import setup_logging
from app.core.middleware.cors import setup_cors
from app.core.middleware.lifecycle import register_lifecycle_events


logger = setup_logging()

# App instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Middleware
setup_cors(app)
register_lifecycle_events(app, logger)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.API_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME
    }
