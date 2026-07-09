from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product, Store
from users.models import RecentlyViewed


def get_product_rating_data(product):
    """Get average rating and review count for a product"""
    reviews = product.reviews.filter(is_approved=True)
    count = reviews.count()
    if count > 0:
        average = sum(r.rating for r in reviews) / count
    else:
        average = 0
    return round(average, 1), count

def home(request):
    return render(request, 'catalog/home.html')

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
            avg, count = get_product_rating_data(product)
            products_data.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'price': str(product.price),
                'discount_price': str(product.discount_price) if product.discount_price else None,
                'description': product.description[:80],
                'image': product.main_image if product.main_image else None,
                'average_rating': avg,
                'review_count': count,
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
    store, _ = Store.objects.get_or_create(
        name='Sierra Luxe',
        defaults={
            'smooth_shipping': True,
            'speedy_replies': True,
            'average_rating': 4.8,
            'total_reviews': 0
        }
    )
    
    # Get review and rating data
    reviews = product.reviews.filter(is_approved=True).select_related('customer')
    average_rating, review_count = get_product_rating_data(product)
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = product.reviews.filter(customer=request.user).exists()
    
    # Get shop-wide reviews
    from reviews.models import Review
    shop_reviews = Review.objects.filter(is_approved=True).select_related('customer', 'product').order_by('-created_at')[:10]
    
    # Track recently viewed for authenticated users
    if request.user.is_authenticated:
        RecentlyViewed.objects.update_or_create(
            user=request.user,
            product=product
        )
    
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_count': review_count,
        'user_has_reviewed': user_has_reviewed,
        'store': store,
        'shop_reviews': shop_reviews,
    })
