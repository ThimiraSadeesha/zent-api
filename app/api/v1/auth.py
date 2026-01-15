# from fastapi import APIRouter, Depends, HTTPException, status
# from supabase import Client
#
# import logging
#
# router = APIRouter()
# logger = logging.getLogger(__name__)
#
#
# @router.post("/test-connection")
# async def test_supabase_connection(db: Client = Depends(get_db)):
#     """
#     Test Supabase connection and return database info
#     """
#     try:
#         # Try to execute a simple query to test connection
#         # This attempts to query a hypothetical 'users' table
#         # Adjust table name based on your actual schema
#         # response = db.table('users').select("count", count='exact').execute()
#
#         logger.info("Supabase connection test successful")
#
#         return {
#             "status": "success",
#             "message": "Successfully connected to Supabase",
#             "database_url": db.supabase_url,
#             "connection": "active"
#         }
#     except Exception as e:
#         logger.error(f"Supabase connection test failed: {str(e)}")
#         return {
#             "status": "error",
#             "message": "Failed to connect to Supabase",
#             "error": str(e),
#             "connection": "failed"
#         }
#
#
# @router.get("/connection-status")
# async def get_connection_status(db: Client = Depends(get_db)):
#     """
#     Get current Supabase connection status
#     """
#     try:
#         is_connected = db is not None
#         logger.info(f"Connection status check: {'connected' if is_connected else 'disconnected'}")
#
#         return {
#             "connected": is_connected,
#             "database_url": db.supabase_url if is_connected else None,
#             "timestamp": None
#         }
#     except Exception as e:
#         logger.error(f"Connection status check failed: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to check connection status: {str(e)}"
#         )