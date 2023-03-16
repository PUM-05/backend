from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('check', views.check),
    path('case', views.case),
    path('case/<int:id>', views.case_id),
    path('case/categories', views.case_categories),
]
