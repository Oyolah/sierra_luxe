from django.conf import settings
from .constants import CURRENCY_SYMBOL, SITE_NAME, SITE_DESCRIPTION, CONTACT_EMAIL, CONTACT_PHONE, SOCIAL_MEDIA

def site_settings(request):
    """Global site settings available in all templates"""
    return {
        'site_name': SITE_NAME,
        'site_description': SITE_DESCRIPTION,
        'contact_email': CONTACT_EMAIL,
        'contact_phone': CONTACT_PHONE,
        'social_media': SOCIAL_MEDIA,
        'currency_symbol': CURRENCY_SYMBOL,
    }

def cart_count(request):
    """Get cart item count for authenticated users"""
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            return {'cart_count': cart.get_item_count()}
        except:
            return {'cart_count': 0}
    return {'cart_count': 0}

def categories_context(request):
    """Provide active categories to all templates"""
    from catalog.models import Category
    try:
        categories = Category.objects.filter(is_active=True, show_in_navbar=True)
        return {'nav_categories': categories}
    except:
        return {'nav_categories': []}

def dashboard_permissions(request):
    """Provide dashboard permission checks as context variables"""
    if not request.user.is_authenticated:
        return {}
    
    if request.user.is_superuser:
        # SuperAdmin has all permissions
        return {
            'can_view_dashboard': True,
            'can_view_products': True,
            'can_view_categories': True,
            'can_view_orders': True,
            'can_view_reviews': True,
            'can_view_likes': True,
            'can_view_users': True,
            'can_view_roles': True,
            'can_manage_roles': True,
        }
    
    if not request.user.is_staff:
        return {}
    
    return {
        'can_view_dashboard': request.user.has_dashboard_permission('view_dashboard'),
        'can_view_products': request.user.has_dashboard_permission('view_products'),
        'can_view_categories': request.user.has_dashboard_permission('view_categories'),
        'can_view_orders': request.user.has_dashboard_permission('view_orders'),
        'can_view_reviews': request.user.has_dashboard_permission('view_reviews'),
        'can_view_likes': request.user.has_dashboard_permission('view_likes'),
        'can_view_users': request.user.has_dashboard_permission('view_users'),
        'can_view_roles': request.user.has_dashboard_permission('view_roles'),
        'can_manage_roles': request.user.has_dashboard_permission('manage_roles'),
    }
