"""
Project API routes.
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status

from app.dependencies.auth_dependency import (
    require_admin,
    require_member
)

from app.schemas.project_schema import (
    ProjectCreateRequest
)

from app.schemas.project_update_schema import (
    ProjectUpdateRequest
)

from app.schemas.member_schema import (
    ProjectMemberRequest
)

from app.services.project_service import (
    ProjectService
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED
)
def create_project(
    project: ProjectCreateRequest,
    current_user: dict = Depends(require_admin)
):
    """
    Create a new project.
    """

    return ProjectService.create_project(
        project,
        current_user
    )


@router.get("")
def get_all_projects(
    current_user: dict = Depends(require_member)
):
    """
    Fetch all active projects.
    """

    return ProjectService.get_all_projects()


@router.get("/{project_id}")
def get_project_by_id(
    project_id: str = Path(...),
    current_user: dict = Depends(require_member)
):
    """
    Fetch project using id.
    """

    return ProjectService.get_project_by_id(
        project_id
    )


@router.put("/{project_id}")
def update_project(
    project_id: str,
    updated_project: ProjectUpdateRequest,
    current_user: dict = Depends(require_admin)
):
    """
    Update project.
    """

    return ProjectService.update_project(
        project_id,
        updated_project.model_dump(
            exclude_unset=True
        ),
        current_user
    )


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    current_user: dict = Depends(require_admin)
):
    """
    Soft delete project.
    """

    return ProjectService.delete_project(
        project_id
    )


@router.post("/{project_id}/members")
def add_member(
    project_id: str,
    member: ProjectMemberRequest,
    current_user: dict = Depends(require_admin)
):
    """
    Add member to project.
    """

    return ProjectService.add_member(
        project_id,
        member.email
    )


@router.delete("/{project_id}/members/{email}")
def remove_member(
    project_id: str,
    email: str,
    current_user: dict = Depends(require_admin)
):
    """
    Remove member from project.
    """

    return ProjectService.remove_member(
        project_id,
        email
    )


@router.get("/assigned/me")
def get_assigned_projects(
    current_user: dict = Depends(require_member)
):
    """
    Fetch projects assigned to current user.
    """

    return ProjectService.get_assigned_projects(
        current_user
    )