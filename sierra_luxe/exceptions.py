"""
Custom exceptions for the sierra_luxe project.
These exceptions provide specific error types for different application scenarios.
"""


class SierraLuxeException(Exception):
    """Base exception for all custom exceptions in the project."""
    def __init__(self, message="An error occurred", status_code=500, details=None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundException(SierraLuxeException):
    """Exception raised when a requested resource is not found."""
    def __init__(self, resource_type="Resource", resource_id=None, message=None):
        if message is None:
            if resource_id:
                message = f"{resource_type} with ID {resource_id} not found"
            else:
                message = f"{resource_type} not found"
        super().__init__(message=message, status_code=404, details={
            'resource_type': resource_type,
            'resource_id': resource_id
        })


class PermissionDeniedException(SierraLuxeException):
    """Exception raised when a user doesn't have permission to perform an action."""
    def __init__(self, action="perform this action", resource=None, message=None):
        if message is None:
            if resource:
                message = f"You don't have permission to {action} on {resource}"
            else:
                message = f"You don't have permission to {action}"
        super().__init__(message=message, status_code=403, details={
            'action': action,
            'resource': resource
        })


class ValidationException(SierraLuxeException):
    """Exception raised when form or data validation fails."""
    def __init__(self, errors=None, message="Validation failed"):
        super().__init__(message=message, status_code=400, details={
            'errors': errors or {}
        })


class AuthenticationException(SierraLuxeException):
    """Exception raised when authentication fails."""
    def __init__(self, message="Authentication failed"):
        super().__init__(message=message, status_code=401)


class RateLimitException(SierraLuxeException):
    """Exception raised when rate limit is exceeded."""
    def __init__(self, retry_after=None, message="Rate limit exceeded"):
        super().__init__(message=message, status_code=429, details={
            'retry_after': retry_after
        })


class ExternalServiceException(SierraLuxeException):
    """Exception raised when an external service call fails."""
    def __init__(self, service_name="External Service", message=None, original_error=None):
        if message is None:
            message = f"Failed to communicate with {service_name}"
        super().__init__(message=message, status_code=503, details={
            'service_name': service_name,
            'original_error': str(original_error) if original_error else None
        })


class DatabaseException(SierraLuxeException):
    """Exception raised when database operations fail."""
    def __init__(self, operation="database operation", message=None, original_error=None):
        if message is None:
            message = f"Failed to perform {operation}"
        super().__init__(message=message, status_code=500, details={
            'operation': operation,
            'original_error': str(original_error) if original_error else None
        })


class FileUploadException(SierraLuxeException):
    """Exception raised when file upload fails."""
    def __init__(self, reason="File upload failed", message=None):
        if message is None:
            message = f"File upload failed: {reason}"
        super().__init__(message=message, status_code=400, details={
            'reason': reason
        })
