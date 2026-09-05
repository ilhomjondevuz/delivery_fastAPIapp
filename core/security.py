from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import jwt
from environs import Env
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status


env = Env()
env.read_env()

SECRET_KEY = env.str("JWT_SECRET_KEY")
ALGORITHM = env.str("ALGORITHM")

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/accounts/login")

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(username: str) -> str:
    tashkent_time_now = datetime.now(ZoneInfo('Asia/Tashkent'))
    expire = tashkent_time_now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def create_refresh_token(username: str) -> str:
    expire = datetime.now(ZoneInfo('Asia/Tashkent')) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": username,
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not validate credentials",
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )