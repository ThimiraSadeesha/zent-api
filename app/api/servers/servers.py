from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ssh_service import ssh_connect
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class SSHLoginRequest(BaseModel):
    host: str
    username: str
    password: str = None
    port: int = 22
    key: str = None

@router.post("/ssh")
def login_server_ssh(data: SSHLoginRequest):
    client = ssh_connect(
        host=data.host,
        username=data.username,
        password=data.password,
        port=data.port,
        key=data.key
    )
    if not client:
        raise HTTPException(status_code=401, detail="SSH login failed")
    stdin, stdout, stderr = client.exec_command("uptime")
    result = stdout.read().decode().strip()
    client.close()
    return {"message": "SSH login successful", "uptime": result}
