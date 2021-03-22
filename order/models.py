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
    order_number = models.CharField(max_length=45, null=True)
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('user.Address', on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL,null=True)
    order_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'


class Cart(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.SET_NULL, null=True, default=1)
    quantity = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    #기존에는 auto_now_add를 했지만 이번에는 auto_now로
    created_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey('Order', on_delete = models.SET_NULL, null=True)

    class Meta:
        db_table = 'carts'


    