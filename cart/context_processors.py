from .cart import Cart

def cart_item_count(request):
    cart = Cart(request)
    return {'cart_item_count': sum(item['quantity'] for item in cart.cart.values())}
