from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status

from app.dependencies.auth_dependency import (require_admin,require_member)
from app.schemas.project_schema import ProjectCreateRequest
from app.schemas.project_update_schema import ProjectUpdateRequest
from app.schemas.member_schema import ProjectMemberRequest
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects",tags=["Projects"])


@router.post("",status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreateRequest,current_user: dict = Depends(require_admin)):
    ProjectService.create_project(project,current_user)
    return {"message": "Project created successfully."}


@router.get("", status_code=status.HTTP_200_OK)
def get_all_projects(current_user: dict = Depends(require_member)):
    return ProjectService.get_all_projects(current_user)


@router.get("/{project_id}")
def get_project_by_id(project_id: str = Path(...),current_user: dict = Depends(require_member)):
    return ProjectService.get_project_by_id(project_id,current_user)


@router.put("/{project_id}")
def update_project(
    project_id: str,
    updated_project: ProjectUpdateRequest,
    current_user: dict = Depends(require_admin)
):
    ProjectService.update_project(
        project_id,
        updated_project.model_dump(
            exclude_unset=True
        ),
        current_user
    )
    return {"message": "Project updated successfully."}


@router.delete("/{project_id}")
def delete_project(
    project_id: str,
    current_user: dict = Depends(require_admin)
):
    ProjectService.delete_project(project_id,current_user)
    return {"message": "Project deleted successfully."}


@router.post("/{project_id}/members")
def add_member(
    project_id: str,
    member: ProjectMemberRequest,
    current_user: dict = Depends(require_admin)
):
    
    ProjectService.add_member(
        project_id,
        member.email,
        current_user
    )
    return {"message": "Member added successfully."}


@router.delete("/{project_id}/members/{email}")
def remove_member(
    project_id: str,
    email: str,
    current_user: dict = Depends(require_admin)
):
    """
    Remove member from project.
    """
    ProjectService.remove_member(project_id,email,current_user)
    return {"message": "Member removed successfully."}

@router.get("/assigned/me")
def get_assigned_projects(current_user: dict = Depends(require_member)):
    return ProjectService.get_assigned_projects(current_user)