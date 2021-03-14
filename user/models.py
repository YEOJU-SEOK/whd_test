from django.db import models

class Gender(models.Model):
    name = models.CharField(max_length=5)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genders'

class User(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=256)
    number = models.CharField(max_length=11, unique=True)
    gender = models.ForeignKey('Gender', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Address(models.Model):
    user = models.ManyToManyField(User)
    address = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'

