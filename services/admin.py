from django.contrib import admin
from .models import Service

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'veterinary', 'pet_grooming', 'pet_boarding', 'emergency_service', 'in_service')
    list_filter = ('district', 'veterinary', 'pet_grooming', 'pet_boarding', 'emergency_service', 'in_service')
    search_fields = ('name', 'address', 'district', 'description')
    list_editable = ('veterinary', 'pet_grooming', 'pet_boarding', 'emergency_service', 'in_service')
    prepopulated_fields = {}
    ordering = ('name',)
    readonly_fields = ('created', 'updated')
    list_per_page = 20
    date_hierarchy = 'created'
    

