
from typing import Any
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from . import models
from django.db.models import Avg
from django.db.models.query import QuerySet, Q
from django.utils import timezone
from django.views import generic
from django.urls import reverse


def index(request: HttpRequest) -> HttpResponse:
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1
    context = {
    'num_visits': num_visits,
}
    return render(request, "autoservice/index.html", context)

class UserServiceListView(LoginRequiredMixin, generic.ListView):
    model = models.ServiceOrder
    template_name = "autoservice/user_service_list.html"
    paginate_by = 1

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        queryset = queryset.filter(client=self.request.user, client__isnull=False)
        return queryset


class BrandListView(generic.ListView):
    template_name = "autoservice/brand_list.html"
    context_object_name = "brands"
    def get_queryset(self):
        all_brands = models.CarModel.objects.values_list('make', flat=True)
        unique_brands = list(set(brand.capitalize() for brand in all_brands))
        unique_brands.sort()
        return unique_brands


class OrderListView(generic.ListView):
    template_name = "autoservice/order_list.html"
    context_object_name = "orders"
    model = models.OrderLine

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["search"] = True
        return context
    
    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        query = self.request.GET.get("query")
        if query:
            queryset = queryset.filter(
            Q(order__car__customer__icontains=query) |
            Q(order__car__plate__icontains=query) |
            Q(order__service__name__icontains=query) |
            Q(order__date__icontains=query) 
            )
        return queryset


class ServiceListView(generic.ListView):
    template_name = "autoservice/service_list.html"
    model = models.Services
    paginate_by = 1



class ServiceDetailView(generic.edit.FormMixin, generic.DetailView):
    model = models.Services
    template_name = "autoservice/service_detail.html"

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial["service"] = self.get_object()
        initial["reviewer"] = self.request.user
        return initial
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["reviews"] = self.object.reviews.all()
        return context
    
    def post(self, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        form.instance.service = self.object
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, "Thank you for your review!")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse("service_detail", kwargs={"pk": self.object.pk})


def info(request):
    current_year = timezone.now().year
    context = {
        'brands': models.CarModel.objects.values_list('make', flat=True).distinct(),
        'num_orders': models.ServiceOrder.objects.count(),
        'cars_average_age': current_year - models.CarModel.objects.aggregate(Avg('year'))['year__avg'],
        'average_service_price': models.OrderLine.objects.aggregate(Avg('price'))['price__avg'],
    }

    return render(request, "autoservice/info.html", context)

def contact_us(request):
    return render(request, "autoservice/contact.html")

# def services(request):

