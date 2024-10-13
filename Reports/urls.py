# urls.py
from django.urls import path
from .views import inventory_report,inventory_report_item,item_status_report,warehouse_status_report,inventory_report_beneficiary

urlpatterns = [
    path('inventory-report/', inventory_report, name='inventory_report'),
    path('inventory_report_item/', inventory_report_item, name='inventory_report_item'),
    path('warehouse_status_report/', warehouse_status_report, name='warehouse_status_report'),
    path('item_status_report/', item_status_report, name='item_status_report'),
    path('inventory_report_beneficiary/', inventory_report_beneficiary, name='inventory_report_beneficiary'),

]

