from datetime import datetime
from datetime import timezone
from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exception import (
    BadRequestException,
    ForbiddenException,
    NotFoundException
)
from app.schemas.response_schema import (
    IssueCreatedResponse,
    IssueUpdatedResponse,
    IssueDeletedResponse,
    IssueResponse,
    PaginatedResponse
)
from app.utils.audit import generate_audit_fields


ALLOWED_TRANSITIONS = {
    "BACKLOG": ["TODO"],
    "TODO": ["IN_PROGRESS"],
    "IN_PROGRESS": ["REVIEW", "TODO", "DONE"],
    "REVIEW": ["DONE", "IN_PROGRESS"],
    "DONE": []
}

ALLOWED_UPDATE_FIELDS = {"title", "description", "assignee_email", "issue_type", "priority", "story_points"}


class IssueService:
    @staticmethod
    def _format_issue(issue: dict) -> IssueResponse:
        if issue is None:
            return None

        return IssueResponse(
            id=str(issue.get("_id")),
            issue_key=issue.get("issue_key"),
            title=issue.get("title"),
            description=issue.get("description"),
            project_id=str(issue.get("project_id")),
            parent_id=str(issue.get("parent_id")) if issue.get("parent_id") else None,
            reporter=issue.get("reporter_email"),
            assignee=issue.get("assignee_email"),
            issue_type=issue.get("issue_type"),
            status=issue.get("status"),
            priority=issue.get("priority", "Medium"),
            story_points=issue.get("story_points", 0)
        )

    @staticmethod
    def _generate_issue_key(project_key: str, project_id: str) -> str:
        issue_count = IssueRepository.count_issues_by_project(
            project_id
        )

        return f"{project_key}-{issue_count + 1}"

    @staticmethod
    def _paginate(items: list, page: int, limit: int) -> PaginatedResponse:
        page = max(page, 1)
        limit = min(max(limit, 1), 100)
        total = len(items)
        start = (page - 1) * limit
        end = start + limit

        return PaginatedResponse(
            items=items[start:end],
            page=page,
            limit=limit,
            total=total,
            pages=(total + limit - 1) // limit
        )

    @staticmethod
    def _validate_project_access(project_id: str, current_user: dict):
        project = ProjectRepository.get_project_by_id(project_id)

        if project is None:
            raise NotFoundException("Project not found.")

        if current_user["role"] != "ADMIN" and not ProjectRepository.member_exists(
            project_id,
            current_user["email"]
        ):
            raise ForbiddenException(
                "Only project members or admins can perform this action."
            )

        return project

    @staticmethod
    def _validate_assignee(project_id: str, assignee_email: str):
        if not ProjectRepository.member_exists(project_id, assignee_email):
            raise BadRequestException(
                "Assignee must be a valid project member."
            )

        assignee_user = UserRepository.get_user_by_email(assignee_email)

        if assignee_user is None:
            raise BadRequestException(
                "Assignee user not found."
            )

    @staticmethod
    def _ensure_status_update_access(issue: dict, current_user: dict):
        if current_user["role"] == "ADMIN":
            return

        if issue.get("assignee_email") != current_user["email"]:
            raise ForbiddenException(
                "Only the assignee or admin can update issue status."
            )

    @staticmethod
    def _ensure_edit_access(issue: dict, current_user: dict):
        if current_user["role"] == "ADMIN":
            return

        if issue.get("assignee_email") == current_user["email"] or issue.get("reporter_email") == current_user["email"]:
            return

        raise ForbiddenException(
            "Only the reporter, assignee, or admin can edit this issue."
        )

    @staticmethod
    def create_issue(issue_request, current_user: dict) -> IssueCreatedResponse:
        project = ProjectRepository.get_project_by_id(
            issue_request.project_id
        )

        if project is None:
            raise NotFoundException("Project not found.")

        if current_user["role"] != "ADMIN" and not ProjectRepository.member_exists(
            issue_request.project_id,
            current_user["email"]
        ):
            raise ForbiddenException(
                "Only project members or admins can create an issue."
            )

        if issue_request.assignee_email:
            IssueService._validate_assignee(
                issue_request.project_id,
                issue_request.assignee_email
            )

        issue_key = IssueService._generate_issue_key(
            project["project_key"],
            issue_request.project_id
        )

        if issue_request.parent_id:
            parent_issue = IssueRepository.get_issue_by_id(issue_request.parent_id)
            if parent_issue is None:
                raise NotFoundException("Parent issue not found.")
            if parent_issue.get("project_id") != issue_request.project_id:
                raise BadRequestException("Parent issue must belong to the same project.")

        issue_document = {
            "title": issue_request.title,
            "description": issue_request.description,
            "project_id": issue_request.project_id,
            "parent_id": issue_request.parent_id,
            "reporter_email": current_user["email"],
            "assignee_email": issue_request.assignee_email,
            "issue_type": issue_request.issue_type.value,
            "status": issue_request.status.value,
            "priority": issue_request.priority.value,
            "story_points": issue_request.story_points,
            "issue_key": issue_key,
            **generate_audit_fields(current_user["email"])
        }

        result = IssueRepository.create_issue(issue_document)

        return IssueCreatedResponse(issue_id=str(result.inserted_id))

    @staticmethod
    def get_issue_by_id(issue_id: str, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        if current_user["role"] not in ("ADMIN", "VIEWER") and not ProjectRepository.member_exists(
            issue["project_id"],
            current_user["email"]
        ):
            raise ForbiddenException(
                "Only project members or admin can view this issue."
            )

        return IssueService._format_issue(issue)

    @staticmethod
    def get_issues_by_project(project_id: str, current_user: dict):
        IssueService._validate_project_access(project_id, current_user)

        return [
            IssueService._format_issue(issue)
            for issue in IssueRepository.get_issues_by_project(project_id)
        ]

    @staticmethod
    def get_assigned_issues(current_user: dict):
        return [
            IssueService._format_issue(issue)
            for issue in IssueRepository.get_issues_by_assignee(
                current_user["email"]
            )
        ]

    @staticmethod
    def get_all_issues(current_user: dict):
        if current_user["role"] in ("ADMIN", "VIEWER"):
            issues = IssueRepository.get_all_issues()
        else:
            projects = ProjectRepository.get_projects_by_member(
                current_user["email"]
            )
            project_ids = [
                project["_id"]
                for project in projects
            ]
            project_issues = IssueRepository.get_issues_by_project_ids(
                project_ids
            )
            assigned_issues = IssueRepository.get_issues_by_assignee(
                current_user["email"]
            )
            issue_map = {
                issue["_id"]: issue
                for issue in project_issues
            }
            for issue in assigned_issues:
                issue_map[issue["_id"]] = issue
            issues = list(issue_map.values())

        return [
            IssueService._format_issue(issue)
            for issue in issues
        ]

    @staticmethod
    def search_issues(
        current_user: dict,
        project_id: str | None = None,
        status: str | None = None,
        assignee_email: str | None = None,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
        paginated: bool = False
    ):
        if project_id:
            IssueService._validate_project_access(project_id, current_user)

        if current_user["role"] not in ("ADMIN", "VIEWER") and not project_id:
            projects = ProjectRepository.get_projects_by_member(
                current_user["email"]
            )
            allowed_project_ids = {
                project["_id"]
                for project in projects
            }

            issues = [
                issue
                for issue in IssueRepository.search_issues(
                    status=status,
                    assignee_email=assignee_email,
                    search=search
                )
                if issue["project_id"] in allowed_project_ids
                or issue.get("assignee_email") == current_user["email"]
            ]
        else:
            issues = IssueRepository.search_issues(
                project_id=project_id,
                status=status,
                assignee_email=assignee_email,
                search=search
            )

        formatted_issues = [
            IssueService._format_issue(issue)
            for issue in issues
        ]

        if paginated:
            return IssueService._paginate(
                formatted_issues,
                page,
                limit
            )

        return formatted_issues

    @staticmethod
    def get_subtasks(issue_id: str, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        IssueService._validate_project_access(issue["project_id"], current_user)

        return [
            IssueService._format_issue(subtask)
            for subtask in IssueRepository.get_issues_by_parent_id(issue_id)
        ]

    @staticmethod
    def update_issue(issue_id: str, updated_issue: dict, current_user: dict) -> IssueUpdatedResponse:
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        invalid_fields = set(updated_issue.keys()) - ALLOWED_UPDATE_FIELDS
        if invalid_fields:
            raise BadRequestException(f"Cannot update fields: {', '.join(invalid_fields)}")

        IssueService._ensure_edit_access(issue, current_user)

        if "assignee_email" in updated_issue and updated_issue["assignee_email"] is not None:
            IssueService._validate_assignee(
                issue["project_id"],
                updated_issue["assignee_email"]
            )

        updated_issue["updated_by"] = current_user["email"]
        updated_issue["updated_at"] = datetime.now(timezone.utc)

        IssueRepository.update_issue(
            issue_id,
            updated_issue
        )

        return IssueUpdatedResponse()

    @staticmethod
    def update_issue_status(issue_id: str, status: str, current_user: dict) -> IssueUpdatedResponse:
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        IssueService._ensure_status_update_access(issue, current_user)

        if status == issue["status"]:
            return IssueUpdatedResponse()

        allowed = ALLOWED_TRANSITIONS.get(issue["status"], [])

        if status not in allowed:
            raise BadRequestException(
                f"Cannot transition from {issue['status']} to {status}."
            )

        updated_document = {
            "status": status,
            "updated_by": current_user["email"],
            "updated_at": datetime.now(timezone.utc)
        }

        IssueRepository.update_issue(
            issue_id,
            updated_document
        )

        return IssueUpdatedResponse()

    @staticmethod
    def delete_issue(issue_id: str, current_user: dict) -> IssueDeletedResponse:
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        if current_user["role"] != "ADMIN" and issue.get("reporter_email") != current_user["email"]:
            raise ForbiddenException("Only the reporter or admin can delete this issue.")

        IssueRepository.delete_issue(issue_id)

        return IssueDeletedResponse()
