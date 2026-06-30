from pydantic import BaseModel
from pydantic import Field


class ProjectCreateRequest(BaseModel):

    name: str = Field(
        min_length=3,
        max_length=50
    )

    description: str = Field(
        min_length=5,
        max_length=500
    )