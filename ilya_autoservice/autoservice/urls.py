from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('contact/', views.contact_us, name='contact_us'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('orderlist/', views.OrderListView.as_view(), name='orders'),
    path('service/<int:pk>/', views.ServiceDetailView.as_view(), name='service_detail'),
    path('services/my/', views.UserServiceListView.as_view(), name='user_service'),
]