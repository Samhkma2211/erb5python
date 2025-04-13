from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['user', 'cart', 'total', 'created_at']
    
    def has_add_permission(self, request):
        return False  # Prevent manual order creation in admin

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'subtotal']
    list_filter = ['order__status']
    
    def subtotal(self, obj):
        return obj.quantity * obj.price
    subtotal.short_description = 'Subtotal'


