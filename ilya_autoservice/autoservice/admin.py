from django.contrib import admin
from . import models


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year')
    search_fields = ('make', 'model')
    list_filter = ('make', 'model', 'year')
    ordering = ('-make', '-model', '-year')


class CarAdmin(admin.ModelAdmin):
    list_display = ('customer', 'plate', 'vin', 'color')
    search_fields = ('customer', 'plate', 'vin', 'color')
    list_filter = ('customer', 'plate', 'vin', 'color')
    list_display_links = ('car_model', 'customer', 'plate')
    ordering = ('-customer', '-car_model', '-plate')

class PartServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('-name',)


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ('car', 'date', 'status')
    search_fields = ('car', 'date', 'status')
    list_filter = ('car', 'date', 'status')
    ordering = ('-date',)

class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'part_service', 'quantity', 'price')
    search_fields = ('order', 'part_service', 'quantity', 'price')
    list_filter = ('order', 'part_service', 'quantity', 'price')
    ordering = ('-order',)


admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.PartService, PartServiceAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)