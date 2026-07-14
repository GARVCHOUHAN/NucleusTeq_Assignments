from datetime import datetime
from datetime import timezone
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exception import (
    AlreadyExistsException,
    NotFoundException,
    ForbiddenException
)
from app.schemas.response_schema import (
    ProjectCreatedResponse,
    ProjectUpdatedResponse,
    ProjectDeletedResponse,
    MemberAddedResponse,
    MemberRemovedResponse
)
from app.utils.audit import generate_audit_fields


class ProjectService:
    @staticmethod
    def create_project(project, current_user: dict) -> ProjectCreatedResponse:
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can create projects.")
        existing_project = ProjectRepository.get_project_by_name(project.name)

        if existing_project:
            raise AlreadyExistsException("Project already exists.")
        
        existing_key = ProjectRepository.get_project_by_key(project.project_key)
        if existing_key:
            raise AlreadyExistsException("Project key already exists.")

        members = []
        member_emails = set()

        for member in project.members:
            if member.email in member_emails:
                raise AlreadyExistsException("Duplicate member email in project request.")
            member_emails.add(member.email)
            user = UserRepository.get_user_by_email(member.email)

            if user is None:
                raise NotFoundException(f"User not found: {member.email}")

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
            **generate_audit_fields(current_user["email"])
        }

        result = ProjectRepository.create_project(project_document)
        return ProjectCreatedResponse(project_id=str(result.inserted_id))
        

    @staticmethod
    def get_all_projects(current_user: dict):
        # the projects should only be the ones the admin created or the ones the user is a member of
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can view all projects.")
        return ProjectRepository.get_all_projects()

    @staticmethod
    def get_project_by_id(project_id: str, current_user: dict):
        # it should be restricted to admin and project members only
        if current_user["role"] != "ADMIN":
            project = ProjectRepository.get_project_by_id(project_id)

            if project is None:
                raise NotFoundException("Project not found.")

            if not any(
                member["email"] == current_user["email"]
                for member in project["members"]):
                raise ForbiddenException("You are not a member of this project.")
        project = ProjectRepository.get_project_by_id(project_id)

        return project

    @staticmethod
    def update_project(
        project_id: str,
        updated_project: dict,
        current_user: dict
    ) -> ProjectUpdatedResponse:
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can update projects.")
        project = ProjectRepository.get_project_by_id(project_id)

        if project is None:
            raise NotFoundException("Project not found.")

        if "name" in updated_project:
            existing_project = ProjectRepository.get_project_by_name(updated_project["name"])

            if (
                existing_project
                and str(existing_project["_id"]) != project_id
            ):
                raise AlreadyExistsException("Project already exists.")

        if "project_key" in updated_project:
            existing_key = ProjectRepository.get_project_by_key(
                updated_project["project_key"]
            )

            if (
                existing_key
                and str(existing_key["_id"]) != project_id
            ):
                raise AlreadyExistsException("Project key already exists.")

        updated_project["updated_by"] = current_user["email"]

        updated_project["updated_at"] = datetime.now(timezone.utc)

        ProjectRepository.update_project(project_id, updated_project)

        return ProjectUpdatedResponse()

        

    @staticmethod
    def delete_project(project_id: str, current_user: dict) -> ProjectDeletedResponse:
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can delete projects.")

        project = ProjectRepository.get_project_by_id(project_id)

        if project is None:
            raise NotFoundException("Project not found.")

        ProjectRepository.soft_delete_project(project_id)
        return ProjectDeletedResponse()
        

    @staticmethod
    def add_member(
        project_id: str,
        member_email: str,
        current_user: dict
    ) -> MemberAddedResponse:
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can manage project members.")

        project = ProjectRepository.get_project_by_id(project_id)

        if project is None:
            raise NotFoundException("Project not found.")

        if ProjectRepository.member_exists(
            project_id,
            member_email
        ):
            raise AlreadyExistsException("Member already assigned.")

        user = UserRepository.get_user_by_email(member_email)

        if user is None:
            raise NotFoundException("User not found.")

        ProjectRepository.add_member(
            project_id,
            {
                "email": user["email"],
                "name": user["name"],
                "role": user["role"]
            }
        )

        return MemberAddedResponse()


    @staticmethod
    def remove_member(
        project_id: str,
        email: str,
        current_user: dict
    ) -> MemberRemovedResponse:
        if current_user["role"] != "ADMIN":
            raise ForbiddenException("Only admins can manage project members.")
 
        if not ProjectRepository.member_exists(
            project_id,
            email
        ):
            raise NotFoundException("Member not assigned.")

        ProjectRepository.remove_member(
            project_id,
            email
        )

        return MemberRemovedResponse()


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
