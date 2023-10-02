from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.db.models import Avg
from django.utils import timezone

def index(request):
    current_year = timezone.now().year
    context = {
        'brands': models.CarModel.objects.values_list('make', flat=True).distinct(),
        'num_orders': models.ServiceOrder.objects.count(),
        'cars_average_age': current_year - models.CarModel.objects.aggregate(Avg('year'))['year__avg'],
        'average_service_price': models.OrderLine.objects.aggregate(Avg('price'))['price__avg'],
    }
    return render(request, "autoservice/index.html", context)







