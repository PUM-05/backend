from typing import List
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy

from django.contrib.auth.forms import UserCreationForm

from api.models import Category


class CategoryCreationForm(forms.ModelForm):
    """
    Form for creating a new category in the admin panel.
    """
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(level=1))

    class Meta:
        model = Category
        fields = ('name', 'parent')


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin panel for categories.
    """
    list_display = ('name', 'parent')
    form = CategoryCreationForm


admin.site.register(Category, CategoryAdmin)


class CustomUserForm(UserCreationForm):
    """
    Form for creating a new user in the admin panel.
    """
    password1 = forms.CharField(
        label=gettext_lazy("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=gettext_lazy("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=gettext_lazy("Enter the same password as before, for verification."),
        required=False,
    )


UserAdmin.list_display = ('username', 'is_staff')
UserAdmin.add_form = CustomUserForm


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
