from django.shortcuts import render
from products.models import Product
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
# Create your views here.


def cart_detail(request):
    cart = Cart(request)
    total_price = cart.get_total_price()
    in_ksh = total_price*129
    return render(request, 'cart/card_detail.html', {'cart': cart,'tp_in_ksh':f'{round(in_ksh,2):,}'})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product)
    return redirect('products_list')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.remove(product)
    return redirect('cart_detail')