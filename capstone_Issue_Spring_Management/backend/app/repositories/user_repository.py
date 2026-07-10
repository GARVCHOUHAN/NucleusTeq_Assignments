from datetime import datetime
from typing import Any
from bson import ObjectId
from app.database.collections import users_collection


def _serialize_value(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)

    if isinstance(value, datetime):
        return value.isoformat()

    if isinstance(value, list):
        return [
            _serialize_value(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            key: _serialize_value(item)
            for key, item in value.items()
            if key != "password"
        }

    return value


class UserRepository:
    @staticmethod
    def get_user_by_email(email: str):
        return users_collection.find_one({"email": email})

    @staticmethod
    def create_user(user_document: dict):
        users_collection.insert_one(user_document)

    @staticmethod
    def search_users(search: str | None = None, role: str | None = None):
        query = {}

        if role:
            query["role"] = role

        if search:
            query["$or"] = [
                {
                    "name": {
                        "$regex": search,
                        "$options": "i"
                    }
                },
                {
                    "email": {
                        "$regex": search,
                        "$options": "i"
                    }
                }
            ]

        return [
            _serialize_value(user)
            for user in users_collection.find(query)
        ]
