from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['id','user','phone','address','date_of_birth']
  list_display_links = ['id','user']
  list_filter = 'favorite_dog',
  filter_horizontal = 'favorite_dog',
  search_fields = ['favorite_dog__name']
  ordering = 'user',
  readonly_fields = ['user','created_at', 'updated_at']
  list_per_page = 20

