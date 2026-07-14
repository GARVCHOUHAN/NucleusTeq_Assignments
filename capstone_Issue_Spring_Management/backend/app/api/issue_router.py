from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status
from typing import List

from pydantic import BaseModel

from app.dependencies.auth_dependency import require_member
from app.schemas.issue_schema import (
    IssueCreateRequest,
    IssueStatusUpdateRequest,
    IssueUpdateRequest,
)
from app.schemas.response_schema import (
    IssueCreatedResponse,
    IssueUpdatedResponse,
    IssueDeletedResponse,
    IssueResponse,
    PaginatedResponse
)
from app.services.issue_service import IssueService

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_issue(
    issue: IssueCreateRequest,
    current_user: dict = Depends(require_member)
) -> dict:
    result = IssueService.create_issue(issue, current_user)
    return {
        **result.model_dump(),
        "message": "Issue created successfully."
    }


def _serialize_result(item):
    if isinstance(item, BaseModel):
        return item.model_dump()
    return item


@router.get("", status_code=status.HTTP_200_OK)
def get_all_issues(
    project_id: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    assignee: str | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    paginated: bool = Query(default=False),
    current_user: dict = Depends(require_member)
) -> dict | list[dict]:
    result = IssueService.search_issues(
        current_user=current_user,
        project_id=project_id,
        status=status_filter,
        assignee_email=assignee,
        search=search,
        page=page,
        limit=limit,
        paginated=paginated
    )
    
    if isinstance(result, PaginatedResponse):
        return result.model_dump()
    
    return [_serialize_result(item) for item in result]


@router.get("/{issue_id}")
def get_issue_by_id(
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = IssueService.get_issue_by_id(issue_id, current_user)
    return result.model_dump() if isinstance(result, IssueResponse) else result


@router.get("/project/{project_id}")
def get_project_issues(
    project_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> list:
    result = IssueService.get_issues_by_project(project_id, current_user)
    return [_serialize_result(item) for item in result]


@router.get("/{issue_id}/assigned/me")
def get_assigned_issues(current_user: dict = Depends(require_member)) -> list:
    result = IssueService.get_assigned_issues(current_user)
    return [_serialize_result(item) for item in result]


@router.get("/{issue_id}/subtasks")
def get_subtasks(
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> list:
    result = IssueService.get_subtasks(issue_id, current_user)
    return [_serialize_result(item) for item in result]


@router.patch("/{issue_id}")
def update_issue(
    issue_id: str,
    issue: IssueUpdateRequest,
    current_user: dict = Depends(require_member)
) -> dict:
    result = IssueService.update_issue(issue_id, issue.model_dump(exclude_unset=True), current_user)
    return {
        **result.model_dump(),
        "message": "Issue updated successfully."
    }


@router.patch("/{issue_id}/status")
def update_issue_status(
    issue_id: str,
    status_update: IssueStatusUpdateRequest,
    current_user: dict = Depends(require_member)
) -> dict:
    result = IssueService.update_issue_status(issue_id, status_update.status.value, current_user)
    return {
        **result.model_dump(),
        "message": "Issue status updated successfully."
    }


@router.delete("/{issue_id}")
def delete_issue(
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = IssueService.delete_issue(issue_id, current_user)
    return {
        **result.model_dump(),
        "message": "Issue deleted successfully."
    }
