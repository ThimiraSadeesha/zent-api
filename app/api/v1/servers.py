# from fastapi import APIRouter, Depends
# from supabase import Client
# from app.db.session import get_db
# import logging
#
# router = APIRouter()
# logger = logging.getLogger(__name__)
#
#
# @router.get("/servers")
# async def get_servers(db: Client = Depends(get_db)):
#     """
#     Get all servers from database
#     """
#     try:
#         response = db.table('servers').select("*").execute()
#         logger.info(f"Retrieved {len(response.data)} servers")
#         return {
#             "status": "success",
#             "data": response.data,
#             "count": len(response.data)
#         }
#     except Exception as e:
#         logger.error(f"Failed to retrieve servers: {str(e)}")
#         return {
#             "status": "error",
#             "message": "Failed to retrieve servers",
#             "error": str(e),
#             "data": []
#         }
#
#
# @router.get("/logs")
# async def get_api_logs():
#     """
#     Get recent API logs
#     """
#     try:
#         with open('logs/app.log', 'r') as f:
#             lines = f.readlines()
#             recent_logs = lines[-100:]  # Get last 100 lines
#
#         logger.info("Retrieved API logs")
#         return {
#             "status": "success",
#             "logs": recent_logs,
#             "count": len(recent_logs)
#         }
#     except FileNotFoundError:
#         logger.warning("Log file not found")
#         return {
#             "status": "warning",
#             "message": "No logs found yet",
#             "logs": [],
#             "count": 0
#         }
#     except Exception as e:
#         logger.error(f"Failed to retrieve logs: {str(e)}")
#         return {
#             "status": "error",
#             "message": "Failed to retrieve logs",
#             "error": str(e),
#             "logs": []
#         }