from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import field_validator


class ProjectMemberRequest(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()
