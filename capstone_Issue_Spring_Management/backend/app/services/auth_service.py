from app.core.security import create_access_token
from app.core.security import hash_password
from app.core.security import verify_password
from app.exceptions.custom_exception import AlreadyExistsException
from app.exceptions.custom_exception import UnauthorizedException
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (UserRegisterRequest , UserResponse , LoginResponse)


class AuthService:
    @staticmethod
    def register_user(user: UserRegisterRequest):
        existing_user = UserRepository.get_user_by_email(user.email)

        if existing_user:
            raise AlreadyExistsException("Email already registered.")

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
            raise UnauthorizedException("Invalid email or password.")

        is_password_valid = verify_password(
            user.password,
            existing_user["password"]
        )

        if not is_password_valid:
            raise UnauthorizedException("Invalid email or password.")

        user_response = UserResponse(
            name=existing_user["name"],
            email=existing_user["email"],
            role=existing_user["role"]
        )

        access_token = create_access_token(
            {
                "sub": str(existing_user["_id"]),
                "email": existing_user["email"],
                "role": existing_user["role"]
            }
        )

        return LoginResponse(
            message="Login successful.",
            access_token=access_token,
            token_type="bearer",
            user=user_response
        )

    @staticmethod
    def get_current_user(email: str):
        if not email:
            return None

        return UserRepository.get_user_by_email(email)

    @staticmethod
    def search_users(search: str | None = None):
        return UserRepository.search_users(
            search=search,
            role="MEMBER"
        )
