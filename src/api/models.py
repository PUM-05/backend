from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True,
                               related_name='children', parent_link=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        """
        Override save() to also set the correct value of level based on parent "depth"
        """
        if self.level == 0:
            self.level = 1
            p = self.parent
            while p:
                p = p.parent
                self.level = self.level + 1
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ['level']
        verbose_name_plural = "categories"


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

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "cases"
