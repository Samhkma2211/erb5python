from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Product listing URLs
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/update/<str:action>/', views.update_quantity, name='update_quantity'),

    # Cart functionality URLs
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
]