from typing import Optional

from pydantic import BaseModel


class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: Optional[str]
    fullname: Optional[str]
    phone_number: Optional[str]
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "test",
                "email": "test@mail.org",
                "fullname": "test",
                "phone": "test",
                "password": "qwerty123!",
                "is_active": True,
                "is_superuser": False,
                "is_staff": False
            }
        }