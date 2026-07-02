from pydantic import BaseModel
from pydantic import EmailStr


class LoginRequest(BaseModel):
    """
    Login request model.
    """

    email: EmailStr

    password: str