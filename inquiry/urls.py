from django.urls import path
from . import views

urlpatterns = [
    path('inquiry/', views.create_inquiry, name='inquiry'),
]