"""Domain exceptions and error codes for the application."""

from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes for API error responses."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    DUPLICATE_ERROR = "DUPLICATE_ERROR"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FEATURE_DISABLED = "FEATURE_DISABLED"
    WORKFLOW_ERROR = "WORKFLOW_ERROR"
    ENROLLMENT_ERROR = "ENROLLMENT_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    AWS_SERVICE_ERROR = "AWS_SERVICE_ERROR"


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        code: ErrorCode,
        message: str,
        status_code: int = 500,
        details: list[dict] | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


class ValidationError(AppException):
    def __init__(self, message: str, details: list[dict] | None = None):
        super().__init__(ErrorCode.VALIDATION_ERROR, message, 400, details)


class AuthenticationRequiredError(AppException):
    def __init__(self, message: str = "Authentication is required"):
        super().__init__(ErrorCode.AUTHENTICATION_REQUIRED, message, 401)


class AuthorizationError(AppException):
    def __init__(self, message: str = "You do not have permission to perform this action"):
        super().__init__(ErrorCode.AUTHORIZATION_ERROR, message, 403)


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(ErrorCode.NOT_FOUND, message, 404)


class DuplicateError(AppException):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(ErrorCode.DUPLICATE_ERROR, message, 409)


class FileTooLargeError(AppException):
    def __init__(self, message: str = "File exceeds maximum allowed size"):
        super().__init__(ErrorCode.FILE_TOO_LARGE, message, 413)


class InvalidFileTypeError(AppException):
    def __init__(self, message: str = "File type is not allowed"):
        super().__init__(ErrorCode.INVALID_FILE_TYPE, message, 415)


class FeatureDisabledError(AppException):
    def __init__(self, message: str = "This feature is currently disabled"):
        super().__init__(ErrorCode.FEATURE_DISABLED, message, 422)


class WorkflowError(AppException):
    def __init__(self, message: str = "Workflow configuration error"):
        super().__init__(ErrorCode.WORKFLOW_ERROR, message, 422)


class EnrollmentError(AppException):
    def __init__(self, message: str = "Biometric enrollment quality failure"):
        super().__init__(ErrorCode.ENROLLMENT_ERROR, message, 422)


class AWSServiceError(AppException):
    def __init__(self, message: str = "AWS service is unavailable"):
        super().__init__(ErrorCode.AWS_SERVICE_ERROR, message, 502)
