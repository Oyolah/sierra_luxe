from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Count, Q
import logging
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, UserUpdateForm
from sierra_luxe.decorators import admin_required, customer_required
from sierra_luxe.api_responses import success_response, error_response, validation_error_response
from sierra_luxe.exceptions import ValidationException, DatabaseException
from .models import RecentlyViewed, BillingAddress
from orders.models import Order, OrderItem
from reviews.models import Review, Like
from catalog.models import Product

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
        # Redirect based on user type if already authenticated
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard:dashboard')
        return redirect('users:customer_dashboard')
    
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
                    
                    # Determine redirect based on user type
                    if user.is_staff or user.is_superuser:
                        default_redirect = '/admin-dashboard/'
                    else:
                        default_redirect = '/customer-dashboard/'
                    
                    # Handle AJAX requests
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        next_page = request.GET.get('next', default_redirect)
                        return success_response(
                            data={'redirect': next_page},
                            message=f'Welcome back, {username}!'
                        )
                    
                    messages.success(request, f'Welcome back, {username}!')
                    next_page = request.GET.get('next', default_redirect)
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


# ============ CUSTOMER DASHBOARD VIEWS ============

@login_required
@customer_required
def customer_dashboard(request):
    """Customer dashboard home with overview"""
    # Security: Always use request.user, never trust user_id from request
    user = request.user
    
    # Get customer's orders
    orders = Order.objects.filter(customer=user).order_by('-created_at')
    total_orders = orders.count()
    pending_orders = orders.filter(status='PENDING').count()
    completed_orders = orders.filter(status='DELIVERED').count()
    
    # Get customer's likes
    likes = Like.objects.filter(user=user).select_related('product')[:5]
    
    # Get customer's reviews
    reviews = Review.objects.filter(customer=user).select_related('product')[:5]
    
    # Get recent orders
    recent_orders = orders[:5]
    
    context = {
        'user': user,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'likes': likes,
        'reviews': reviews,
        'recent_orders': recent_orders,
    }
    return render(request, 'users/customer_dashboard.html', context)


@login_required
@customer_required
def customer_orders(request):
    """Customer's order history"""
    # Security: Always use request.user
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
    }
    return render(request, 'users/customer_orders.html', context)


@login_required
@customer_required
def customer_order_detail(request, order_id):
    """Customer's order details with IDOR protection"""
    # Security: Always filter by request.user to prevent IDOR
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    items = order.items.select_related('product')
    
    context = {
        'order': order,
        'items': items,
    }
    return render(request, 'users/customer_order_detail.html', context)


@login_required
@customer_required
def customer_wishlist(request):
    """Customer's wishlist/liked products"""
    # Security: Always use request.user
    likes = Like.objects.filter(user=request.user).select_related('product').order_by('-created_at')
    
    context = {
        'likes': likes,
    }
    return render(request, 'users/customer_wishlist.html', context)


@login_required
@customer_required
def customer_reviews(request):
    """Customer's reviews"""
    # Security: Always use request.user
    reviews = Review.objects.filter(customer=request.user).select_related('product').order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    return render(request, 'users/customer_reviews.html', context)


@login_required
@customer_required
def customer_billing_address(request):
    """Customer's billing addresses"""
    # Security: Always use request.user
    addresses = BillingAddress.objects.filter(user=request.user).order_by('-is_default', '-created_at')
    
    context = {
        'addresses': addresses,
    }
    return render(request, 'users/customer_billing_address.html', context)


@login_required
@customer_required
def customer_billing_address_edit(request):
    """Add or edit billing address"""
    # Security: Always use request.user
    user = request.user
    
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        
        if address_id:
            # Edit existing address
            address = get_object_or_404(BillingAddress, id=address_id, user=user)
            address.full_name = request.POST.get('full_name')
            address.address_line1 = request.POST.get('address_line1')
            address.address_line2 = request.POST.get('address_line2', '')
            address.city = request.POST.get('city')
            address.state_province = request.POST.get('state_province', '')
            address.postal_code = request.POST.get('postal_code')
            address.country = request.POST.get('country')
            address.phone = request.POST.get('phone')
            address.is_default = request.POST.get('is_default') == 'on'
            address.save()
            messages.success(request, 'Billing address updated successfully.')
        else:
            # Create new address
            BillingAddress.objects.create(
                user=user,
                full_name=request.POST.get('full_name'),
                address_line1=request.POST.get('address_line1'),
                address_line2=request.POST.get('address_line2', ''),
                city=request.POST.get('city'),
                state_province=request.POST.get('state_province', ''),
                postal_code=request.POST.get('postal_code'),
                country=request.POST.get('country'),
                phone=request.POST.get('phone'),
                is_default=request.POST.get('is_default') == 'on'
            )
            messages.success(request, 'Billing address added successfully.')
        
        return redirect('users:customer_billing_address')
    
    # GET request - show form
    address_id = request.GET.get('address_id')
    address = None
    if address_id:
        address = get_object_or_404(BillingAddress, id=address_id, user=user)
    
    context = {
        'address': address,
    }
    return render(request, 'users/customer_billing_address_edit.html', context)


@login_required
@customer_required
def customer_change_password(request):
    """Customer change password"""
    # Security: Always use request.user
    user = request.user
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if not user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
            return redirect('users:customer_change_password')
        
        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('users:customer_change_password')
        
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('users:customer_change_password')
        
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password changed successfully.')
        return redirect('users:customer_dashboard')
    
    return render(request, 'users/customer_change_password.html')
