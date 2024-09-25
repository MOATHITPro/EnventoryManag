

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

    def __str__(self):
        return self.station_name

class Supplier(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Beneficiary(models.Model):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


class Receiving(models.Model):
    warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE)
    receiving_date = models.DateField()
    document_number = models.CharField(max_length=50)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE)
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    supply_receipt_number = models.CharField(max_length=50)
    delivered_by_name = models.CharField(max_length=100)
    delivered_by_id = models.CharField(max_length=50)
    received_by_name = models.CharField(max_length=100)
    received_by_id = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f'Receiving {self.document_number} on {self.receiving_date}'

class ImportedItem(models.Model):
    receiving = models.ForeignKey(Receiving, related_name='imported_items', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    imported_quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # تحقق مما إذا كانت الكمية المستوردة موجودة بالفعل
        existing_item = ImportedItem.objects.filter(receiving=self.receiving, item=self.item).first()
        
        if existing_item:
            # إذا كان العنصر موجودًا، يمكنك تحديث الكمية بدلاً من إضافة صف جديد
            existing_item.imported_quantity += self.imported_quantity
            existing_item.save()
        else:
            # إذا لم يكن موجودًا، قم بإضافة الصف الجديد
            self.item.quantity_in_stock += self.imported_quantity
            self.item.save()
            super().save(*args, **kwargs)

