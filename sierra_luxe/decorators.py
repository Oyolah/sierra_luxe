from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(view_func):
    """
    Decorator to restrict access to admin users only.
    Must be used after @login_required.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'ADMIN':
            return redirect('users:profile')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def customer_required(view_func):
    """
    Decorator to restrict access to customer users only.
    Must be used after @login_required.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if request.user.role != 'CUSTOMER':
            return redirect('admin:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def admin_or_customer_required(view_func):
    """
    Decorator to restrict access to authenticated users only (both admin and customer).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Combined decorators to reduce repetition
def login_admin_required(view_func):
    """Combined decorator for login required + admin required"""
    return login_required(admin_required(view_func))

def login_customer_required(view_func):
    """Combined decorator for login required + customer required"""
    return login_required(customer_required(view_func))

def dashboard_required(view_func):
    """
    Decorator to restrict access to dashboard (staff or superuser).
    SuperAdmins bypass all permission checks.
    Staff users must have is_staff=True.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_staff or request.user.is_superuser):
            return redirect('catalog:home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def dashboard_permission_required(permission_code):
    """
    Decorator to check if user has specific dashboard permission.
    SuperAdmins automatically pass all permission checks.
    Shows toast notification for permission denied.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('users:login')
            
            # SuperAdmin bypasses all permission checks
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user is staff and has the required permission
            if not request.user.is_staff:
                return redirect('catalog:home')
            
            if not request.user.has_dashboard_permission(permission_code):
                from django.contrib import messages
                
                # Handle AJAX requests with JSON response
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({
                        'success': False,
                        'error': 'PermissionDenied',
                        'message': 'You do not have permission to perform this action.'
                    }, status=403)
                
                # For regular requests, show error message and redirect to safe page
                messages.error(request, 'You do not have permission to access this section.')
                
                # Redirect to dashboard (safe page they can access)
                return redirect('admin_dashboard:dashboard')
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def login_dashboard_required(view_func):
    """Combined decorator for login required + dashboard access"""
    return login_required(dashboard_required(view_func))
