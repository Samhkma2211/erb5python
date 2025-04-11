from django.shortcuts import render, get_object_or_404
from .models import Service
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .choices import district_choices

# Create your views here.
def services(request):    
    return render(request, 'services/services.html')

def service_detail(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    context = {'service': service}
    return render(request, 'services/service_detail.html', context)
    
def serv_search(request):
    queryset_list = Service.objects.order_by('name').filter(in_service=True)
    
    # Get search parameters from request.GET first
    filters = {
        'district' : request.GET.get('district', ''),   
        'veterinary' : 'veterinary' in request.GET,
        'pet_grooming' : 'pet_grooming' in request.GET,
        'pet_boarding' : 'pet_boarding' in request.GET,
        'emergency_service': 'emergency_service' in request.GET,
    }
    
    if filters['district']:
        queryset_list = queryset_list.filter(district__iexact=filters['district'])
    if filters['veterinary']:
        queryset_list = queryset_list.filter(veterinary=True)
    if filters['pet_grooming']:
        queryset_list = queryset_list.filter(pet_grooming=True)
    if filters['pet_boarding']:
        queryset_list = queryset_list.filter(pet_boarding=True)
    if filters['emergency_service']:
        queryset_list = queryset_list.filter(emergency_service=True)
    
    #user input keyword to search
    search_query = request.GET.get('search', '')
    if search_query:
        queryset_list = queryset_list.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(district__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    #results = queryset_list.count()    
    paginator = Paginator(queryset_list, 3)
    page = request.GET.get('page')
    paged_services = paginator.get_page(page)
    values = request.GET.copy()  # Preserve search parameters
    if 'page' in values:
        del values["page"]

    context = {
        'services': paged_services,
        'district_choices': district_choices,
        'values' : values,
        'search_query': search_query,
        #'results': results,
        }

    return render(request, 'services/search.html', context)