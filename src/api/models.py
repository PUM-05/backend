from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                               related_name='children', parent_link=True)

    def save(self, *args, **kwargs):
        if self.level == 0:
            self.level = 1
            p = self.parent
            while p:
                p = p.parent
                self.level = self.level + 1
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id', 'level']


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
