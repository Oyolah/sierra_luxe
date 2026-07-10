from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from catalog.models import Product
from .models import Review, Like
from .forms import ReviewForm


def get_product_rating_data(product):
    """Get average rating and review count for a product"""
    reviews = product.reviews.filter(is_approved=True)
    count = reviews.count()
    if count > 0:
        average = sum(r.rating for r in reviews) / count
    else:
        average = 0
    rating_distribution = {
        5: reviews.filter(rating=5).count(),
        4: reviews.filter(rating=4).count(),
        3: reviews.filter(rating=3).count(),
        2: reviews.filter(rating=2).count(),
        1: reviews.filter(rating=1).count(),
    }
    return {
        'average': round(average, 1),
        'count': count,
        'distribution': rating_distribution,
    }


def get_product_like_data(product, user=None):
    """Get like count and user's like status for a product"""
    like_count = product.likes.count()
    is_liked = False
    if user and user.is_authenticated:
        is_liked = product.likes.filter(user=user).exists()
    return {
        'like_count': like_count,
        'is_liked': is_liked,
    }


@require_POST
@login_required
def toggle_like(request, product_id):
    """Toggle like/unlike for a product (AJAX)"""
    product = get_object_or_404(Product, id=product_id)
    
    # Validate that product exists and is active
    if not product.is_active:
        return JsonResponse({
            'success': False,
            'error': 'This product is not available.'
        }, status=400)
    
    like, created = Like.objects.get_or_create(
        product=product,
        user=request.user
    )
    
    if not created:
        # User already liked, so unlike
        like.delete()
        is_liked = False
        message = 'Product unliked'
    else:
        is_liked = True
        message = 'Product liked'
    
    like_data = get_product_like_data(product, request.user)
    
    return JsonResponse({
        'success': True,
        'is_liked': is_liked,
        'like_count': like_data['like_count'],
        'message': message,
    })


def product_reviews_api(request, product_id):
    """Get reviews for a product as JSON (AJAX)"""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.filter(is_approved=True).select_related('customer')
    
    data = []
    for review in reviews:
        data.append({
            'id': review.id,
            'customer': review.customer.username,
            'rating': review.rating,
            'title': review.title,
            'comment': review.comment,
            'is_verified_purchase': review.is_verified_purchase,
            'created_at': review.created_at.strftime('%B %d, %Y'),
        })
    
    rating_data = get_product_rating_data(product)
    
    return JsonResponse({
        'success': True,
        'reviews': data,
        'average_rating': rating_data['average'],
        'review_count': rating_data['count'],
        'distribution': rating_data['distribution'],
    })


@require_POST
@login_required
def add_review(request, product_id):
    """Submit a review for a product (AJAX)"""
    product = get_object_or_404(Product, id=product_id)
    form = ReviewForm(request.POST)
    
    if form.is_valid():
        # Check if user already reviewed this product
        existing_review = Review.objects.filter(product=product, customer=request.user).first()
        if existing_review:
            return JsonResponse({
                'success': False,
                'error': 'You have already reviewed this product. You can edit your existing review.'
            }, status=400)
        
        review = form.save(commit=False)
        review.product = product
        review.customer = request.user
        # Optionally check if the user has purchased the product
        review.is_verified_purchase = product.order_items.filter(order__customer=request.user).exists()
        review.save()
        
        # Update store total reviews count
        from catalog.models import Store
        store = Store.objects.first()
        if store:
            store.total_reviews = Review.objects.filter(is_approved=True).count()
            # Update store average rating
            all_reviews = Review.objects.filter(is_approved=True)
            if all_reviews.count() > 0:
                store.average_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
            store.save()
        
        rating_data = get_product_rating_data(product)
        
        return JsonResponse({
            'success': True,
            'message': 'Review submitted successfully!',
            'review': {
                'id': review.id,
                'customer': review.customer.username,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'is_verified_purchase': review.is_verified_purchase,
                'created_at': review.created_at.strftime('%B %d, %Y'),
            },
            'average_rating': rating_data['average'],
            'review_count': rating_data['count'],
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


@require_POST
@login_required
def update_review(request, product_id):
    """Update an existing review (AJAX)"""
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(Review, product=product, customer=request.user)
    form = ReviewForm(request.POST, instance=review)
    
    if form.is_valid():
        review = form.save()
        
        rating_data = get_product_rating_data(product)
        
        return JsonResponse({
            'success': True,
            'message': 'Review updated successfully!',
            'review': {
                'id': review.id,
                'customer': review.customer.username,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'is_verified_purchase': review.is_verified_purchase,
                'created_at': review.created_at.strftime('%B %d, %Y'),
            },
            'average_rating': rating_data['average'],
            'review_count': rating_data['count'],
        })
    else:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)

