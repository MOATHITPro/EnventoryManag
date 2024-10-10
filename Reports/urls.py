# urls.py
from django.urls import path
from .views import inventory_report

urlpatterns = [
    path('inventory-report/', inventory_report, name='inventory_report'),
]
