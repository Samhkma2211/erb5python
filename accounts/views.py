from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth.models import User
from order.models import Order
from shop.views import restore_stock_quantities
from adoption.models import Dog
from .models import Profile

# Create your views here.
def register(request):
  if request.method == 'POST':
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']
    if password == password2:
      if User.objects.filter(username=username).exists():
        messages.error(request,"Username already exists!")
        return redirect('login')
      else:
        if User.objects.filter(email=email).exists():
          messages.error(request,"Email already exist!")
          return redirect('login')
        else:
          user = User.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name)
          user.save()
          profile = Profile.objects.create(user=user)
          profile.save()
          messages.success(request,"You are now registered and can log in!")
          return redirect('login')
    else:
      messages.error(request,"Password do not match!")
      return redirect('login')
  else:
    return render(request,'accounts/login.html')


def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username,password=password)
    if user is not None:
      auth.login(request,user)
      next_url = request.POST.get('next', 'index')
      return redirect(next_url)
    else:
      messages.error(request,"Username or password incorrect!")
      return redirect('login')
  else:
    return render(request,'accounts/login.html')

def logout(request):
  if request.method == 'POST':
    # Restore stock quantities from cart before logout
    cart = request.session.get('cart', {})
    if cart:
        restore_stock_quantities(cart)
    
    # Clear the cart
    request.session['cart'] = {}
    
    auth.logout(request)
  return redirect ('index')

def profile(request):
  pass

def dashboard(request):
  if request.user.is_authenticated:
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    profile = request.user.profile
    fav_dogs = profile.favorite_dog.all()
    user_info = {
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'date_joined': request.user.date_joined
    }
    context = {'orders':orders,
              'fav_dogs':fav_dogs,
              'user_info':user_info}
    return render(request, 'accounts/dashboard.html',context)
  else:
    return redirect('index')