from fastapi import APIRouter, HTTPException

from app.core.supabase.supabase_client import get_db

from pydantic import BaseModel
import logging
logger = logging.getLogger(__name__)

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    username: str


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register_user(data: RegisterRequest):
    supabase = get_db()

    logger.info(f"Registering user: {data.email}")

    # 1. Create Supabase auth user
    auth_response = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password,
    })

    if not auth_response.user:
        raise HTTPException(status_code=400, detail="Registration failed")

    user_id = auth_response.user.id

    # 2. Insert profile
    supabase.table("tbl_users").insert({
        "id": user_id,
        "username": data.username,
    }).execute()

    return {"message": "User registered successfully"}


@router.post("/login")
def login_user(data: LoginRequest):
    supabase = get_db()

    logger.info(f"Login attempt: {data.email}")

    auth_response = supabase.auth.sign_in_with_password({
        "email": data.email,
        "password": data.password,
    })

    if not auth_response.session:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": auth_response.session.access_token,
        "refresh_token": auth_response.session.refresh_token,
        "user": auth_response.user,
    }
