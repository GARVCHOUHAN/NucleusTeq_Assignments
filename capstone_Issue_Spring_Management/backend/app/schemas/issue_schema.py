from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import field_validator

from app.constants import (
    ISSUE_TITLE_MAX_LENGTH,
    ISSUE_TITLE_MIN_LENGTH,
    ISSUE_DESCRIPTION_MAX_LENGTH,
    ISSUE_DESCRIPTION_MIN_LENGTH,
    ISSUE_KEY_MAX_LENGTH,
    ISSUE_STORY_POINTS_MIN,
    ISSUE_STORY_POINTS_MAX
)


class IssueType(str, Enum):
    TASK = "TASK"
    BUG = "BUG"
    STORY = "STORY"


class IssuePriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class IssueStatus(str, Enum):
    BACKLOG = "BACKLOG"
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    REVIEW = "REVIEW"
    DONE = "DONE"


class IssueCreateRequest(BaseModel):
    title: str = Field(
        min_length=ISSUE_TITLE_MIN_LENGTH,
        max_length=ISSUE_TITLE_MAX_LENGTH
    )
    description: str = Field(
        min_length=ISSUE_DESCRIPTION_MIN_LENGTH,
        max_length=ISSUE_DESCRIPTION_MAX_LENGTH
    )
    project_id: str = Field(
        min_length=1,
        max_length=ISSUE_KEY_MAX_LENGTH
    )
    parent_id: Optional[str] = None
    assignee_email: Optional[EmailStr] = None
    issue_type: IssueType = IssueType.TASK
    priority: IssuePriority = IssuePriority.MEDIUM
    story_points: int = Field(
        default=0,
        ge=ISSUE_STORY_POINTS_MIN,
        le=ISSUE_STORY_POINTS_MAX
    )
    status: IssueStatus = IssueStatus.TODO

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Field cannot be empty.")

        return cleaned

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: str) -> str:
        project_id = value.strip()

        if not project_id:
            raise ValueError("Project id cannot be empty.")

        return project_id


class IssueUpdateRequest(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=ISSUE_TITLE_MIN_LENGTH,
        max_length=ISSUE_TITLE_MAX_LENGTH
    )
    description: Optional[str] = Field(
        default=None,
        min_length=ISSUE_DESCRIPTION_MIN_LENGTH,
        max_length=ISSUE_DESCRIPTION_MAX_LENGTH
    )
    assignee_email: Optional[EmailStr] = None
    issue_type: Optional[IssueType] = None
    priority: Optional[IssuePriority] = None
    story_points: Optional[int] = Field(
        default=None,
        ge=ISSUE_STORY_POINTS_MIN,
        le=ISSUE_STORY_POINTS_MAX
    )

    @field_validator("title", "description")
    @classmethod
    def validate_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value

        cleaned = value.strip()

        if not cleaned:
            raise ValueError("Field cannot be empty.")

        return cleaned


class IssueStatusUpdateRequest(BaseModel):
    status: IssueStatus


class IssueResponse(BaseModel):
    id: Optional[str] = None
    issue_key: Optional[str] = None
    title: str
    description: str
    project_id: Optional[str] = None
    parent_id: Optional[str] = None
    reporter: Optional[str] = None
    assignee: Optional[str] = None
    issue_type: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    story_points: Optional[int] = None
