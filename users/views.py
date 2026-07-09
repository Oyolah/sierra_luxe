from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm
from sierra_luxe.decorators import admin_required, customer_required
from .models import RecentlyViewed


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
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

@rate_limit(max_attempts=5, timeout=300)
def user_login(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_page = request.GET.get('next', 'catalog:home')
                return redirect(next_page)
    else:
        form = UserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
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
