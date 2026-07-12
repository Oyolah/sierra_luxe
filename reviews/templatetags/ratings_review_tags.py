from django import template

register = template.Library()


@register.filter
def average_rating(product):
    """Get average rating for a product"""
    reviews = product.reviews.filter(is_approved=True)
    if reviews.count() == 0:
        return 0
    return sum(r.rating for r in reviews) / reviews.count()


@register.filter
def review_count(product):
    """Get approved review count for a product"""
    return product.reviews.filter(is_approved=True).count()


@register.inclusion_tag('components/star_rating.html')
def star_rating(rating, review_count=None):
    """Render star rating with optional review count"""
    full_stars = int(rating)
    has_half = (rating - full_stars) >= 0.5
    empty_stars = 5 - full_stars - (1 if has_half else 0)
    return {
        'rating': rating,
        'full_stars': range(full_stars),
        'has_half': has_half,
        'empty_stars': range(empty_stars),
        'review_count': review_count,
    }


@register.filter
def category_image(category):
    """Get image URL for a category - uses the category's uploaded Cloudinary image"""
    # If category has an image, return its URL (handle CloudinaryField)
    if hasattr(category, 'image') and category.image:
        return category.image.url if hasattr(category.image, 'url') else str(category.image)
    
    # No image uploaded - return None to let template handle fallback
    return None


@register.filter
def image_url(image_field):
    """Get URL from image field, handling both CloudinaryField and string URLs"""
    if not image_field:
        return None
    return image_field.url if hasattr(image_field, 'url') else str(image_field)


@register.filter
def status_badge_class(status, type='default'):
    """Get Bootstrap badge classes for different status types"""
    if type == 'order':
        status_map = {
            'DELIVERED': 'success',
            'CANCELLED': 'danger',
            'SHIPPED': 'info',
            'PENDING': 'warning',
        }
        return status_map.get(status, 'primary')
    elif type == 'product':
        return 'success' if status else 'secondary'
    elif type == 'user_role':
        return 'danger' if status == 'ADMIN' else 'info'
    elif type == 'user_active':
        return 'success' if status else 'danger'
    return 'primary'


@register.filter
def like_count(product):
    """Get like count for a product with error handling"""
    try:
        return product.likes.count()
    except:
        return 0
