# ecomm/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='ecomm_home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]