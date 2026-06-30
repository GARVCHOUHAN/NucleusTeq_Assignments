from bson import ObjectId

from app.database.collections import (projects_collection)


class ProjectRepository:

    @staticmethod
    def create_project(
        project_document: dict
    ):

        return projects_collection.insert_one(
            project_document
        )


    @staticmethod
    def get_project_by_name(
        project_name: str
    ):

        return projects_collection.find_one(

            {

                "name": project_name,

                "is_deleted": False

            }

        )


    @staticmethod
    def get_all_projects():

        return list(

            projects_collection.find(

                {

                    "is_deleted": False

                }

            )

        )


    @staticmethod
    def get_project_by_id(
        project_id: str
    ):

        return projects_collection.find_one(

            {

                "_id": ObjectId(project_id),

                "is_deleted": False

            }

        )