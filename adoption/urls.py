from django.urls import path, include  # Make sure include is imported here
from . import views

app_name = 'adoption'

urlpatterns = [
    path('', views.dog_list, name='dog_list'),
    path('dog/<int:dog_id>/', views.dog_detail, name='dog_detail'),
    path('dog/<int:dog_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.adop_search, name='adop_search'),
]