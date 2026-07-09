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
