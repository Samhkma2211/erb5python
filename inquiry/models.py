from django.db import models
from django.utils import timezone
from django.core.validators import EmailValidator
from .choices import inquiry_choices

# Create your models here.

class Inquiry(models.Model):
    
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100, validators=[EmailValidator()])
    phone = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=timezone.now, blank=True)
    inquiry_type = models.CharField(max_length=200, choices=inquiry_choices.items(), default='General Inquiry')
    dog_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"