from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from fastapi import status

from app.dependencies.auth_dependency import require_member
from app.schemas.sprint_schema import SprintCreateRequest
from app.schemas.sprint_schema import SprintIssueRequest
from app.services.sprint_service import SprintService


router = APIRouter(
    prefix="/sprints",
    tags=["Sprints"]
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_sprint(
    sprint: SprintCreateRequest,
    current_user: dict = Depends(require_member)
) -> dict:
    result = SprintService.create_sprint(sprint, current_user)
    return {
        **result.model_dump(),
        "message": "Sprint created successfully."
    }


@router.get("")
def get_sprints(
    project_id: str | None = Query(default=None),
    current_user: dict = Depends(require_member)
) -> list:
    return SprintService.get_sprints(current_user, project_id)


@router.get("/{sprint_id}")
def get_sprint_by_id(
    sprint_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    return SprintService.get_sprint_by_id(sprint_id, current_user)


@router.post("/{sprint_id}/issues")
def add_issue_to_sprint(
    sprint: SprintIssueRequest,
    sprint_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = SprintService.add_issue(sprint_id, sprint.issue_id, current_user)
    return {
        **result.model_dump(),
        "message": "Issue added to sprint successfully."
    }


@router.delete("/{sprint_id}/issues/{issue_id}")
def remove_issue_from_sprint(
    sprint_id: str = Path(...),
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = SprintService.remove_issue(sprint_id, issue_id, current_user)
    return {
        **result.model_dump(),
        "message": "Issue removed from sprint successfully."
    }


@router.patch("/{sprint_id}/start")
def start_sprint(
    sprint_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = SprintService.start_sprint(sprint_id, current_user)
    return {
        **result.model_dump(),
        "message": "Sprint started successfully."
    }


@router.patch("/{sprint_id}/complete")
def complete_sprint(
    sprint_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = SprintService.complete_sprint(sprint_id, current_user)
    return {
        **result.model_dump(),
        "message": "Sprint completed successfully."
    }
