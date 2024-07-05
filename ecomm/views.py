# ecomm/views.py

from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'ecomm_home.html')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'ecomm_product_list.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'ecomm_product_detail.html', {'product': product})

def cart(request):
    return render(request, 'ecomm_cart.html')

def checkout(request):
    return render(request, 'ecomm_checkout.html')