from django.db import models
from django.conf import settings
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField(default=0)
    sizes = models.CharField(max_length=100, help_text='Comma-separated sizes (e.g., S,M,L,XL)')
    colors = models.CharField(max_length=100, help_text='Comma-separated colors')
    material = models.CharField(max_length=100, blank=True)
    care_instructions = models.TextField(blank=True)
    main_image = models.CharField(max_length=500, blank=True, null=True)
    video = models.CharField(max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price
    
    def get_discount_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def is_in_stock(self):
        return self.stock > 0
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.CharField(max_length=500)
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'
        ordering = ['-is_primary', 'created_at']


class Store(models.Model):
    """Store/shop model to track shop-wide metrics"""
    name = models.CharField(max_length=200, default='Sierra Luxe')
    description = models.TextField(blank=True)
    smooth_shipping = models.BooleanField(default=True, help_text='Has a history of shipping on time with tracking')
    speedy_replies = models.BooleanField(default=True, help_text='Has a history of replying to messages quickly')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=4.8, help_text='Average review rating')
    total_reviews = models.IntegerField(default=0, help_text='Total number of reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

