from django.db import models


class Category(models.Model):
    name = models.CharField()


class Customer(models.Model):
    phone = models.CharField()
    email = models.CharField()


class Case(models.Model):
    notes = models.CharField()
    medium = models.CharField(max_length=50)
    customer_time = models.DurationField()
    additional_time = models.DurationField()
    form_fill_time = models.DurationField()
    created_at = models.DateTimeField()
    edited_at = models.DateTimeField()

    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL)
