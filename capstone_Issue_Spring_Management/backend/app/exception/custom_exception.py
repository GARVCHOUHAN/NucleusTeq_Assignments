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