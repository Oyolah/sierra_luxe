from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Dashboard permission constants - organized by module with categories
DASHBOARD_PERMISSIONS = [
    # Dashboard
    ('view_dashboard', 'View Dashboard', 'Dashboard'),
    
    # Products
    ('view_products', 'View Products', 'Products'),
    ('add_products', 'Add Products', 'Products'),
    ('edit_products', 'Edit Products', 'Products'),
    ('delete_products', 'Delete Products', 'Products'),
    ('manage_featured', 'Manage Featured Products', 'Products'),
    
    # Categories
    ('view_categories', 'View Categories', 'Categories'),
    ('add_categories', 'Add Categories', 'Categories'),
    ('edit_categories', 'Edit Categories', 'Categories'),
    ('delete_categories', 'Delete Categories', 'Categories'),
    
    # Orders
    ('view_orders', 'View Orders', 'Orders'),
    ('edit_orders', 'Edit Orders', 'Orders'),
    ('delete_orders', 'Delete Orders', 'Orders'),
    ('update_order_status', 'Update Order Status', 'Orders'),
    
    # Reviews
    ('view_reviews', 'View Reviews', 'Reviews'),
    ('edit_reviews', 'Edit Reviews', 'Reviews'),
    ('delete_reviews', 'Delete Reviews', 'Reviews'),
    ('approve_reviews', 'Approve Reviews', 'Reviews'),
    
    # Likes
    ('view_likes', 'View Likes', 'Likes'),
    ('delete_likes', 'Delete Likes', 'Likes'),
    
    # Users
    ('view_users', 'View Users', 'Users'),
    ('add_staff', 'Add Staff', 'Users'),
    ('edit_staff', 'Edit Staff', 'Users'),
    ('delete_staff', 'Delete Staff', 'Users'),
    ('activate_users', 'Activate/Deactivate Users', 'Users'),
    
    # Roles & Permissions
    ('view_roles', 'View Roles', 'Roles & Permissions'),
    ('add_roles', 'Add Roles', 'Roles & Permissions'),
    ('edit_roles', 'Edit Roles', 'Roles & Permissions'),
    ('delete_roles', 'Delete Roles', 'Roles & Permissions'),
    ('manage_role_permissions', 'Manage Role Permissions', 'Roles & Permissions'),
]

# Helper function to get permissions grouped by category
def get_permissions_by_category():
    """Return permissions grouped by category from database"""
    grouped = {}
    # Get permissions from database to ensure they exist
    db_permissions = RolePermission.objects.all()
    
    if db_permissions.exists():
        # Use database permissions if they exist
        for perm in db_permissions:
            if perm.category not in grouped:
                grouped[perm.category] = []
            grouped[perm.category].append((perm.code, perm.name))
    else:
        # Fallback to constant if database is empty (shouldn't happen after seeding)
        for code, name, category in DASHBOARD_PERMISSIONS:
            if category not in grouped:
                grouped[category] = []
            grouped[category].append((code, name))
    
    return grouped

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
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default='General')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'code']
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
    
    def __str__(self):
        return self.name
