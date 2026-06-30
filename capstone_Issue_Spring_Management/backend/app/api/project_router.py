from fastapi import APIRouter
from fastapi import Depends
from fastapi import status

from app.dependencies.auth_dependency import (
    require_admin
)

from app.schemas.project_schema import (
    ProjectCreateRequest
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

    current_user=Depends(
        require_admin
    )

):

    return ProjectService.create_project(

        project,

        current_user

    )