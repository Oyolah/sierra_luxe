from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Category, Product

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
            products_data.append({
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'price': str(product.price),
                'discount_price': str(product.discount_price) if product.discount_price else None,
                'description': product.description[:80],
                'image': product.main_image if product.main_image else None,
            })
        return JsonResponse({
            'products': products_data,
            'count': products.count()
        })
    
    return render(request, 'catalog/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    return render(request, 'catalog/product_detail.html', {'product': product, 'related_products': related_products})
