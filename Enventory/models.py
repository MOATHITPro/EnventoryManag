

# Create your models here.

# Create your models here.
from django.db import models
import uuid


class Warehouse(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity_in_stock = models.IntegerField(default=0)  # تأكد من وجود هذا الحقل
    warehouse = models.ForeignKey(Warehouse, related_name='items', on_delete=models.CASCADE, default=1)  # ربط الصنف بالمخزن

    def __str__(self):
        return self.name

class StockItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.item.name} in {self.warehouse.name}"

class Station(models.Model):
    station_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.station_name

class Supplier(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.full_name

class Beneficiary(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.full_name

