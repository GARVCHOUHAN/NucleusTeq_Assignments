from typing import Optional, Any, List, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel):
    message: str


# Issue Response Schemas
class IssueCreatedResponse(BaseModel):
    issue_id: str = Field(..., description="The ID of the created issue")


class IssueUpdatedResponse(BaseModel):
    pass


class IssueDeletedResponse(BaseModel):
    pass


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


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    page: int
    limit: int
    total: int
    pages: int


# Comment Response Schemas
class CommentCreatedResponse(BaseModel):
    comment_id: str = Field(..., description="The ID of the created comment")


class CommentUpdatedResponse(BaseModel):
    pass


class CommentDeletedResponse(BaseModel):
    pass


# Project Response Schemas
class ProjectCreatedResponse(BaseModel):
    project_id: str = Field(..., description="The ID of the created project")


class ProjectUpdatedResponse(BaseModel):
    pass


class ProjectDeletedResponse(BaseModel):
    pass


class MemberAddedResponse(BaseModel):
    pass


class MemberRemovedResponse(BaseModel):
    pass


# Sprint Response Schemas
class SprintCreatedResponse(BaseModel):
    sprint_id: str = Field(..., description="The ID of the created sprint")


class SprintStartedResponse(BaseModel):
    pass


class SprintCompletedResponse(BaseModel):
    pass


class IssueAddedToSprintResponse(BaseModel):
    pass


class IssueRemovedFromSprintResponse(BaseModel):
    pass