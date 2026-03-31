class DomainException(Exception):
    """Base class for all domain exceptions."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class EntityNotFoundException(DomainException):
    """Exception raised when an entity is not found."""
    def __init__(self, entity_name: str, identifier: str):
        self.entity_name = entity_name
        self.identifier = identifier
        super().__init__(f"{entity_name} with identifier {identifier} not found.")


class UnauthorizedException(DomainException):
    """Exception raised when an action is unauthorized."""
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message)


class ForbiddenException(DomainException):
    """Exception raised when access to a resource is forbidden."""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message)


class ValidationException(DomainException):
    """Exception raised when domain validation fails."""
    def __init__(self, message: str):
        super().__init__(message)
