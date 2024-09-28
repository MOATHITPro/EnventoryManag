
from django.urls import path
from .views import home,warehouses_view,items_view,add_warehouse,additem,stockitems_view,station_view,add_station,add_supplier,supplier_view,add_beneficiary,beneficiary_view,add_stock_item_view

urlpatterns = [
    path('', home, name='home'),
    path('add-warehouse/', add_warehouse, name='add_warehouse'),  # تأكد من استخدام المسار الصحيح
    path('warehouses/', warehouses_view, name='warehouses'),#عرض المخازن
    
    path('add-item/', additem, name='add_item'),     # اضافة صنف
    path('items/', items_view, name='items'),# عرض الاصناف

    path('add_stock_items/', stockitems_view, name='add_stock_items'),
    path('add-stock-item/', add_stock_item_view, name='add_stock_item'),
    path('add_station/', add_station, name='add_station'),
    path('stations/', station_view, name='stations'),

    path('add_supplier/', add_supplier, name='add_supplier'),
    path('suppliers/', supplier_view, name='suppliers'),

    path('add_beneficiary/', add_beneficiary, name='add_beneficiary'),
    path('beneficiarys/', beneficiary_view, name='beneficiarys'),

]
                        
