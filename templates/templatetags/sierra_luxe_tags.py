from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def format_price(price):
    """Format price to currency format"""
    if price is None:
        return '$0.00'
    return f'${price:.2f}'

@register.filter
def calculate_discount(original_price, discount_price):
    """Calculate discount percentage"""
    if discount_price and original_price > discount_price:
        return int(((original_price - discount_price) / original_price) * 100)
    return 0

@register.filter
def get_item(dictionary, key):
    """Get item from dictionary"""
    return dictionary.get(key)

@register.simple_tag
def current_year():
    """Return current year"""
    return timezone.now().year

@register.simple_tag
def get_range(count):
    """Generate range for template iteration"""
    return range(count)

@register.filter
def truncate_chars(value, arg):
    """Truncate string to specified character count"""
    if len(value) > arg:
        return value[:arg] + '...'
    return value

@register.filter
def star_rating(rating):
    """Generate star rating HTML"""
    stars = ''
    for i in range(1, 6):
        if i <= rating:
            stars += '<i class="fas fa-star text-warning"></i>'
        elif i - 0.5 <= rating:
            stars += '<i class="fas fa-star-half-alt text-warning"></i>'
        else:
            stars += '<i class="far fa-star text-warning"></i>'
    return stars
