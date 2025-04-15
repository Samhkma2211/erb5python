from django.shortcuts import render, get_object_or_404, redirect
from . models import Dog
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
from .choices import gender_choices, size_choices, dogtype_choices
from django.contrib import messages
from accounts.models import Profile

def dog_list(request):
    dogs = Dog.objects.filter(available=True)
    
    paginator = Paginator(dogs, 6)
    page = request.GET.get('page')
    paged_dogs = paginator.get_page(page)
    
    context = {
        'dogs': paged_dogs,
        'gender_choices': gender_choices,
        'size_choices': size_choices,
        'dogtype_choices': dogtype_choices,
        'values': {},
    }
    return render(request, 'adoption/dog_list.html', context)

def dog_detail(request, dog_id):
    dog_detail = get_object_or_404(Dog, pk=dog_id)
    is_favorite = False
    if request.user.is_authenticated:        
        favorite = dog_detail.userprofile.all() #find all user add this dog to favorite
        if request.user in favorite:
            is_favorite = True    
            
    context = {
        'dog_detail': dog_detail,
        'is_favorite': is_favorite,
    }
    return render(request, 'adoption/dog_detail.html', context)

def adop_search(request):
    queryset_list = Dog.objects.order_by('-created').filter(available=True)
    # In your search view, update the filter to use 'description' instead of 'dog_description'
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(Q(name__icontains=keywords) | 
                                            Q(description__icontains=keywords))
    if 'gender' in request.GET:
        gender = request.GET['gender']
        if gender:
            queryset_list = queryset_list.filter(gender__iexact=gender)
    if 'size' in request.GET:
        size = request.GET['size']
        if size:
            queryset_list = queryset_list.filter(size__iexact=size)
    if 'type' in request.GET:
        type = request.GET['type']
        if type:
            queryset_list = queryset_list.filter(dogtype__iexact=type)            

    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    paged_dogs = paginator.get_page(page)
    values = request.GET.copy()
    
    if 'page' in values:
        del values['page']

    context = {
        'gender_choices': gender_choices,
        'size_choices': size_choices,
        'dogtype_choices': dogtype_choices,  # Make sure this is included
        'dogs': paged_dogs,
        'values': values,
    }

    return render(request, 'adoption/search.html', context)

def toggle_favorite(request,dog_id):
    dog = get_object_or_404(Dog, id=dog_id)
    profile = request.user.profile
    if dog in profile.favorite_dog.all():
        profile.favorite_dog.remove(dog)
    else:
        profile.favorite_dog.add(dog)        
    return redirect('adoption:dog_detail', dog_id=dog.id)