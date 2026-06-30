from capstone_Issue_Spring_Management.backend.app.services.project_service import ProjectService
from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth_dependency import require_admin

router = APIRouter(prefix="/projects",tags=["Projects"])


@router.post("/")

def create_project(

    current_user = Depends(
        require_admin
    )

):

    return {

        "message": "Project created successfully.",

        "created_by": current_user["name"]

    }

@router.get("")
def get_all_projects():

    return ProjectService.get_all_projects()


@router.get("/{project_id}")
def get_project_by_id(
    project_id: str
):

    return ProjectService.get_project_by_id(
        project_id
    )