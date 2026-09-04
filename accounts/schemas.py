from typing import Optional

from pydantic import BaseModel, ConfigDict


class SignupModel(BaseModel):
    username: str
    email: Optional[str] = None
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