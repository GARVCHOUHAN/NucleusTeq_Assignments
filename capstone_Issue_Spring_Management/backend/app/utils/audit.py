"""
Utility functions for audit fields.
"""

from datetime import datetime
from typing import Dict


def generate_audit_fields(current_user_email: str) -> Dict:
    """
    Generate common audit fields for
    MongoDB documents.
    """

    current_time = datetime.utcnow()

    return {

        "created_by": current_user_email,

        "updated_by": current_user_email,

        "created_at": current_time,

        "updated_at": current_time,

        "is_deleted": False

    }