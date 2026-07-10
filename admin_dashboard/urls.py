from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:product_id>/images/', views.product_images, name='product_images'),
    path('products/bulk-delete/', views.product_bulk_delete, name='product_bulk_delete'),
    path('featured/', views.featured_products, name='featured_products'),
    path('featured/<int:product_id>/add/', views.add_featured, name='add_featured'),
    path('featured/<int:product_id>/remove/', views.remove_featured, name='remove_featured'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:category_id>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:category_id>/delete/', views.category_delete, name='category_delete'),
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<int:order_id>/status/', views.order_status_update, name='order_status_update'),
    path('reviews/', views.review_list, name='review_list'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/<int:review_id>/approve/', views.review_approve, name='review_approve'),
    path('reviews/<int:review_id>/reject/', views.review_reject, name='review_reject'),
    path('reviews/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('reviews/bulk-action/', views.review_bulk_action, name='review_bulk_action'),
    path('likes/', views.like_list, name='like_list'),
    path('likes/<int:like_id>/delete/', views.like_delete, name='like_delete'),
    path('likes/bulk-delete/', views.like_bulk_delete, name='like_bulk_delete'),
]
