from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
import logging
from app.services.docker_service import get_docker_stats, docker_start_container, docker_stop_container, \
    docker_restart_container
from app.services.server_service import get_client

logger = logging.getLogger(__name__)
router = APIRouter()


class DockerActionRequest(BaseModel):
    container_name: str


@router.get("/stats")
def docker_stats():
    client = get_client()
    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": get_docker_stats(client)
    }

@router.post("/start")
def start_container(container_name: str):
    client = get_client()
    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": docker_start_container(client, container_name)
    }


@router.post("/stop")
def stop_container(container_name: str):
    client = get_client()
    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": docker_stop_container(client, container_name)
    }


@router.post("/restart")
def restart_container(container_name: str):
    client = get_client()
    if client is None:
        raise HTTPException(status_code=400, detail="SSH not connected. Please call /ssh first.")

    return {
        "status": "success",
        "data": docker_restart_container(client, container_name)
    }