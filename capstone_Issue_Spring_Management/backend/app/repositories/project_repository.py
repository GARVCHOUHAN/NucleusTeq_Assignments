from bson import ObjectId

from app.database.collections import (projects_collection)


"""
Repository layer for Project collection.

This class contains only database operations.
No business logic should be written here.
"""

class ProjectRepository:
    """
    Repository class for Project CRUD operations.
    """

    @staticmethod
    def create_project(project_document: dict):
        """
        Insert a new project.
        """

        return projects_collection.insert_one(
            project_document
        )

    @staticmethod
    def get_project_by_name(project_name: str):
        """
        Fetch project by name.
        """

        return projects_collection.find_one(
            {
                "name": project_name,
                "is_deleted": False
            }
        )

    @staticmethod
    def get_project_by_key(project_key: str):
        """
        Fetch project by project key.
        """

        return projects_collection.find_one(
            {
                "project_key": project_key,
                "is_deleted": False
            }
        )

    @staticmethod
    def get_project_by_id(project_id: str):
        """
        Fetch project using project id.
        """

        return projects_collection.find_one(
            {
                "_id": ObjectId(project_id),
                "is_deleted": False
            }
        )

    @staticmethod
    def get_all_projects():
        """
        Fetch all active projects.
        """

        return list(
            projects_collection.find(
                {
                    "is_deleted": False
                }
            )
        )

    @staticmethod
    def get_projects_by_member(email: str):
        """
        Fetch projects assigned to a member.
        """

        return list(
            projects_collection.find(
                {
                    "members.email": email,
                    "is_deleted": False
                }
            )
        )

    @staticmethod
    def update_project(
        project_id: str,
        updated_document: dict
    ):
        """
        Update project details.
        """

        return projects_collection.update_one(
            {
                "_id": ObjectId(project_id),
                "is_deleted": False
            },
            {
                "$set": updated_document
            }
        )

    @staticmethod
    def soft_delete_project(project_id: str):
        """
        Soft delete a project.
        """

        return projects_collection.update_one(
            {
                "_id": ObjectId(project_id)
            },
            {
                "$set": {
                    "is_deleted": True
                }
            }
        )

    @staticmethod
    def add_member(
        project_id: str,
        member_document: dict
    ):
        """
        Add a member to project.
        """

        return projects_collection.update_one(
            {
                "_id": ObjectId(project_id)
            },
            {
                "$push": {
                    "members": member_document
                }
            }
        )

    @staticmethod
    def remove_member(
        project_id: str,
        email: str
    ):
        """
        Remove member from project.
        """

        return projects_collection.update_one(
            {
                "_id": ObjectId(project_id)
            },
            {
                "$pull": {
                    "members": {
                        "email": email
                    }
                }
            }
        )

    @staticmethod
    def member_exists(
        project_id: str,
        email: str
    ):
        """
        Check whether member already belongs
        to the project.
        """

        project = projects_collection.find_one(
            {
                "_id": ObjectId(project_id),
                "members.email": email,
                "is_deleted": False
            }
        )

        return project is not None

    @staticmethod
    def project_exists(project_id: str):
        """
        Check whether project exists.
        """

        project = projects_collection.find_one(
            {
                "_id": ObjectId(project_id),
                "is_deleted": False
            }
        )

        return project is not None