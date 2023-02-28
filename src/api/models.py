from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Customer(models.Model):
    phone = models.CharField(max_length=20)
    email = models.EmailField()


class Case(models.Model):
    notes = models.TextField(null=True)
    medium = models.CharField(max_length=50, null=True)
    customer_time = models.DurationField(null=True)
    additional_time = models.DurationField(null=True)
    form_fill_time = models.DurationField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    user = models.ManyToManyField(User)
