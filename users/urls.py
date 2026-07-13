from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('auth/', views.auth_page, name='auth'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('recently-viewed/', views.recently_viewed, name='recently_viewed'),
    # Customer Dashboard URLs
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer-dashboard/orders/', views.customer_orders, name='customer_orders'),
    path('customer-dashboard/orders/<int:order_id>/', views.customer_order_detail, name='customer_order_detail'),
    path('customer-dashboard/wishlist/', views.customer_wishlist, name='customer_wishlist'),
    path('customer-dashboard/reviews/', views.customer_reviews, name='customer_reviews'),
    path('customer-dashboard/billing-address/', views.customer_billing_address, name='customer_billing_address'),
    path('customer-dashboard/billing-address/edit/', views.customer_billing_address_edit, name='customer_billing_address_edit'),
    path('customer-dashboard/change-password/', views.customer_change_password, name='customer_change_password'),
]
