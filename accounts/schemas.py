from typing import Optional

from environs import Env
from pydantic import BaseModel, ConfigDict


env = Env()
env.read_env()

class SignupModel(BaseModel):
    username: str
    email: str
    fullname: Optional[str] = None
    phone_number: Optional[str] = None
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            'example': {
                "username": "testuser",
                "email": "test@mail.com",
                "fullname": "Test User",
                "phone_number": "+998901234567",
                "password": "qwerty123!"
            }
        }
    )

class SettingsModel(BaseModel):
    authjwt_secret_key: str = env.str("AUTHJWT_SECRET_KEY")

class LoginModel(BaseModel):
    username_or_email: str
    password: str