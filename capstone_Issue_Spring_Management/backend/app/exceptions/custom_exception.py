from capstone_Issue_Spring_Management.backend.app.services.project_service import ProjectService


class UserAlreadyExistsException(Exception):
    """Raised when a user already exists."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidCredentialsException(Exception):
    """Raised when login credentials are invalid."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        
        
class ProjectAlreadyExistsException(Exception):

    def __init__(self, message: str):

        self.message = message

        super().__init__(message)


class ProjectNotFoundException(Exception):

    def __init__(self, message: str):

        self.message = message

        super().__init__(message)
        
"""
Project Exceptions
"""


class ProjectAlreadyExistsException(Exception):
    """
    Raised when project name or key already exists.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ProjectNotFoundException(Exception):
    """
    Raised when project is not found.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class MemberAlreadyExistsException(Exception):
    """
    Raised when member already belongs to project.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class MemberNotFoundException(Exception):
    """
    Raised when member is not assigned.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)