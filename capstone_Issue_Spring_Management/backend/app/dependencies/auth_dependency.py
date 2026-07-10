from jose import JWTError

from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from app.core.roles import Roles
from app.core.security import decode_access_token
from app.services.auth_service import AuthService


def _extract_bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None

    scheme, _, token = authorization.partition(" ")

    if scheme.lower() != "bearer" or not token:
        return None

    return token.strip()


def get_current_user(
    authorization: str | None = Header(default=None),
    user_email: str | None = Header(default=None, alias="X-User-Email")
):
    """
    Fetch current user from JWT bearer token.

    X-User-Email remains supported for existing tests and local manual calls.
    """

    token = _extract_bearer_token(authorization)
    email = user_email

    if token:
        try:
            payload = decode_access_token(token)
            email = payload.get("email")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token."
            )

    current_user = AuthService.get_current_user(email)

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
