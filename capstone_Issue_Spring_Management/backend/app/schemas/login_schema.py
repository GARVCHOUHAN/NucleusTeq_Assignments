from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class LoginRequest(BaseModel):
    email: EmailStr

    password: str = Field(min_length=1)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def password_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password is required.")

        return value
