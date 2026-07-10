import re
from enum import Enum

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator


class UserRole(str, Enum):
    ADMIN = "ADMIN"

    MEMBER = "MEMBER"

    VIEWER = "VIEWER"


class UserRegisterRequest(BaseModel):
    name: str = Field(min_length=3,max_length=50)
    email: EmailStr
    password: str = Field(min_length=8,max_length=30)
    role: UserRole

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        name = value.strip()
        if len(name) < 3:
            raise ValueError("Name must contain at least 3 non-space characters.")
        if re.search(r"[A-Za-z]", name) is None:
            raise ValueError("Name must contain letters.")

        return name

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if value != value.strip():
            raise ValueError("Password cannot start or end with spaces.")

        checks = [
            (r"[A-Z]", "one uppercase letter"),
            (r"[a-z]", "one lowercase letter"),
            (r"\d", "one number"),
            (r"[^A-Za-z0-9]", "one special character")
        ]

        missing = [
            message
            for pattern, message in checks
            if re.search(pattern, value) is None
        ]

        if missing:
            raise ValueError("Password must include " + ", ".join(missing) + ".")
        return value


class UserResponse(BaseModel):
    name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    