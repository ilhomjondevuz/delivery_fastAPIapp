from fastapi import APIRouter, HTTPException, status
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
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        fullname=user.fullname,
        phone_number=user.phone_number,
    )
    session.add(new_user)
    return user