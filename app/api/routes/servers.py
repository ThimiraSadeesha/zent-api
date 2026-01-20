from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.server_service import ssh_connect, get_client, get_docker_stats
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


class SSHLoginRequest(BaseModel):
    host: str
    username: str
    password: str = None
    port: int = 22
    key: str = None


@router.post("/login")
def login_server_ssh(request: SSHLoginRequest):
    try:
        data = ssh_connect(
            host=request.host,
            username=request.username,
            password=request.password,
            port=request.port,
            key=request.key,
        )
        return {
            "status": "success",
            "data": data
        }
    except Exception as e:
        logger.error(f"SSH connection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"SSH connection failed: {str(e)}"
        )


@router.get("/docker/stats")
def docker_stats():
    client = get_client()

    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": get_docker_stats(client)
    }
