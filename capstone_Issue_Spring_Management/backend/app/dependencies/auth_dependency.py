from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from app.core.roles import Roles
from app.services.auth_service import AuthService


def get_current_user(
    user_email: str = Header(alias="X-User-Email")
):
    """
    Fetch current user from database.

    NOTE:
    This is a temporary solution.
    Later this dependency will read the
    email from JWT instead of request header.
    """

    current_user = AuthService.get_current_user(
        user_email
    )

    if current_user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )

    return current_user


def require_admin(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != Roles.ADMIN:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only ADMIN can perform this action."
        )

    return current_user


def require_member(
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] not in [
        Roles.ADMIN,
        Roles.MEMBER
    ]:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized."
        )

    return current_user