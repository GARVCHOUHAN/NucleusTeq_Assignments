﻿
from enum import Enum
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserRole(str, Enum):

    ADMIN = "ADMIN"

    MEMBER = "MEMBER"

    VIEWER = "VIEWER"


class UserRegisterRequest(BaseModel):

    name: str = Field(min_length=3,max_length=50)

    email: EmailStr

    password: str = Field(min_length=8,max_length=30)

    role: UserRole