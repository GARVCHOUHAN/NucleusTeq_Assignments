"""
Schema for updating project.
"""

from typing import Optional

from pydantic import BaseModel
from pydantic import Field


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