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

from app.utils.audit import generate_audit_fields


ALLOWED_TRANSITIONS = {
    "BACKLOG": ["TODO"],
    "TODO": ["IN_PROGRESS"],
    "IN_PROGRESS": ["REVIEW", "TODO", "DONE"],
    "REVIEW": ["DONE", "IN_PROGRESS"],
    "DONE": []
}


class IssueService:
    
    @staticmethod
    def _format_issue(issue: dict):
        if issue is None:
            return None

        formatted = issue.copy()
        formatted["id"] = formatted.get("_id")
        formatted["assignee"] = formatted.get("assignee_email")
        formatted["reporter"] = formatted.get("reporter_email")
        formatted["priority"] = formatted.get("priority", "Medium")
        formatted["story_points"] = formatted.get("story_points", 0)

        return formatted

    @staticmethod
    def _generate_issue_key(project_key: str, project_id: str) -> str:
        issue_count = IssueRepository.count_issues_by_project(
            project_id
        )

        return f"{project_key}-{issue_count + 1}"

    @staticmethod
    def _paginate(items: list, page: int, limit: int):
        page = max(page, 1)
        limit = min(max(limit, 1), 100)
        total = len(items)
        start = (page - 1) * limit
        end = start + limit

        return {
            "items": items[start:end],
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }

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
    def _ensure_issue_access(issue: dict, current_user: dict):
        if current_user["role"] == "ADMIN":
            return

        if issue.get("assignee_email") != current_user["email"]:
            raise ForbiddenException(
                "Only assigned users or admin can update this issue."
            )

    @staticmethod
    def create_issue(issue_request, current_user: dict):
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

        issue_document = {
            "title": issue_request.title,
            "description": issue_request.description,
            "project_id": issue_request.project_id,
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

        return {
            "message": "Issue created successfully.",
            "issue_id": str(result.inserted_id)
        }

    @staticmethod
    def get_issue_by_id(issue_id: str, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        if current_user["role"] != "ADMIN" and not ProjectRepository.member_exists(
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
        if current_user["role"] == "ADMIN":
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

        if current_user["role"] != "ADMIN" and not project_id:
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
    def update_issue(issue_id: str, updated_issue: dict, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        IssueService._ensure_issue_access(issue, current_user)

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

        return {
            "message": "Issue updated successfully."
        }

    @staticmethod
    def update_issue_status(issue_id: str, status: str, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        IssueService._ensure_issue_access(issue, current_user)

        if status == issue["status"]:
            return {
                "message": "Issue status unchanged."
            }

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

        return {
            "message": "Issue status updated successfully."
        }
