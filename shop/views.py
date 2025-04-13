from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem
from decimal import Decimal
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    else:
        current_category = None
    
    return render(request, 'shop/product_list.html', {
        'categories': categories,
        'current_category': current_category,
        'products': products,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    current_quantity = request.session.get(f'product_{product_id}_quantity', 1)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'current_quantity': current_quantity
    })

def restore_stock_quantities(cart_session):
    """Restore product stock quantities from cart items"""
    if not cart_session:
        return
    
    for product_id, item in cart_session.items():
        try:
            product = Product.objects.get(id=product_id)
            product.stock += item['quantity']
            product.save()
        except Product.DoesNotExist:
            continue
        
def handle_cart_item(request, product_id, quantity_change=0):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    product_key = str(product_id)
    
    if product_key not in cart:
        cart[product_key] = {'quantity': 0}
    
    # Add stock validation
    new_quantity = cart[product_key]['quantity'] + quantity_change
    if new_quantity > product.stock:
        messages.warning(request, f"Only {product.stock} items available!")
        return product
    
    # Update product stock
    product.stock -= quantity_change
    product.save()
    
    cart[product_key]['quantity'] = new_quantity
    
    if cart[product_key]['quantity'] < 1:
        del cart[product_key]
    
    request.session['cart'] = cart
    return product

def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = handle_cart_item(request, product_id, quantity)
        messages.success(request, f'{quantity} {product.name}(s) added to cart!', extra_tags="shop")
        return redirect('shop:cart')
    return redirect('shop:product_list')

def update_cart(request, item_id, action):
    quantity_change = 1 if action == 'increase' else -1
    handle_cart_item(request, item_id, quantity_change)
    return redirect('shop:cart')

def update_quantity(request, product_id, action):
    product = get_object_or_404(Product, id=product_id)
    session_key = f'product_{product_id}_quantity'
    current_quantity = request.session.get(session_key, 1)
    
    if action == 'increase' and current_quantity < product.stock:
        request.session[session_key] = current_quantity + 1
    elif action == 'decrease' and current_quantity > 1:
        request.session[session_key] = current_quantity - 1
    
    return redirect('shop:product_detail', product_id=product_id)

def get_cart_context(cart_session):
    product_ids = [int(id) for id in cart_session.keys()]
    products = Product.objects.filter(id__in=product_ids)
    
    # Create cart items with subtotal included
    cart_items = []
    for p in products:
        quantity = cart_session[str(p.id)]['quantity']
        cart_items.append({
            'product': p,
            'quantity': quantity,
            'subtotal': p.price * quantity  # Add subtotal calculation
        })
    
    subtotal = sum(item['subtotal'] for item in cart_items)
    total_quantity = sum(item['quantity'] for item in cart_items)
    shipping = 5 * total_quantity
    # shipping = Decimal('10.00')
    
    return {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': subtotal + shipping,
        'total_quantity':total_quantity
    }

def cart(request):
    return render(request, 'shop/cart.html', get_cart_context(request.session.get('cart', {})))

def clear_cart(request):
    """Clear cart and restore stock quantities"""
    cart = request.session.get('cart', {})
    if cart:
        restore_stock_quantities(cart)
        request.session['cart'] = {}
    return redirect('shop:cart')