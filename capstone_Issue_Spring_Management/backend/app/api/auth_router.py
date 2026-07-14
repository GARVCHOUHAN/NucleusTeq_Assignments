from fastapi import APIRouter
from fastapi import Depends
from fastapi import Query
from fastapi import status

from app.dependencies.auth_dependency import require_member
from app.schemas.login_schema import LoginRequest
from app.schemas.response_schema import SuccessResponse
from app.schemas.user_schema import UserRegisterRequest
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login_user(user: LoginRequest):
    return AuthService.login_user(user)


@router.post("/register",response_model=SuccessResponse,status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegisterRequest):
    AuthService.register_user(user)
    return SuccessResponse(message="User registered successfully.")


@router.get("/users")
def search_users(
    search: str | None = Query(default=None),
    current_user: dict = Depends(require_member)
):
    return AuthService.search_users(search)