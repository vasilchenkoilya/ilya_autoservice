from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
import uuid

# Create your models here.
class CarModel (models.Model):
    make = models.CharField(_("Brand"), max_length=100, db_index=True)
    model = models.CharField(_("model"), max_length=100, db_index=True)
    year = models.IntegerField(_("year",), db_index=True)

    class Meta:
        verbose_name = _("car model")
        verbose_name_plural = _("car models")
        ordering = ["-year", "-make", "-model"]

    def __str__(self):
        return f'{self.make} {self.model}, {self.year} year.'

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    


class PartService(models.Model):
    name = models.CharField(_("name"), max_length=100, db_index=True)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    part_id = models.UUIDField(_("part id"), db_index=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = _("part service")
        verbose_name_plural = _("part services")
        ordering = ["-name"]
    
    def __str__(self):
        return f'{self.name} - price: {self.price} EUR.'
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
    

class Car (models.Model):
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_("car model"),
        related_name="cars",
        on_delete=models.CASCADE
        )
    customer = models.CharField(_("customer"), max_length=50, db_index=True)
    plate = models.CharField(_("plate"), max_length=10, db_index=True)
    vin = models.CharField(_("vin"), max_length=17, db_index=True)
    color = models.CharField(_("color"), max_length=100, null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")
        ordering = ["-customer", "-car_model", "-plate"]

    def __str__(self):
        return f'{self.customer} - {self.car_model}, Plate: {self.plate}.'
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})

ORDER_STATUS = (
    (0, _('New')),
    (1, _('In progress')),
    (2, _('Completed')),
    (3, _('Canceled')),       
    )
class ServiceOrder(models.Model):
    car = models.ForeignKey(
        Car,
        verbose_name=_("car"),
        related_name="orders",
        on_delete=models.CASCADE
    )
    date = models.DateField(_("date"), auto_now_add=True)
    order_id = models.UUIDField(_("order id"), db_index=True, default=uuid.uuid4, editable=False)
    status = models.PositiveSmallIntegerField(
        _("status"), choices=ORDER_STATUS, default=0,
        )

    class Meta:
        verbose_name = _("service order")
        verbose_name_plural = _("service orders")
        ordering = ["-date"]
    
    def __str__(self):
        return f'{self.car} /// {self.date} /// Status: {self.get_status_display()}'
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class OrderLine(models.Model):
    order = models.ForeignKey(
        ServiceOrder,
        verbose_name=_("order"),
        related_name="orderlines",
        on_delete=models.CASCADE
    )
    part_service = models.ForeignKey(
        PartService,
        verbose_name=_("part service"),
        related_name="orderlines",
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(_("quantity"))
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("order line")
        verbose_name_plural = _("order lines")
        ordering = ["-order", "-part_service", "-quantity"]
    
    def __str__(self):
        return f'{self.order} /// {self.part_service} /// Quantity: {self.quantity} - Final price: {self.price} EUR'
    
    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


