from fastapi import FastAPI
from app.api import ping, notes
from app.db import engine, metadata, database
from fastapi_users.authentication import JWTAuthentication
from settings import SECRET
from fastapi_users import FastAPIUsers
from app.db import user_db
from app.api.models import User, UserCreate, UserUpdate, UserDB
from starlette.requests import Request




metadata.create_all(engine)


app = FastAPI()


auth_backends = [
    JWTAuthentication(secret=SECRET, lifetime_seconds=3600),
]

app = FastAPI()

fastapi_users = FastAPIUsers(
    user_db, auth_backends, User, UserCreate, UserUpdate, UserDB, SECRET,
)

app.include_router(fastapi_users.router, prefix="/users", tags=["users"])



@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@fastapi_users.on_after_register()
def on_after_register(user: User, request: Request):
    print(f"User {user.id} has registered.")


@fastapi_users.on_after_forgot_password()
def on_after_forgot_password(user: User, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")




app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
