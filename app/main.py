
from fastapi import FastAPI
from app.api.auth import auth
from app.core.configs.config import settings
from app.core.logging.logger import setup_logging
from app.core.middleware.cors import setup_cors
from app.core.middleware.lifecycle import register_lifecycle_events
from app.api.routes import servers, docker


logger = setup_logging()

# App instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    debug=settings.DEBUG
)

# Middleware
app = FastAPI()
setup_cors(app)
register_lifecycle_events(app, logger)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(servers.router, prefix="/api/v1/server", tags=["server"])
app.include_router(docker.router, prefix="/api/v1/docker", tags=["docker"])

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
