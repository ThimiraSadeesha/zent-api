import logging
from supabase import create_client, Client
from app.core.configs.config import settings

logger = logging.getLogger(__name__)


class SupabaseClient:
    _instance: Client = None
    @classmethod
    def get_client(cls) -> Client:

        if cls._instance is None:
            try:
                cls._instance = create_client(
                    supabase_url=settings.SUPABASE_URL,
                    supabase_key=settings.SUPABASE_KEY,
                )
                logger.info("Supabase client initialized successfully ✅")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client ❌: {e}")
                raise
        return cls._instance


def get_db() -> Client:
    return SupabaseClient.get_client()
def test_connection() -> bool:
    try:
        client = SupabaseClient.get_client()
        response = client.auth.get_session()
        logger.info("Supabase connection test successful ✅")
        return True
    except Exception as e:
        error_msg = str(e).lower()
        if any(phrase in error_msg for phrase in [
            "no session",
            "not authenticated",
            "jwt",
            "could not find the table",
            "pgrst"
        ]):
            logger.info("Supabase connection test successful ✅ (API reachable)")
            return True
        logger.error(f"Supabase connection test failed ❌: {e}")
        return False