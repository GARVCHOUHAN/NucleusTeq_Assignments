from typing import List
from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator
from app.constants import (
    PROJECT_DESCRIPTION_MAX_LENGTH,
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_KEY_MAX_LENGTH,
    PROJECT_KEY_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH
)

class ProjectMember(BaseModel):
    email: EmailStr

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()


class ProjectCreateRequest(BaseModel):
    name: str = Field(
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )

    description: str = Field(
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH
    )

    project_key: str = Field(
        min_length=PROJECT_KEY_MIN_LENGTH,
        max_length=PROJECT_KEY_MAX_LENGTH
    )

    members: List[ProjectMember] = Field(default_factory=list)

    @field_validator("name", "description")
    @classmethod
    def validate_text(cls, value: str) -> str:
        stripped_value = value.strip()

        if not stripped_value:
            raise ValueError("Field cannot be empty.")

        return stripped_value

    @field_validator("project_key")
    @classmethod
    def validate_project_key(cls, value: str) -> str:
        project_key = value.strip().upper()

        if not project_key.replace("_", "").isalnum():
            raise ValueError("Project key can contain only letters, numbers, and underscores.")

        return project_key


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )

    description: Optional[str] = Field(
        default=None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH,
        max_length=PROJECT_DESCRIPTION_MAX_LENGTH
    )

    project_key: Optional[str] = Field(
        default=None,
        min_length=PROJECT_KEY_MIN_LENGTH,
        max_length=PROJECT_KEY_MAX_LENGTH
    )

    @field_validator("name", "description")
    @classmethod
    def validate_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("Field cannot be empty.")
        return stripped_value

    @field_validator("project_key")
    @classmethod
    def validate_optional_project_key(cls,value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        project_key = value.strip().upper()
        if not project_key.replace("_", "").isalnum():
            raise ValueError("Project key can contain only letters, numbers, and underscores.")

        return project_key
