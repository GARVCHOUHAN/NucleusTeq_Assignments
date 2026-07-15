from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


class CommentCreateRequest(BaseModel):
    body: str = Field(min_length=1, max_length=1000)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Comment cannot be empty.")

        return cleaned


class CommentUpdateRequest(BaseModel):
    body: str = Field(min_length=1, max_length=1000)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Comment cannot be empty.")

        return cleaned
