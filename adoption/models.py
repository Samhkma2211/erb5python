from django.db import models
from django.utils import timezone
from datetime import datetime
from .choices import gender_choices, size_choices, dogtype_choices

class Dog(models.Model):
    name = models.CharField(max_length=200)
    dateofbirth = models.DateField(default=timezone.now, blank=True)
    gender = models.CharField(max_length=10, choices=gender_choices.items(), blank=True)
    size = models.CharField(max_length=20, choices=size_choices.items())
    dogtype = models.CharField(max_length=50, choices=dogtype_choices.items())
    description = models.TextField(blank=True)
    mircochip_no = models.CharField(max_length=100, blank=True)  # Added blank=True
    desexed = models.BooleanField(default=False)
    medical_history = models.TextField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now, blank=True)  # Changed from datetime.now
    updated = models.DateTimeField(default=timezone.now, blank=True)  # Changed from datetime.now
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    class Meta:
        ordering = ['-created']  # Shows newest dogs first
        verbose_name = 'Dog'
        verbose_name_plural = 'Dogs'

    def __str__(self):
        return self.name
