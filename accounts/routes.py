from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User
from .schemas import SignupModel
from database import Session, engine

session = Session(bind=engine)

accounts_routes = APIRouter(
    prefix="/accounts",
)

@accounts_routes.get("/")
async def accounts_base_api() -> dict[str, str]:
    return {
        'message': 'Welcome to Accounts API',
    }

@accounts_routes.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup_api(user: SignupModel):
    result = await session.execute(
        select(User).where(User.email == user.email)
    )
    db_email = result.scalar_one_or_none()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    result = await session.execute(
        select(User).where(User.username == user.username)
    )
    db_username = result.scalar_one_or_none()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        fullname=user.fullname,
        phone_number=user.phone_number,
    )
    resp_model = {
        "username": new_user.username,
        "email": new_user.email,
        "fullname": new_user.fullname,
        "phone_number": new_user.phone_number,
    }
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return resp_model