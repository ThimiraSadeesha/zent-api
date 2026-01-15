from app.core.supabase.supabase_client import test_connection

def register_lifecycle_events(app, logger):

    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 Application starting...")
        if test_connection():
            logger.info("Supabase connected ✅")
        else:
            logger.error("Supabase connection failed ❌")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("🛑 Application shutting down")
