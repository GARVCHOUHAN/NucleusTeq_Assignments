from app.repositories.project_repository import (
    ProjectRepository
)


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

            "created_by": current_user["email"]

        }

        ProjectRepository.create_project(
            project_document
        )

        return {

            "message": "Project created successfully."

        }