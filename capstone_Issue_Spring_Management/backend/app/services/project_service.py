"""
Business logic for Project Module.
"""

from datetime import datetime

from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository

from app.exceptions.custom_exception import (
    ProjectAlreadyExistsException,
    ProjectNotFoundException,
    MemberAlreadyExistsException,
    MemberNotFoundException
)

from app.utils.audit import generate_audit_fields


class ProjectService:
    """
    Project business logic.
    """

    @staticmethod
    def create_project(
        project,
        current_user
    ):
        """
        Create a new project.
        """

        existing_project = ProjectRepository.get_project_by_name(
            project.name
        )

        if existing_project:

            raise ProjectAlreadyExistsException(
                "Project already exists."
            )

        existing_key = ProjectRepository.get_project_by_key(
            project.project_key
        )

        if existing_key:

            raise ProjectAlreadyExistsException(
                "Project key already exists."
            )

        members = []

        for member in project.members:

            user = UserRepository.get_user_by_email(
                member.email
            )

            if user is None:
                continue

            members.append(
                {
                    "email": user["email"],
                    "name": user["name"],
                    "role": user["role"]
                }
            )

        project_document = {

            "name": project.name,

            "description": project.description,

            "project_key": project.project_key,

            "members": members,

            **generate_audit_fields(
                current_user["email"]
            )
        }

        ProjectRepository.create_project(
            project_document
        )

        return {

            "message": "Project created successfully."

        }

    @staticmethod
    def get_all_projects():
        """
        Return all active projects.
        """

        return ProjectRepository.get_all_projects()

    @staticmethod
    def get_project_by_id(
        project_id: str
    ):
        """
        Fetch project using id.
        """

        project = ProjectRepository.get_project_by_id(
            project_id
        )

        if project is None:

            raise ProjectNotFoundException(
                "Project not found."
            )

        return project

    @staticmethod
    def update_project(
        project_id: str,
        updated_project: dict,
        current_user: dict
    ):
        """
        Update project.
        """

        project = ProjectRepository.get_project_by_id(
            project_id
        )

        if project is None:

            raise ProjectNotFoundException(
                "Project not found."
            )

        updated_project["updated_by"] = current_user["email"]

        updated_project["updated_at"] = datetime.utcnow()

        ProjectRepository.update_project(
            project_id,
            updated_project
        )

        return {

            "message": "Project updated successfully."

        }

    @staticmethod
    def delete_project(
        project_id: str
    ):
        """
        Soft delete project.
        """

        project = ProjectRepository.get_project_by_id(
            project_id
        )

        if project is None:

            raise ProjectNotFoundException(
                "Project not found."
            )

        ProjectRepository.soft_delete_project(
            project_id
        )

        return {

            "message": "Project deleted successfully."

        }

    @staticmethod
    def add_member(
        project_id: str,
        member_email: str
    ):
        """
        Add member to project.
        """

        project = ProjectRepository.get_project_by_id(
            project_id
        )

        if project is None:

            raise ProjectNotFoundException(
                "Project not found."
            )

        if ProjectRepository.member_exists(
            project_id,
            member_email
        ):

            raise MemberAlreadyExistsException(
                "Member already assigned."
            )

        user = UserRepository.get_user_by_email(
            member_email
        )

        if user is None:

            raise MemberNotFoundException(
                "User not found."
            )

        ProjectRepository.add_member(

            project_id,

            {

                "email": user["email"],

                "name": user["name"],

                "role": user["role"]

            }

        )

        return {

            "message": "Member added successfully."

        }

    @staticmethod
    def remove_member(
        project_id: str,
        email: str
    ):
        """
        Remove member from project.
        """

        if not ProjectRepository.member_exists(
            project_id,
            email
        ):

            raise MemberNotFoundException(
                "Member not assigned."
            )

        ProjectRepository.remove_member(
            project_id,
            email
        )

        return {

            "message": "Member removed successfully."

        }

    @staticmethod
    def get_assigned_projects(
        current_user
    ):
        """
        Fetch assigned projects.
        """

        return ProjectRepository.get_projects_by_member(
            current_user["email"]
        )