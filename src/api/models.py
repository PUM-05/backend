from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Customer(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()


class Case(models.Model):
    notes = models.TextField()
    medium = models.CharField(max_length=50)
    customer_time = models.DurationField()
    additional_time = models.DurationField()
    form_fill_time = models.DurationField()
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(User)
