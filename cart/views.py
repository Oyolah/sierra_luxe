from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from decimal import Decimal
from .models import Cart, CartItem
from catalog.models import Product

@login_required
def cart_view(request):
    """Display the shopping cart"""
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = cart.items.select_related('product').filter(saved_for_later=False)
    saved_items = cart.items.select_related('product').filter(saved_for_later=True)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'saved_items': saved_items,
        'subtotal': cart.get_total(),
        'shipping': Decimal('7.95'),  # Fixed shipping cost
        'total': cart.get_total() + Decimal('7.95'),
        'currency_symbol': '€',
    }
    return render(request, 'cart/cart.html', context)

@login_required
@require_POST
def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size', '')
    color = request.POST.get('color', '')
    
    # Validate size and color if product has options
    if product.sizes and not size:
        messages.error(request, 'Please select a size.')
        return redirect('catalog:product_detail', slug=product.slug)
    
    if product.colors and not color:
        messages.error(request, 'Please select a color.')
        return redirect('catalog:product_detail', slug=product.slug)
    
    # Get or create cart
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    # Check if item already exists in cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
        defaults={'quantity': quantity}
    )
    
    if not item_created:
        # Item exists, update quantity
        cart_item.quantity += quantity
        cart_item.save()
        message = f'Updated {product.name} quantity in cart.'
    else:
        message = f'Added {product.name} to cart.'
    
    messages.success(request, message)
    
    # Handle image URL
    image_url = ''
    if product.main_image:
        if hasattr(product.main_image, 'url'):
            image_url = product.main_image.url
        else:
            image_url = str(product.main_image)
    
    # Always return JSON for better UX
    return JsonResponse({
        'success': True,
        'cart_count': cart.get_item_count(),
        'message': message,
        'product_name': product.name,
        'product_image': image_url,
        'cart_total': float(cart.get_total())
    })

@login_required
@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, 'Cart updated successfully.')
    else:
        cart_item.delete()
        messages.success(request, 'Item removed from cart.')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = cart_item.cart if quantity > 0 else Cart.objects.get(customer=request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'subtotal': float(cart_item.get_subtotal()) if quantity > 0 else 0,
            'cart_total': float(cart.get_total()),
            'total': float(cart.get_total() + Decimal('7.95'))
        })
    
    return redirect('cart:cart_view')

@login_required
@require_POST
def remove_cart_item(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    messages.success(request, f'Removed {product_name} from cart.')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = Cart.objects.get(customer=request.user)
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'total': float(cart.get_total() + Decimal('7.95'))
        })
    
    return redirect('cart:cart_view')

def cart_preview(request):
    """Get cart items for dropdown preview"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': True,
            'items': [],
            'cart_count': 0,
            'cart_total': 0.0,
            'currency_symbol': '€'
        })
    
    try:
        cart, created = Cart.objects.get_or_create(customer=request.user)
        cart_items = cart.items.select_related('product').filter(saved_for_later=False)[:5]  # Show max 5 active items
        
        items_data = []
        for item in cart_items:
            # Handle both URL and path for images
            image_url = ''
            if item.product.main_image:
                if hasattr(item.product.main_image, 'url'):
                    image_url = item.product.main_image.url
                else:
                    image_url = str(item.product.main_image)
            
            items_data.append({
                'id': item.id,
                'product_name': item.product.name,
                'product_image': image_url,
                'product_slug': item.product.slug,
                'quantity': item.quantity,
                'size': item.size,
                'color': item.color,
                'subtotal': float(item.get_subtotal())
            })
        
        return JsonResponse({
            'success': True,
            'items': items_data,
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'currency_symbol': '€'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'items': [],
            'cart_count': 0,
            'cart_total': 0.0,
            'currency_symbol': '€'
        })

@login_required
@require_POST
def save_for_later(request, item_id):
    """Move an active cart item to saved for later"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.saved_for_later = True
    cart_item.save()
    
    cart = cart_item.cart
    messages.success(request, f'{cart_item.product.name} saved for later.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'total': float(cart.get_total() + Decimal('7.95'))
        })
    
    return redirect('cart:cart_view')

@login_required
@require_POST
def move_to_cart(request, item_id):
    """Move a saved for later item back to active cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    cart_item.saved_for_later = False
    cart_item.save()
    
    cart = cart_item.cart
    messages.success(request, f'{cart_item.product.name} moved to cart.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'cart_total': float(cart.get_total()),
            'total': float(cart.get_total() + Decimal('7.95'))
        })
    
    return redirect('cart:cart_view')

@login_required
@require_POST
def remove_saved_item(request, item_id):
    """Remove a saved for later item"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    
    cart = Cart.objects.get(customer=request.user)
    messages.success(request, f'Removed {product_name} from saved items.')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.get_item_count(),
            'saved_count': cart.get_saved_items().count()
        })
    
    return redirect('cart:cart_view')

@login_required
def checkout(request):
    """Checkout simulation (no real payment)"""
    cart = get_object_or_404(Cart, customer=request.user)
    
    if not cart.items.filter(saved_for_later=False).exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('catalog:product_list')
    
    if request.method == 'POST':
        # Simulate order creation
        from orders.models import Order, OrderItem
        
        # Create order with shipping information
        order = Order.objects.create(
            customer=request.user,
            total_amount=cart.get_total() + Decimal('7.95'),
            shipping_cost=Decimal('7.95'),
            status='pending',
            shipping_address=request.POST.get('address', ''),
            shipping_city=request.POST.get('city', ''),
            shipping_country=request.POST.get('country', ''),
            shipping_postal_code=request.POST.get('postal_code', ''),
            phone=request.POST.get('phone', ''),
            notes=request.POST.get('notes', '')
        )
        
        # Create order items from active cart items only
        active_items = cart.items.filter(saved_for_later=False)
        for cart_item in active_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                size=cart_item.size,
                color=cart_item.color,
                price=cart_item.product.get_price()
            )
        
        # Clear active cart items (keep saved for later)
        active_items.delete()
        
        messages.success(request, f'Order #{order.id} placed successfully! (Simulation)')
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').filter(saved_for_later=False),
        'subtotal': cart.get_total(),
        'shipping': Decimal('7.95'),
        'total': cart.get_total() + Decimal('7.95'),
        'currency_symbol': '€',
    }
    return render(request, 'cart/checkout.html', context)
