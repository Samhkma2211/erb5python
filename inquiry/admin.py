from django.contrib import admin
from .models import Inquiry

class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'inquiry_type', 'dog_id', 'name', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    list_filter = 'inquiry_type',
    search_fields = ('name', 'email', 'dog_id')
    readonly_fields = ('contact_date', 'user_id')
    list_per_page = 25

admin.site.register(Inquiry, InquiryAdmin)