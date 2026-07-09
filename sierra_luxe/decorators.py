from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from functools import wraps

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
