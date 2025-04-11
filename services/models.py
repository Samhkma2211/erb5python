from django.db import models
from django.utils import timezone
from .choices import district_choices

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    district = models.CharField(max_length=50, choices=district_choices.items())
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    website = models.URLField(blank=True, null=True)
    veterinary = models.BooleanField(default=False)
    pet_grooming = models.BooleanField(default=False)
    pet_boarding = models.BooleanField(default=False)
    emergency_service = models.BooleanField(default=False)   
    created = models.DateTimeField(default=timezone.now, blank=True)
    updated = models.DateTimeField(auto_now=True)  # Changed to auto_now
    in_service = models.BooleanField(default=True)    
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
