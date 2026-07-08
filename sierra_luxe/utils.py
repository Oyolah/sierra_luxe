# Shared utility functions for Sierra Luxe

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_order_number():
    """Generate unique order number"""
    import uuid
    return f"SL-{uuid.uuid4().hex[:8].upper()}"

def format_price(price):
    """Format price to currency format"""
    return f"${price:.2f}"

def calculate_discount_percentage(original_price, discount_price):
    """Calculate discount percentage"""
    if discount_price and original_price > discount_price:
        return int(((original_price - discount_price) / original_price) * 100)
    return 0
