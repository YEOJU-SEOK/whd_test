from django.db import models
from user.models import User, Address
from product.models import Product


class Payment(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'payments'


class Order(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    addredss = models.ForeignKey('user.Address', on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,null=True)
    prder_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
