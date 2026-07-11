"""
Global error handling middleware for the sierra_luxe project.
This middleware catches unhandled exceptions and converts them to appropriate responses.
"""
import logging
import traceback
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import DatabaseError
from django.conf import settings
from .exceptions import SierraLuxeException

logger = logging.getLogger(__name__)


class GlobalExceptionHandlerMiddleware:
    """
    Middleware to handle all unhandled exceptions globally.
    Catches exceptions and returns appropriate JSON or HTML responses.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)
    
    def process_exception(self, request, exception):
        """
        Handle unhandled exceptions from views.
        Returns appropriate response based on exception type and request format.
        """
        # Log the exception with full traceback
        logger.exception(
            "Unhandled exception - Type: %s - Message: %s - Method: %s - Path: %s - User: %s",
            type(exception).__name__,
            str(exception),
            request.method,
            request.path,
            str(request.user) if request.user.is_authenticated else "Anonymous"
        )
        
        # Check if request expects JSON response
        if self._is_api_request(request):
            return self._handle_api_exception(request, exception)
        
        # For regular web requests, let Django's default error handlers handle it
        # They will use our custom error pages configured in urls.py
        return None
    
    def _is_api_request(self, request):
        """
        Determine if the request expects a JSON response.
        Checks headers and content type.
        """
        return (
            request.headers.get('Accept') == 'application/json' or
            request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
            request.content_type == 'application/json' or
            request.path.startswith('/api/')
        )
    
    def _handle_api_exception(self, request, exception):
        """
        Handle exceptions for API requests and return JSON response.
        """
        # Handle custom SierraLuxe exceptions
        if isinstance(exception, SierraLuxeException):
            return JsonResponse({
                'success': False,
                'error': type(exception).__name__,
                'message': exception.message,
                'details': exception.details,
                'status_code': exception.status_code,
                'timestamp': self._get_timestamp()
            }, status=exception.status_code)
        
        # Handle Django built-in exceptions
        if isinstance(exception, PermissionDenied):
            return JsonResponse({
                'success': False,
                'error': 'PermissionDenied',
                'message': 'You do not have permission to perform this action',
                'details': {},
                'status_code': 403,
                'timestamp': self._get_timestamp()
            }, status=403)
        
        if isinstance(exception, ValidationError):
            return JsonResponse({
                'success': False,
                'error': 'ValidationError',
                'message': 'Validation failed',
                'details': {'errors': dict(exception)},
                'status_code': 400,
                'timestamp': self._get_timestamp()
            }, status=400)
        
        if isinstance(exception, DatabaseError):
            return JsonResponse({
                'success': False,
                'error': 'DatabaseError',
                'message': 'A database error occurred. Please try again later.',
                'details': {},
                'status_code': 500,
                'timestamp': self._get_timestamp()
            }, status=500)
        
        # Handle generic exceptions
        # In production, don't expose exception details
        if settings.DEBUG:
            error_message = str(exception)
            error_details = {
                'exception_type': type(exception).__name__,
                'traceback': traceback.format_exc()
            }
        else:
            error_message = 'An unexpected error occurred. Please try again later.'
            error_details = {}
        
        return JsonResponse({
            'success': False,
            'error': 'InternalServerError',
            'message': error_message,
            'details': error_details,
            'status_code': 500,
            'timestamp': self._get_timestamp()
        }, status=500)
    
    def _get_timestamp(self):
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'
