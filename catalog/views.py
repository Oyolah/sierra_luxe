from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Store
from users.models import RecentlyViewed
from reviews.views import get_product_rating_data


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })

def product_list(request):
    products = Product.objects.filter(is_active=True)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(price__lte=max_price)
    
    size = request.GET.get('size')
    if size:
        products = products.filter(sizes__icontains=size)
    
    color = request.GET.get('color')
    if color:
        products = products.filter(colors__icontains=color)
    
    categories = Category.objects.all()
    
    # AJAX request - return JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        products_data = []
        for product in products:
            rating_data = get_product_rating_data(product)
            products_data.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'price': str(product.price),
                'discount_price': str(product.discount_price) if product.discount_price else None,
                'description': product.description[:80],
                'image': product.main_image if product.main_image else None,
                'average_rating': rating_data['average'],
                'review_count': rating_data['count'],
            })
        return JsonResponse({
            'products': products_data,
            'count': products.count()
        })
    
    return render(request, 'catalog/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    # Get store data
    try:
        store, _ = Store.objects.get_or_create(
            name='Sierra Luxe',
            defaults={
                'smooth_shipping': True,
                'speedy_replies': True,
                'average_rating': 4.8,
                'total_reviews': 0
            }
        )
    except:
        # Store table doesn't exist yet, use default values
        class DefaultStore:
            name = 'Sierra Luxe'
            smooth_shipping = True
            speedy_replies = True
            average_rating = 4.8
            total_reviews = 0
        store = DefaultStore()
    
    # Get review and rating data
    reviews = product.reviews.filter(is_approved=True).select_related('customer')
    rating_data = get_product_rating_data(product)
    average_rating = rating_data['average']
    review_count = rating_data['count']
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = product.reviews.filter(customer=request.user).exists()
    
    # Get like data
    from reviews.views import get_product_like_data
    like_data = get_product_like_data(product, request.user)
    like_count = like_data['like_count']
    is_liked = like_data['is_liked']
    
    # Get shop-wide reviews
    from reviews.models import Review
    shop_reviews = Review.objects.filter(is_approved=True).select_related('customer', 'product').order_by('-created_at')[:10]
    
    # Track recently viewed for authenticated users
    if request.user.is_authenticated:
        try:
            RecentlyViewed.objects.update_or_create(
                user=request.user,
                product=product
            )
        except:
            # RecentlyViewed table doesn't exist yet, skip tracking
            pass
    
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count,
        'user_has_reviewed': user_has_reviewed,
        'like_count': like_count,
        'is_liked': is_liked,
        'store': store,
        'shop_reviews': shop_reviews,
    })
