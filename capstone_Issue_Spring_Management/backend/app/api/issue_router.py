from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status

from app.dependencies.auth_dependency import require_member
from app.schemas.issue_schema import (
    IssueCreateRequest,
    IssueStatusUpdateRequest,
    IssueUpdateRequest
)
from app.services.issue_service import IssueService

router = APIRouter(
    prefix="/issues",
    tags=["Issues"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_issue(
    issue: IssueCreateRequest,
    current_user: dict = Depends(require_member)
):
    return IssueService.create_issue(
        issue,
        current_user
    )


@router.get("")
def get_all_issues(
    project_id: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    assignee: str | None = Query(default=None),
    search: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    paginated: bool = Query(default=False),
    current_user: dict = Depends(require_member)
):
    return IssueService.search_issues(
        current_user=current_user,
        project_id=project_id,
        status=status_filter,
        assignee_email=assignee,
        search=search,
        page=page,
        limit=limit,
        paginated=paginated
    )


@router.get("/{issue_id}")
def get_issue_by_id(
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
):
    return IssueService.get_issue_by_id(
        issue_id,
        current_user
    )


@router.get("/project/{project_id}")
def get_project_issues(
    project_id: str = Path(...),
    current_user: dict = Depends(require_member)
):
    return IssueService.get_issues_by_project(
        project_id,
        current_user
    )


@router.get("/assigned/me")
def get_assigned_issues(
    current_user: dict = Depends(require_member)
):
    return IssueService.get_assigned_issues(
        current_user
    )


@router.patch("/{issue_id}")
def update_issue(
    issue_id: str,
    issue: IssueUpdateRequest,
    current_user: dict = Depends(require_member)
):
    return IssueService.update_issue(
        issue_id,
        issue.model_dump(exclude_unset=True),
        current_user
    )


@router.patch("/{issue_id}/status")
def update_issue_status(
    issue_id: str,
    status_update: IssueStatusUpdateRequest,
    current_user: dict = Depends(require_member)
):
    return IssueService.update_issue_status(
        issue_id,
        status_update.status.value,
        current_user
    )
