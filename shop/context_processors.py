from .views import get_cart_context

def cart_quantity(request):
    cart = request.session.get('cart', {})
    cart_context = get_cart_context(cart)
    return {
        'total_quantity': cart_context['total_quantity']
    } 