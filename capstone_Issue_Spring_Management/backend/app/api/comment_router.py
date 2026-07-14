from fastapi import APIRouter
from fastapi import Depends
from fastapi import Path
from fastapi import status
from app.dependencies.auth_dependency import require_member
from app.schemas.comment_schema import CommentCreateRequest
from app.schemas.comment_schema import CommentUpdateRequest
from app.services.comment_service import CommentService


router = APIRouter(
    tags=["Comments"]
)


@router.post("/issues/{issue_id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    comment: CommentCreateRequest,
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = CommentService.create_comment(issue_id, comment, current_user)
    return {
        **result.model_dump(),
        "message": "Comment added successfully."
    }


@router.get("/issues/{issue_id}/comments")
def get_issue_comments(
    issue_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> list:
    return CommentService.get_issue_comments(issue_id, current_user)


@router.put("/comments/{comment_id}")
def update_comment(
    comment: CommentUpdateRequest,
    comment_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = CommentService.update_comment(comment_id, comment, current_user)
    return {
        **result.model_dump(),
        "message": "Comment updated successfully."
    }


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: str = Path(...),
    current_user: dict = Depends(require_member)
) -> dict:
    result = CommentService.delete_comment(comment_id, current_user)
    return {
        **result.model_dump(),
        "message": "Comment deleted successfully."
    }
