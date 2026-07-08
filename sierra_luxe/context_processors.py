from django.conf import settings
from .models import User

def site_settings(request):
    """Global site settings available in all templates"""
    return {
        'site_name': 'Sierra Luxe',
        'site_description': 'Authentic African Fashion for Women, Men & Kids',
        'contact_email': 'info@sierraluxe.com',
        'contact_phone': '+1 (555) 123-4567',
        'social_media': {
            'facebook': 'https://facebook.com/sierraluxe',
            'instagram': 'https://instagram.com/sierraluxe',
            'twitter': 'https://twitter.com/sierraluxe',
        }
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

def user_wishlist_count(request):
    """Get wishlist count for authenticated users"""
    if request.user.is_authenticated:
        return {'wishlist_count': request.user.wishlist.count()}
    return {'wishlist_count': 0}
