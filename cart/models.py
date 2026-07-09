from django.db import models
from django.conf import settings
from catalog.models import Product

class Cart(models.Model):
    customer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.filter(saved_for_later=False))
    
    def get_item_count(self):
        return sum(item.quantity for item in self.items.filter(saved_for_later=False))
    
    def get_saved_items(self):
        return self.items.filter(saved_for_later=True)
    
    def __str__(self):
        return f"Cart of {self.customer.username}"
    
    class Meta:
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    saved_for_later = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_subtotal(self):
        return self.product.get_price() * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart.customer.username}'s cart"
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ('cart', 'product', 'size', 'color')
