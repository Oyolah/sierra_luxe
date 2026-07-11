"""
Custom error handlers for the sierra_luxe project.
These views provide user-friendly error pages while logging detailed error information.
"""
import logging
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound, HttpResponseServerError

logger = logging.getLogger(__name__)


def custom_bad_request(request, exception=None):
    """
    Custom handler for 400 Bad Request errors.
    Logs the error and renders a user-friendly error page.
    """
    user = getattr(request, 'user', None)
    logger.warning(
        "Bad Request: %s - Path: %s - User: %s - Exception: %s",
        request.method,
        request.path,
        str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else "Anonymous",
        str(exception) if exception else "No exception details"
    )
    return render(request, 'errors/400.html', status=400)


def custom_permission_denied(request, exception=None):
    """
    Custom handler for 403 Forbidden errors.
    Logs the error and renders a user-friendly error page.
    """
    user = getattr(request, 'user', None)
    logger.warning(
        "Permission Denied: %s - Path: %s - User: %s - Exception: %s",
        request.method,
        request.path,
        str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else "Anonymous",
        str(exception) if exception else "No exception details"
    )
    return render(request, 'errors/403.html', status=403)


def custom_page_not_found(request, exception=None):
    """
    Custom handler for 404 Not Found errors.
    Logs the error and renders a user-friendly error page.
    """
    user = getattr(request, 'user', None)
    logger.info(
        "Page Not Found: %s - Path: %s - User: %s - Exception: %s",
        request.method,
        request.path,
        str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else "Anonymous",
        str(exception) if exception else "No exception details"
    )
    return render(request, 'errors/404.html', status=404)


def custom_server_error(request):
    """
    Custom handler for 500 Internal Server Error.
    Logs the error with full traceback and renders a user-friendly error page.
    """
    user = getattr(request, 'user', None)
    logger.exception(
        "Internal Server Error - Method: %s - Path: %s - User: %s",
        request.method,
        request.path,
        str(user) if user and hasattr(user, 'is_authenticated') and user.is_authenticated else "Anonymous"
    )
    return render(request, 'errors/500.html', status=500)
