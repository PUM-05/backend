from django.urls import path
from . import views

urlpatterns = [
    path('example', views.example),
    path('case', views.case),
    path('case/<int:id>', views.case_id),
    path('case/categories', views.case_categories),
]
