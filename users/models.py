from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField
from catalog.models import Product

class User(AbstractUser):
    ROLE_CHOICES = (
        ('CUSTOMER', 'Customer'),
        ('STAFF', 'Staff'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    staff_role = models.ForeignKey(
        'admin_dashboard.Role',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_users',
        help_text='Role assigned to staff users'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_account_type(self):
        """Return account type: SuperAdmin, Staff, or Customer"""
        if self.is_superuser:
            return 'SuperAdmin'
        elif self.is_staff:
            return 'Staff'
        else:
            return 'Customer'
    
    def has_dashboard_permission(self, permission_code):
        """Check if user has a specific dashboard permission"""
        if self.is_superuser:
            return True
        if not self.is_staff or not self.staff_role:
            return False
        return self.staff_role.permissions.filter(code=permission_code).exists()
    
    def get_dashboard_permissions(self):
        """Return list of dashboard permission codes for this user"""
        if self.is_superuser:
            from admin_dashboard.models import DASHBOARD_PERMISSIONS
            return [code for code, _, _ in DASHBOARD_PERMISSIONS]
        if not self.is_staff or not self.staff_role:
            return []
        return self.staff_role.get_permission_codes()
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class BillingAddress(models.Model):
    """Customer billing address information"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='billing_addresses')
    full_name = models.CharField(max_length=200)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.country}"
    
    def save(self, *args, **kwargs):
        # Ensure only one default address per user
        if self.is_default:
            BillingAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'
        ordering = ['-is_default', '-created_at']

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='viewed_by')
    viewed_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Recently Viewed'
        verbose_name_plural = 'Recently Viewed'
        unique_together = ('user', 'product')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"
