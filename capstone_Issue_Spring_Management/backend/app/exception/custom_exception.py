class AppException(Exception):
    """Base exception for API layer errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource is not found."""


class AlreadyExistsException(AppException):
    """Raised when a resource already exists."""


class BadRequestException(AppException):
    """Raised when request data is invalid."""


class ForbiddenException(AppException):
    """Raised when a user is not authorized to perform an action."""


class UnauthorizedException(AppException):
    """Raised when authentication or credentials are invalid."""


class UserAlreadyExistsException(AlreadyExistsException):
    """Backward-compatible alias for duplicate-user errors."""


class InvalidCredentialsException(UnauthorizedException):
    """Backward-compatible alias for invalid login credentials."""


class ProjectAlreadyExistsException(AlreadyExistsException):
    """Backward-compatible alias for duplicate-project errors."""


class ProjectNotFoundException(NotFoundException):
    """Backward-compatible alias for missing-project errors."""


class MemberAlreadyExistsException(AlreadyExistsException):
    """Backward-compatible alias for duplicate-member errors."""


class MemberNotFoundException(NotFoundException):
    """Backward-compatible alias for missing-member errors."""


class IssueNotFoundException(NotFoundException):
    """Backward-compatible alias for missing-issue errors."""


class InvalidAssigneeException(BadRequestException):
    """Backward-compatible alias for invalid-assignee errors."""


class InvalidStatusTransitionException(BadRequestException):
    """Backward-compatible alias for invalid-status-transition errors."""


class UnauthorizedActionException(ForbiddenException):
    """Backward-compatible alias for forbidden actions."""


class RecordNotFoundException(NotFoundException):
    """Backward-compatible alias for missing records."""
