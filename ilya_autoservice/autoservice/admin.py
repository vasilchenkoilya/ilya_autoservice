from django.contrib import admin
from . import models


class CarModelAdmin(admin.ModelAdmin):
    list_display = ("make", "model", "year")
    search_fields = ("make", "model")
    list_filter = ("make", "model", "year")


class PartServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "part_id",  "price")
    search_fields = ("name",)
    list_filter = ("name",)


class CarAdmin(admin.ModelAdmin):
    list_display = ("customer", "plate", "vin", "color")
    search_fields = ("customer", "plate", "vin")
    list_filter = ("customer", "plate")


class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ("get_customer", "date", "status", "order_id")
    search_fields = ("car__customer", "date", "status")
    list_filter = ("date", "status")


    def get_customer(self, obj):
        return obj.car.customer
    get_customer.short_description = "Customer"


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ("order", "get_order_id", "get_part_name", "quantity", "price")
    search_fields = ("order","order__order_id" "part_service", "quantity")
    list_filter = ("order__status",)

    def get_part_name(self, obj):
        return obj.part_service.name
    get_part_name.short_description = "Part name"

    def get_order_id(self, obj):
        return obj.order.order_id
    get_order_id.short_description = "Order id"

admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.PartService, PartServiceAdmin)
admin.site.register(models.ServiceOrder, ServiceOrderAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)

