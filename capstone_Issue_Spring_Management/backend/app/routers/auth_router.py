from fastapi import APIRouter
from fastapi import HTTPException

from app.schemas.user_schema import UserCreate
from app.database.mongodb import users_collection
from app.core.security import hash_password

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register")
def register_user(user: UserCreate):

    existing_user = users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    user_document = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(
            user.password
        ),
        "role": user.role
    }

    users_collection.insert_one(
        user_document
    )

    return {
        "message": "User registered successfully"
    }