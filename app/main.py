from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, servers
from app.core.supabase_client import test_connection
import logging
from logging.handlers import RotatingFileHandler
import os


os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler("logs/app.log", maxBytes=10_485_760, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# CORS
allowed_origins = settings.ALLOWED_ORIGINS
if isinstance(allowed_origins, str):
    allowed_origins = [origin.strip() for origin in allowed_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Routers
# app.include_router(auth.router, prefix=f"/api/{settings.API_VERSION}", tags=["auth"])
# app.include_router(servers.router, prefix=f"/api/{settings.API_VERSION}", tags=["servers"])

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.API_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Running on {settings.HOST}:{settings.PORT}")

    # Test Supabase connection
    if test_connection():
        logger.info("Supabase is connected ✅")
    else:
        logger.error("Supabase connection failed ❌")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application")

# Health and root endpoints
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.API_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    supabase_status = "connected" if test_connection() else "disconnected"
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "supabase": supabase_status
    }