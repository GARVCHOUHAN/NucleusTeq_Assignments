from fastapi import APIRouter,HTTPException,status

from app.exceptions.custom_exception import UserAlreadyExistsException

from app.schemas.response_schema import SuccessResponse

from app.schemas.user_schema import UserRegisterRequest
from app.schemas.login_schema import LoginRequest
from app.services.auth_service import AuthService

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)

@router.post("/login")
def login_user(
    user: LoginRequest
):

    return AuthService.login_user(user)


@router.post(

    "/register",

    response_model=SuccessResponse,

    status_code=status.HTTP_201_CREATED

)

def register_user(

    user: UserRegisterRequest

):

    try:

        AuthService.register_user(

            user
        )

        return SuccessResponse(

            message="User registered successfully."

        )

    except UserAlreadyExistsException as exception:

        raise HTTPException(

            status_code=status.HTTP_409_CONFLICT,

            detail=str(exception)

        )