from datetime import datetime
from datetime import timezone
from app.exceptions.custom_exception import ForbiddenException
from app.exceptions.custom_exception import NotFoundException
from app.repositories.comment_repository import CommentRepository
from app.repositories.issue_repository import IssueRepository
from app.repositories.project_repository import ProjectRepository
from app.utils.audit import generate_audit_fields


class CommentService:
    @staticmethod
    def _ensure_issue_access(issue_id: str, current_user: dict):
        issue = IssueRepository.get_issue_by_id(issue_id)

        if issue is None:
            raise NotFoundException("Issue not found.")

        if current_user["role"] != "ADMIN" and not ProjectRepository.member_exists(
            issue["project_id"],
            current_user["email"]
        ):
            raise ForbiddenException("Only project members or admins can access comments.")

        return issue

    @staticmethod
    def create_comment(issue_id: str, comment_request, current_user: dict):
        CommentService._ensure_issue_access(issue_id, current_user)

        comment_document = {
            "issue_id": issue_id,
            "body": comment_request.body,
            "author_email": current_user["email"],
            **generate_audit_fields(current_user["email"])
        }
        result = CommentRepository.create_comment(comment_document)

        return {
            "message": "Comment added successfully.",
            "comment_id": str(result.inserted_id)
        }

    @staticmethod
    def get_issue_comments(issue_id: str, current_user: dict):
        CommentService._ensure_issue_access(issue_id, current_user)

        return CommentRepository.get_comments_by_issue(issue_id)


    @staticmethod
    def update_comment(comment_id: str, comment_request, current_user: dict):
        comment = CommentRepository.get_comment_by_id(comment_id)

        if comment is None:
            raise NotFoundException("Comment not found.")

        CommentService._ensure_issue_access(comment["issue_id"],current_user)

        if current_user["role"] != "ADMIN" and comment["author_email"] != current_user["email"]:
            raise ForbiddenException("Only comment author can edit comment.")

        CommentRepository.update_comment(
            comment_id,
            {
                "body": comment_request.body,
                "updated_by": current_user["email"],
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return {
            "message": "Comment updated successfully."
        }

    @staticmethod
    def delete_comment(comment_id: str, current_user: dict):
        comment = CommentRepository.get_comment_by_id(comment_id)

        if comment is None:
            raise NotFoundException("Comment not found.")

        CommentService._ensure_issue_access(
            comment["issue_id"],
            current_user
        )

        if current_user["role"] != "ADMIN" and comment["author_email"] != current_user["email"]:
            raise ForbiddenException("Only comment author can delete comment.")

        CommentRepository.soft_delete_comment(
            comment_id,
            {
                "is_deleted": True,
                "updated_by": current_user["email"],
                "updated_at": datetime.now(timezone.utc)
            }
        )

        return {
            "message": "Comment deleted successfully."
        }
