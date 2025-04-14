from django.db import models
from django.contrib.auth.models import User
from adoption.models import Dog
from django.utils import timezone 

# Create your models here.

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  phone = models.CharField(max_length=20,blank=True)
  address = models.CharField(max_length=200,blank=True)
  date_of_birth = models.DateField(null=True,blank=True)
  favorite_dog = models.ManyToManyField(Dog,related_name="userprofile")  
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.username
