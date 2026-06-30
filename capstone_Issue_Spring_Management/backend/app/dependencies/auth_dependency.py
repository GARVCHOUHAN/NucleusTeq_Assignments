from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.core.roles import Roles

def get_current_user():

    """
    Temporary current user.

    Replace this with JWT decoding later.
    """

    return {

        "name": "Admin User",

        "email": "admin@test.com",

        "role": Roles.ADMIN

    }


def require_admin(

    current_user: dict = Depends(
        get_current_user
    )

):

    """
    Allow only ADMIN.
    """

    if current_user["role"] != Roles.ADMIN:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Admin access required."

        )

    return current_user


def require_member(

    current_user: dict = Depends(
        get_current_user
    )

):

    """
    Allow ADMIN and MEMBER.
    """

    if current_user["role"] not in [

        Roles.ADMIN,

        Roles.MEMBER

    ]:

        raise HTTPException(

            status_code=status.HTTP_403_FORBIDDEN,

            detail="Unauthorized."

        )

    return current_user