# from supabase import create_client, Client
# from app.core.config import settings
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# class SupabaseClient:
#     _instance: Client = None
#
#     @classmethod
#     def get_client(cls) -> Client:
#         """Get Supabase client singleton"""
#         if cls._instance is None:
#             try:
#                 cls._instance = create_client(
#                     settings.SUPABASE_URL,
#                     settings.SUPABASE_KEY
#                 )
#                 logger.info("Supabase client initialized successfully")
#             except Exception as e:
#                 logger.error(f"Failed to initialize Supabase client: {e}")
#                 raise
#         return cls._instance
#
#
# def get_db() -> Client:
#     """Dependency to get Supabase client"""
#     return SupabaseClient.get_client()