from app.repositories.project_repository import (
    ProjectRepository
)
from app.utils.audit import generate_audit_fields


class ProjectService:

    @staticmethod
    def create_project(

        project,

        current_user

    ):

        existing_project = ProjectRepository.get_project_by_name(
            project.name
        )

        if existing_project:

            raise Exception(
                "Project already exists."
            )

        project_document = {

            "name": project.name,

            "description": project.description,

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

            return ProjectRepository.get_all_projects()


        @staticmethod
        def get_project_by_id(
            project_id: str
        ):

            project = ProjectRepository.get_project_by_id(
                project_id
            )

            if project is None:

                raise Exception(
                    "Project not found."
                )

            return project