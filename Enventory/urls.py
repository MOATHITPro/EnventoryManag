
from django.urls import path
from .views import home,warehouses_view,items_view,add_warehouse

urlpatterns = [
    path('', home, name='home'),
    path('warehouses/', warehouses_view, name='warehouses'),
    path('items/', items_view, name='items'),
    path('add-warehouse/', add_warehouse, name='add_warehouse'),  # تأكد من استخدام المسار الصحيح

]