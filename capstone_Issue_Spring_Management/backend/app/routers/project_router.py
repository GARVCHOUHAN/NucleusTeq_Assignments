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