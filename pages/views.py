from django.shortcuts import render
from adoption.models import Dog
from shop.models import Product
import random
# Create your views here.

def index(request):
    dogs = list(Dog.objects.filter(available=True))
    if len(dogs) > 4:
      dogs = random.sample(dogs, 4)
    products = list(Product.objects.filter(available=True))
    if len(products) > 3:
      products = random.sample(products, 3)
    context = {
      'dogs': dogs,
      'products':products,
    }
    return render(request, 'pages/index.html',context)

def about(request):
  return render(request, 'pages/about.html')

def faq (request):
  return render(request, 'pages/faq.html')  