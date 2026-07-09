from datetime import date
from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator

class SprintStatus(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"


class SprintCreateRequest(BaseModel):
    name: str = Field(min_length=3, max_length=80)
    project_id: str = Field(min_length=1)
    start_date: date
    end_date: date
    status: SprintStatus = SprintStatus.PLANNED

    @field_validator("name", "project_id")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Field cannot be empty.")

        return cleaned

    @field_validator("end_date")
    @classmethod
    def validate_end_date(cls, value: date, info):
        start_date = info.data.get("start_date")

        if start_date and value < start_date:
            raise ValueError("End date cannot be before start date.")

        return value


class SprintIssueRequest(BaseModel):
    issue_id: str = Field(min_length=1)

    @field_validator("issue_id")
    @classmethod
    def validate_issue_id(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Issue id cannot be empty.")

        return cleaned
