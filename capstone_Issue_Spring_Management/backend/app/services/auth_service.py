from app.core.security import hash_password

from app.exceptions.custom_exception import UserAlreadyExistsException

from app.repositories.user_repository import UserRepository

from app.schemas.user_schema import UserRegisterRequest


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