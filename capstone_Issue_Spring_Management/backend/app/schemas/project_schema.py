from typing import List

from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr


class ProjectMember(BaseModel):

    email: EmailStr

from app.core.project_constants import *


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

    members: List[ProjectMember] = []
    
"""
Schema for updating project.
"""

from typing import Optional


class ProjectUpdateRequest(BaseModel):

    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50
    )

    description: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=500
    )

    project_key: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=10
    )