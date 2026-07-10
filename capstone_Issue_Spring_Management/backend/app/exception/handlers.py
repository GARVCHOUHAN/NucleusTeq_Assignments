from fastapi import FastAPI
from fastapi import Request
from fastapi import status
from fastapi.responses import JSONResponse

from app.exceptions.custom_exception import AlreadyExistsException
from app.exceptions.custom_exception import BadRequestException
from app.exceptions.custom_exception import ForbiddenException
from app.exceptions.custom_exception import NotFoundException
from app.exceptions.custom_exception import UnauthorizedException


def register_exception_handlers(application: FastAPI) -> None:
    """
    Register generic exception handlers.
    """

    @application.exception_handler(UnauthorizedException)
    async def unauthorized_handler(
        request: Request,
        exception: UnauthorizedException
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(NotFoundException)
    async def not_found_handler(
        request: Request,
        exception: NotFoundException
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(AlreadyExistsException)
    async def already_exists_handler(
        request: Request,
        exception: AlreadyExistsException
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(BadRequestException)
    async def bad_request_handler(
        request: Request,
        exception: BadRequestException
    ):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": exception.message
            }
        )

    @application.exception_handler(ForbiddenException)
    async def forbidden_handler(
        request: Request,
        exception: ForbiddenException
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                "detail": exception.message
            }
        )
