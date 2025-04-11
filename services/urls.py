from django.urls import path
from . import views

app_name = 'services'  # This sets the app namespace

urlpatterns = [
    path('', views.services, name='services'), 
    path('<int:service_id>/', views.service_detail, name='service_detail'),
    path('search/', views.serv_search, name='serv_search'),
]
