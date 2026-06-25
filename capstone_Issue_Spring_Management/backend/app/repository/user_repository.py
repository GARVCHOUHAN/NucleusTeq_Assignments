from app.database.collections import users_collection


class UserRepository:

    @staticmethod
    def get_user_by_email(email: str):

        return users_collection.find_one({"email": email})


    @staticmethod
    def create_user(user_document: dict):

        users_collection.insert_one(user_document)