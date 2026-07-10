from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm
from sierra_luxe.decorators import admin_required, customer_required
from .models import RecentlyViewed


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
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'Account created for {username}! You can now log in.'
                })
            
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
        else:
            # Handle AJAX requests with errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Registration failed. Please check your input.',
                    'errors': form.errors
                })
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/auth.html', {'form': form})

@rate_limit(max_attempts=5, timeout=300)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    # Check if user was logged out due to session timeout
    if request.GET.get('session_timeout') == 'true':
        messages.warning(request, 'You were logged out due to inactivity. Please log in again.')
    
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
                    return JsonResponse({
                        'success': True,
                        'message': f'Welcome back, {username}!',
                        'redirect': next_page
                    })
                
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'catalog:home')
                return redirect(next_page)
        else:
            # Handle AJAX requests with errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid username or password.',
                    'errors': form.errors
                })
    else:
        form = UserLoginForm()
    
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
    # Data isolation: users can only edit their own profile
    # Using request.user ensures they can only modify their own data
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

@login_required
def recently_viewed(request):
    """Display recently viewed products"""
    recent_items = RecentlyViewed.objects.filter(user=request.user).select_related('product')[:20]
    return render(request, 'users/recently_viewed.html', {
        'recent_items': recent_items
    })
