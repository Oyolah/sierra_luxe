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
    """Get image URL for a category based on name"""
    category_images = {
        'women': 'https://res.cloudinary.com/dvcnxfxfu/image/upload/v1/sierra_luxe/products/African Lace Maxi Dress 1.webp',
        'men': 'https://res.cloudinary.com/dvcnxfxfu/image/upload/v1/sierra_luxe/products/luxurious-aso-oke-with-embroidered-agbada-for-groom-1.avif',
        'kids': 'https://res.cloudinary.com/dvcnxfxfu/image/upload/v1/sierra_luxe/products/baby-girl-ankara-ball-gown-dress-1.webp',
        'wedding': 'https://res.cloudinary.com/dvcnxfxfu/image/upload/v1/sierra_luxe/products/aso-oke-couple-outfits-1.webp',
        'traditional': 'https://res.cloudinary.com/dvcnxfxfu/image/upload/v1/sierra_luxe/products/red-beaded-african-dress-1.webp',
    }
    category_name_lower = category.name.lower() if hasattr(category, 'name') else str(category).lower()
    
    # If category has an image, return its URL (handle CloudinaryField)
    if hasattr(category, 'image') and category.image:
        return category.image.url if hasattr(category.image, 'url') else str(category.image)
    
    # Fallback to hardcoded images
    return category_images.get(category_name_lower)


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
