from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.exceptions.custom_exception import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    UserAlreadyExistsException,
    InvalidCredentialsException
)
from app.exceptions.custom_exception import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    MemberAlreadyExistsException,
    MemberNotFoundException
)

def register_exception_handlers(application: FastAPI) -> None:
    """
    Register all custom exception handlers.
    """

    @application.exception_handler(UserAlreadyExistsException)
    async def user_exists_exception_handler(
        request: Request,
        exception: UserAlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exception: InvalidCredentialsException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(
        ProjectAlreadyExistsException
    )
    async def project_exists_handler(
        request: Request,
        exception: ProjectAlreadyExistsException
    ):

        return JSONResponse(
            status_code=409,
            content={
                "detail": exception.message
            }
        )


    @application.exception_handler(
        ProjectNotFoundException
    )
    async def project_not_found_handler(
        request: Request,
        exception: ProjectNotFoundException
    ):

        return JSONResponse(
            status_code=404,
            content={
                "detail": exception.message
            }
        )
        
    @application.exception_handler(
        ProjectAlreadyExistsException
    )
    async def project_exists_handler(
        request: Request,
        exception: ProjectAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exception.message
            }
        )


    @application.exception_handler(
        ProjectNotFoundException
    )
    async def project_not_found_handler(
        request: Request,
        exception: ProjectNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exception.message
            }
        )


    @application.exception_handler(
        MemberAlreadyExistsException
    )
    async def member_exists_handler(
        request: Request,
        exception: MemberAlreadyExistsException
    ):

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exception.message
            }
        )


    @application.exception_handler(
        MemberNotFoundException
    )
    async def member_not_found_handler(
        request: Request,
        exception: MemberNotFoundException
    ):

        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exception.message
            }
        )    