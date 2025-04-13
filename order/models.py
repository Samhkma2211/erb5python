from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from django.utils import timezone 
from shop.models import Category, Product, Cart, CartItem

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='processing', choices=[
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ])

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name if self.product else '[deleted]'} in Order #{self.order.id}"
