from django.db import models
from datetime import datetime, timedelta

def get_deadline():
    return datetime.today() + timedelta(7)


class Product(models.Model):
    name = models.CharField(max_length=50)
    manufacture = models.CharField(max_length=20)
    unit_price = models.DecimalField(decimal_places=3, max_digits=8)
    stock = models.IntegerField()
    expiration_date = models.DateField(null=True, default=get_deadline)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'


