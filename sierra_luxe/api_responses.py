"""
API response utilities for consistent error handling across the application.
Provides functions to create standardized JSON responses for success and error cases.
"""
from datetime import datetime
from django.http import JsonResponse
from typing import Any, Dict, Optional


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200
) -> JsonResponse:
    """
    Create a standardized success response.
    
    Args:
        data: The response data (can be any JSON-serializable type)
        message: Success message
        status_code: HTTP status code (default: 200)
    
    Returns:
        JsonResponse with standardized format
    """
    response_data = {
        'success': True,
        'message': message,
        'data': data,
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    return JsonResponse(response_data, status=status_code)


def error_response(
    error: str,
    message: str,
    details: Optional[Dict] = None,
    status_code: int = 400
) -> JsonResponse:
    """
    Create a standardized error response.
    
    Args:
        error: Error type/name
        message: Error message
        details: Additional error details (optional)
        status_code: HTTP status code (default: 400)
    
    Returns:
        JsonResponse with standardized error format
    """
    response_data = {
        'success': False,
        'error': error,
        'message': message,
        'details': details or {},
        'status_code': status_code,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    return JsonResponse(response_data, status=status_code)


def validation_error_response(
    errors: Dict,
    message: str = "Validation failed"
) -> JsonResponse:
    """
    Create a validation error response.
    
    Args:
        errors: Dictionary of field errors
        message: Error message
    
    Returns:
        JsonResponse with validation error format
    """
    return error_response(
        error='ValidationError',
        message=message,
        details={'errors': errors},
        status_code=400
    )


def not_found_response(
    resource_type: str = "Resource",
    resource_id: Optional[str] = None
) -> JsonResponse:
    """
    Create a not found error response.
    
    Args:
        resource_type: Type of resource that was not found
        resource_id: ID of the resource (optional)
    
    Returns:
        JsonResponse with 404 error format
    """
    if resource_id:
        message = f"{resource_type} with ID {resource_id} not found"
    else:
        message = f"{resource_type} not found"
    
    return error_response(
        error='NotFound',
        message=message,
        details={
            'resource_type': resource_type,
            'resource_id': resource_id
        },
        status_code=404
    )


def permission_denied_response(
    action: str = "perform this action",
    resource: Optional[str] = None
) -> JsonResponse:
    """
    Create a permission denied error response.
    
    Args:
        action: Action that was denied
        resource: Resource on which action was denied (optional)
    
    Returns:
        JsonResponse with 403 error format
    """
    if resource:
        message = f"You don't have permission to {action} on {resource}"
    else:
        message = f"You don't have permission to {action}"
    
    return error_response(
        error='PermissionDenied',
        message=message,
        details={
            'action': action,
            'resource': resource
        },
        status_code=403
    )


def authentication_error_response(
    message: str = "Authentication required"
) -> JsonResponse:
    """
    Create an authentication error response.
    
    Args:
        message: Error message
    
    Returns:
        JsonResponse with 401 error format
    """
    return error_response(
        error='AuthenticationError',
        message=message,
        status_code=401
    )


def server_error_response(
    message: str = "An unexpected error occurred"
) -> JsonResponse:
    """
    Create a server error response.
    
    Args:
        message: Error message
    
    Returns:
        JsonResponse with 500 error format
    """
    return error_response(
        error='InternalServerError',
        message=message,
        status_code=500
    )


def rate_limit_response(
    retry_after: Optional[int] = None
) -> JsonResponse:
    """
    Create a rate limit error response.
    
    Args:
        retry_after: Seconds until retry is allowed (optional)
    
    Returns:
        JsonResponse with 429 error format
    """
    details = {}
    if retry_after:
        details['retry_after'] = retry_after
    
    return error_response(
        error='RateLimitExceeded',
        message="Rate limit exceeded. Please try again later.",
        details=details,
        status_code=429
    )
