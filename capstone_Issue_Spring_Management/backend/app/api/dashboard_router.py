from fastapi import APIRouter
from fastapi import Depends

from app.dependencies.auth_dependency import require_member
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/dashboard",tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(current_user: dict = Depends(require_member)):
    return DashboardService.get_stats(current_user)
