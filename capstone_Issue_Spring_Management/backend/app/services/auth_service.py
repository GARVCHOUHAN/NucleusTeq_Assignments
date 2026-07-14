from app.core.security import hash_password

from app.exceptions.custom_exception import UserAlreadyExistsException

from app.repositories.user_repository import UserRepository

from app.schemas.user_schema import UserRegisterRequest
from app.core.security import verify_password

from app.exceptions.custom_exception import (
    InvalidCredentialsException
)

class AuthService:

    @staticmethod
    def register_user(user: UserRegisterRequest):

        existing_user = UserRepository.get_user_by_email(user.email)

        if existing_user:

            raise UserAlreadyExistsException("Email already registered.")

        user_document = {

            "name": user.name,

            "email": user.email,

            "password": hash_password(user.password),

            "role": user.role.value

        }

        UserRepository.create_user(user_document)
        
    @staticmethod   
    def login_user(user):

        existing_user = UserRepository.get_user_by_email(user.email)

        if existing_user is None:

            raise InvalidCredentialsException("Invalid email or password.")

        is_password_valid = verify_password(
            user.password,
            existing_user["password"]
        )

        if not is_password_valid:

            raise InvalidCredentialsException("Invalid email or password.")

        return {

            "message": "Login successful.",

            "user": {

                "name": existing_user["name"],

                "email": existing_user["email"],

                "role": existing_user["role"]

            }

    }
        
        