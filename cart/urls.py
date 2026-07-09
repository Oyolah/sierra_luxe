from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('preview/', views.cart_preview, name='cart_preview'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('save-for-later/<int:item_id>/', views.save_for_later, name='save_for_later'),
    path('move-to-cart/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
    path('remove-saved/<int:item_id>/', views.remove_saved_item, name='remove_saved_item'),
    path('checkout/', views.checkout, name='checkout'),
]
