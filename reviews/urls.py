from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('product/<int:product_id>/', views.product_reviews_api, name='product_reviews'),
    path('product/<int:product_id>/add/', views.add_review, name='add_review'),
]
