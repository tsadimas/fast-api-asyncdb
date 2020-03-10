from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from settings import SECRET
from app.api.models import User, UserCreate, UserUpdate, UserDB
from app.db import user_db
from fastapi import Body, Depends, HTTPException



auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]

fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB, SECRET,
)
router = APIRouter()


@router.get("/ping")
async def pong(user: user_db = Depends(fastapi_users.authenticator.get_current_active_user)):
    return {"ping": "pong!"}
