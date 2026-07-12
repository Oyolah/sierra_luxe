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

