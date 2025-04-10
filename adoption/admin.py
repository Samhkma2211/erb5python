from django.contrib import admin
from .models import Dog

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'dateofbirth', 'gender','size', 'dogtype', 'available', 'created', 'updated']
    list_filter = ['dogtype', 'size', 'dateofbirth', 'gender','available', 'created']
    list_editable = ['available']
    search_fields = ['name', 'dogtype', 'dateofbirth', 'gender','description']
    list_per_page = 25
    ordering = ['id']