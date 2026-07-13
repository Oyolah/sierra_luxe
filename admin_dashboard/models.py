from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Dashboard permission constants - organized by module
DASHBOARD_PERMISSIONS = [
    # Dashboard
    ('view_dashboard', 'View Dashboard'),
    
    # Products
    ('view_products', 'View Products'),
    ('add_products', 'Add Products'),
    ('edit_products', 'Edit Products'),
    ('delete_products', 'Delete Products'),
    ('manage_featured', 'Manage Featured Products'),
    
    # Categories
    ('view_categories', 'View Categories'),
    ('add_categories', 'Add Categories'),
    ('edit_categories', 'Edit Categories'),
    ('delete_categories', 'Delete Categories'),
    
    # Orders
    ('view_orders', 'View Orders'),
    ('edit_orders', 'Edit Orders'),
    ('delete_orders', 'Delete Orders'),
    ('update_order_status', 'Update Order Status'),
    
    # Reviews
    ('view_reviews', 'View Reviews'),
    ('edit_reviews', 'Edit Reviews'),
    ('delete_reviews', 'Delete Reviews'),
    ('approve_reviews', 'Approve Reviews'),
    
    # Likes
    ('view_likes', 'View Likes'),
    ('delete_likes', 'Delete Likes'),
    
    # Users
    ('view_users', 'View Users'),
    ('add_staff', 'Add Staff'),
    ('edit_staff', 'Edit Staff'),
    ('delete_staff', 'Delete Staff'),
    ('activate_users', 'Activate/Deactivate Users'),
    
    # Roles
    ('view_roles', 'View Roles'),
    ('add_roles', 'Add Roles'),
    ('edit_roles', 'Edit Roles'),
    ('delete_roles', 'Delete Roles'),
    ('manage_role_permissions', 'Manage Role Permissions'),
]

class Role(models.Model):
    """Role model for staff users"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField('RolePermission', blank=True, related_name='roles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.name
    
    def get_permission_codes(self):
        """Return list of permission codes for this role"""
        return list(self.permissions.values_list('code', flat=True))
    
    def user_count(self):
        """Return count of users with this role"""
        return User.objects.filter(staff_role=self).count()

class RolePermission(models.Model):
    """Custom dashboard permissions"""
    code = models.CharField(max_length=50, unique=True, choices=DASHBOARD_PERMISSIONS)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['code']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
    
    def __str__(self):
        return self.name
