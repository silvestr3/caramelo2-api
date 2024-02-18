from django.db import models
from .Customer import Customer
from .Bike import Bike
from .AdditionalFee import AdditionalFee
from .User import User

class Order(models.Model):
    STATUS = [
            ('CPL', 'Complete'),
            ('IPL', 'Incomplete'),
        ]
    
    sale_date = models.DateField(auto_now_add=False)
    seller = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    bikes = models.ManyToManyField(Bike)
    
    total_price = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    down_payment = models.FloatField(default=0, null=True)
    additional_fees = models.ManyToManyField(AdditionalFee, blank=True)

    commission = models.FloatField(default=0, null=True, blank=True)
    total = models.FloatField(default=0, null=True)

    payment_method = models.CharField(max_length=50)
    notes = models.TextField(null=True, blank=True)
    registration_status = models.CharField(
        max_length=3,
        choices=STATUS
    )
    has_checkout = models.BooleanField(default=False)