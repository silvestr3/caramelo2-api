from django.utils import timezone
from django.db import models

class Customer(models.Model):
    GENDERS = [
            ("ML", "Male"),
            ("FL", "Female"),
            ("OT", "Other")
        ]
    
    name = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=13)
    age = models.IntegerField()
    dob = models.DateField(auto_now_add=False, null=True)

    address = models.CharField(max_length=200)
    district = models.CharField(max_length=200, null=True)
    subdistrict = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    
    gender = models.CharField(
        max_length=2,
        choices=GENDERS
    )
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.name
    
    def is_birthday_today(self):
        if self.dob is not None:
            return self.dob.day == timezone.now().day and self.dob.month == timezone.now().month
        else:
            return False