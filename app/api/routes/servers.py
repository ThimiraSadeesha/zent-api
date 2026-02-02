from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.utils.encryption import encryption_service
from app.services.server_service import ssh_connect, get_client
import logging
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter()



class SSHLoginRequest(BaseModel):
    host: str
    username: str
    password: Optional[str] = None
    port: int = 22
    key: Optional[str] = None

@router.post("/login")
def login_server_ssh(request: SSHLoginRequest):
    try:

        host = encryption_service.decrypt(request.host)
        username = encryption_service.decrypt(request.username)

        password = (
            encryption_service.decrypt(request.password)
            if request.password else None
        )

        key = (
            encryption_service.decrypt(request.key)
            if request.key else None
        )

        data = ssh_connect(
            host=host,
            username=username,
            password=password,
            port=request.port,
            key=key,
        )

        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        logger.error(f"SSH connection error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="SSH connection failed"
        )


@router.get("/reboot")
def reboot_server_route():
    client = get_client()
    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": "System is rebooting..."
    }

