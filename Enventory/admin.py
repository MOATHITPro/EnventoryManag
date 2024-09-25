

# Register your models here.

from django.contrib import admin
from .models import Warehouse, Item, StockItem, Station, Supplier, Beneficiary

admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(StockItem)
admin.site.register(Station)
admin.site.register(Supplier)
admin.site.register(Beneficiary)


