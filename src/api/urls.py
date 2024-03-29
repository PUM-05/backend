from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    path('check', views.check),
    path('case', views.case),
    path('case/<int:id>', views.case_id),
    path('case/categories', views.case_categories),
    path('stats/medium', views.stats_per_medium),
    path('stats/category', views.stats_per_category),
    path('stats/periods', views.stats_per_period)
]
