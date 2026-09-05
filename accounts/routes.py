from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import select, or_
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.responses import JSONResponse

from core.security import create_access_token, create_refresh_token, get_current_user
from .models import User
from .schemas import SignupModel, LoginModel, RefreshTokenModel, RefreshTokenResponse, LoginResponse
from database import Session, engine

session = Session(bind=engine)

accounts_routes = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@accounts_routes.get("/")
async def accounts_base_api(current_user:str = Depends(get_current_user)) -> dict[str, str]:
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
    resp_model["id"] = new_user.id
    return resp_model

@accounts_routes.post("/login", status_code=status.HTTP_200_OK)
async def login_view(user: LoginModel) -> LoginResponse:
    result = await session.execute(
        select(User).where(
            or_(
                User.username == user.username_or_email,
                User.email == user.username_or_email)
        )
    )

    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )

    access_token = create_access_token(db_user.username)
    refresh_token = create_refresh_token(db_user.username)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
    }

@accounts_routes.post('/refresh', status_code=status.HTTP_200_OK)
async def refresh_view(refresh_token: RefreshTokenModel) -> RefreshTokenResponse:
    refresh_token = refresh_token.refresh
    user = get_current_user(refresh_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired. Logout",
        )
    access = create_access_token(user)
    return {
        'access': access,
    }