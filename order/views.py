from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Category, Product, Cart, CartItem
from shop.views import get_cart_context
from .models import Order, OrderItem
from decimal import Decimal
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def checkout(request):
    if not request.session.get('cart'):
        messages.warning(request, "Your cart is empty!")
        return redirect('shop:cart')
    
    cart_context = get_cart_context(request.session.get('cart', {}))
    
    # Create the order with all financial details
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        cart=request.user.cart if request.user.is_authenticated and hasattr(request.user, 'cart') else None,
        subtotal=cart_context['subtotal'],
        shipping=cart_context['shipping'],
        total=cart_context['total'],
        created_at=timezone.now(),
        status='processing'  
    )
    
    # Record all cart items as order items
    for item in cart_context['cart_items']:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price,
            subtotal=item['subtotal']
        )
    
    # Clear both session cart and database cart if authenticated
    request.session['cart'] = {}
    if request.user.is_authenticated and hasattr(request.user, 'cart'):
        request.user.cart.items.all().delete()
    
    messages.success(request, "Order placed successfully!")
    return redirect('order:order_confirmation', order_id=order.id)

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_confirmation.html', {'order': order})