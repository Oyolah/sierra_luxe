from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(customer=request.user).prefetch_related('items__product')
    return render(request, 'orders/order_history.html', {
        'orders': orders
    })
