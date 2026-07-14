from datetime import datetime
from datetime import timezone

from app.exceptions.custom_exception import AlreadyExistsException
from app.exceptions.custom_exception import BadRequestException
from app.exceptions.custom_exception import ForbiddenException
from app.exceptions.custom_exception import NotFoundException
from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.sprint_repository import SprintRepository
from app.schemas.response_schema import (
    SprintCreatedResponse,
    SprintStartedResponse,
    SprintCompletedResponse,
    IssueAddedToSprintResponse,
    IssueRemovedFromSprintResponse
)
from app.utils.audit import generate_audit_fields
from app.constants import (COMPLETED,PROJECT_ID,STATUS,DONE)


class SprintService:
    @staticmethod
    def _ensure_project_access(project_id: str, current_user: dict):
        project = ProjectRepository.get_project_by_id(project_id)

        if project is None:
            raise NotFoundException("Project not found.")

        if current_user["role"] != "ADMIN" and not ProjectRepository.member_exists(
            project_id,
            current_user["email"]
        ):
            raise ForbiddenException(
                "Only project members or admins can access this sprint."
            )

        return project

    @staticmethod
    def _ensure_admin_or_member(project_id: str, current_user: dict):
        return SprintService._ensure_project_access(project_id, current_user)

    @staticmethod
    def create_sprint(sprint_request, current_user: dict) -> SprintCreatedResponse:
        SprintService._ensure_admin_or_member(
            sprint_request.project_id,
            current_user
        )

        sprint_document = {
            "name": sprint_request.name,
            "project_id": sprint_request.project_id,
            "start_date": sprint_request.start_date.isoformat(),
            "end_date": sprint_request.end_date.isoformat(),
            "status": sprint_request.status.value,
            "issue_ids": [],
            **generate_audit_fields(current_user["email"])
        }

        result = SprintRepository.create_sprint(sprint_document)

        return SprintCreatedResponse(sprint_id=str(result.inserted_id))

    @staticmethod
    def get_sprints(current_user: dict, project_id: str | None = None):
        if project_id:
            SprintService._ensure_project_access(project_id, current_user)
            return SprintRepository.get_sprints_by_project(project_id)

        if current_user["role"] == "ADMIN":
            return SprintRepository.get_all_sprints()

        projects = ProjectRepository.get_projects_by_member(current_user["email"])
        sprints = []

        for project in projects:
            sprints.extend(
                SprintRepository.get_sprints_by_project(project["_id"])
            )

        return sprints

    @staticmethod
    def get_sprint_by_id(sprint_id: str, current_user: dict):
        sprint = SprintRepository.get_sprint_by_id(sprint_id)

        if sprint is None:
            raise NotFoundException("Sprint not found.")

        SprintService._ensure_project_access(
            sprint["project_id"],
            current_user
        )

        return sprint

    @staticmethod
    def add_issue(sprint_id: str, issue_id: str, current_user: dict) -> IssueAddedToSprintResponse:
        sprint = SprintService.get_sprint_by_id(sprint_id, current_user)

        if sprint[STATUS] == COMPLETED:
            raise BadRequestException("Cannot add issues to a completed sprint.")

        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        if issue[PROJECT_ID] != sprint["project_id"]:
            raise BadRequestException("Issue must belong to the sprint project.")

        if issue["status"] == DONE:
            raise BadRequestException("Completed issues cannot be added to sprint.")

        if SprintRepository.issue_in_sprint(sprint_id, issue_id):
            raise AlreadyExistsException("Issue already exists in sprint.")

        SprintRepository.add_issue(sprint_id, issue_id)

        return IssueAddedToSprintResponse()

    @staticmethod
    def remove_issue(sprint_id: str, issue_id: str, current_user: dict) -> IssueRemovedFromSprintResponse:
        SprintService.get_sprint_by_id(sprint_id, current_user)

        if not SprintRepository.issue_in_sprint(sprint_id, issue_id):
            raise NotFoundException("Issue not found in sprint.")

        SprintRepository.remove_issue(sprint_id, issue_id)

        return IssueRemovedFromSprintResponse()

    @staticmethod
    def start_sprint(sprint_id: str, current_user: dict) -> SprintStartedResponse:
        sprint = SprintService.get_sprint_by_id(sprint_id, current_user)

        if sprint["status"] != "planned":
            raise BadRequestException("Only planned sprints can be started.")

        SprintRepository.update_sprint(
            sprint_id,
            {
                "status": "active",
                "updated_by": current_user["email"],
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return SprintStartedResponse()

    @staticmethod
    def complete_sprint(sprint_id: str, current_user: dict) -> SprintCompletedResponse:
        sprint = SprintService.get_sprint_by_id(sprint_id, current_user)

        if sprint["status"] != "active":
            raise BadRequestException("Only active sprints can be completed.")

        SprintRepository.update_sprint(
            sprint_id,
            {
                "status": "completed",
                "updated_by": current_user["email"],
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return SprintCompletedResponse()
