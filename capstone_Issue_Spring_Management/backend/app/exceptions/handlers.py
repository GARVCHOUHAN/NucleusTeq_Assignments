from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.exceptions.custom_exception import (
    UserAlreadyExistsException,
    InvalidCredentialsException
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