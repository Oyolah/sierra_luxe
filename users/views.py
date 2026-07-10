from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.db import DatabaseError
import logging
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm
from sierra_luxe.decorators import admin_required, customer_required
from sierra_luxe.api_responses import success_response, error_response, validation_error_response
from sierra_luxe.exceptions import ValidationException, DatabaseException
from .models import RecentlyViewed

logger = logging.getLogger(__name__)


def auth_page(request):
    """Unified authentication page with login and register tabs"""
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    # Check if user was logged out due to session timeout
    if request.GET.get('session_timeout') == 'true':
        messages.warning(request, 'You were logged out due to inactivity. Please log in again.')
    
    # Determine which tab to show based on URL parameter
    show_register = request.GET.get('tab') == 'register'
    
    return render(request, 'users/auth.html', {
        'show_register': show_register
    })


def rate_limit(max_attempts=5, timeout=300):
    """Rate limiting decorator to prevent brute force attacks"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Get client IP
            ip = request.META.get('REMOTE_ADDR')
            cache_key = f'rate_limit_{ip}_{view_func.__name__}'
            attempts = cache.get(cache_key, 0)
            
            if attempts >= max_attempts:
                return HttpResponseForbidden('Too many attempts. Please try again later.')
            
            cache.set(cache_key, attempts + 1, timeout)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_attempts=5, timeout=300)
def register(request):
    """Handle user registration with proper error handling"""
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                
                # Handle AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return success_response(
                        data={'username': username},
                        message=f'Account created for {username}! You can now log in.'
                    )
                
                messages.success(request, f'Account created for {username}! You can now log in.')
                return redirect('users:auth')
            else:
                # Handle AJAX requests with errors
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return validation_error_response(
                        errors=dict(form.errors),
                        message='Registration failed. Please check your input.'
                    )
        else:
            form = UserRegistrationForm()
        
        return render(request, 'users/auth.html', {'form': form})
    
    except DatabaseError as e:
        logger.error(f"Database error during registration: {str(e)}")
        messages.error(request, 'A database error occurred. Please try again.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return error_response(
                error='DatabaseError',
                message='A database error occurred. Please try again later.',
                status_code=500
            )
        return render(request, 'users/auth.html', {'form': form})
    
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        messages.error(request, 'An unexpected error occurred. Please try again.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return error_response(
                error='InternalServerError',
                message='An unexpected error occurred. Please try again later.',
                status_code=500
            )
        return render(request, 'users/auth.html', {'form': form})

@rate_limit(max_attempts=5, timeout=300)
def user_login(request):
    """Handle user login with proper error handling"""
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    # Check if user was logged out due to session timeout
    if request.GET.get('session_timeout') == 'true':
        messages.warning(request, 'You were logged out due to inactivity. Please log in again.')
    
    try:
        if request.method == 'POST':
            form = UserLoginForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    
                    # Handle AJAX requests
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        next_page = request.GET.get('next', reverse('catalog:home'))
                        return success_response(
                            data={'redirect': next_page},
                            message=f'Welcome back, {username}!'
                        )
                    
                    messages.success(request, f'Welcome back, {username}!')
                    next_page = request.GET.get('next', 'catalog:home')
                    return redirect(next_page)
                else:
                    # Handle AJAX requests with errors
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return error_response(
                            error='AuthenticationError',
                            message='Invalid username or password.',
                            status_code=401
                        )
            else:
                # Handle AJAX requests with errors
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return validation_error_response(
                        errors=dict(form.errors),
                        message='Invalid login credentials.'
                    )
        else:
            form = UserLoginForm()
        
        return render(request, 'users/auth.html', {'form': form})
    
    except DatabaseError as e:
        logger.error(f"Database error during login: {str(e)}")
        messages.error(request, 'A database error occurred. Please try again.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return error_response(
                error='DatabaseError',
                message='A database error occurred. Please try again later.',
                status_code=500
            )
        return render(request, 'users/auth.html', {'form': form})
    
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        messages.error(request, 'An unexpected error occurred. Please try again.')
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return error_response(
                error='InternalServerError',
                message='An unexpected error occurred. Please try again later.',
                status_code=500
            )
        return render(request, 'users/auth.html', {'form': form})

def user_logout(request):
    logout(request)
    
    # Check if logout was due to session timeout
    if request.GET.get('session_timeout') == 'true':
        return redirect(f"{reverse('users:login')}?session_timeout=true")
    
    messages.info(request, 'You have been logged out.')
    return redirect('catalog:home')

@login_required
@customer_required
def profile(request):
    # Data isolation: users can only view their own profile
    # No need to filter since we're using request.user
    return render(request, 'users/profile.html')

@login_required
@customer_required
def profile_edit(request):
    """Handle profile editing with proper error handling"""
    try:
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('users:profile')
        else:
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.profile)
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'users/profile_edit.html', context)
    
    except DatabaseError as e:
        logger.error(f"Database error during profile edit: {str(e)}")
        messages.error(request, 'A database error occurred. Please try again.')
        return redirect('users:profile')
    
    except Exception as e:
        logger.error(f"Unexpected error during profile edit: {str(e)}", exc_info=True)
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return redirect('users:profile')

@login_required
def recently_viewed(request):
    """Display recently viewed products"""
    recent_items = RecentlyViewed.objects.filter(user=request.user).select_related('product')[:20]
    return render(request, 'users/recently_viewed.html', {
        'recent_items': recent_items
    })
