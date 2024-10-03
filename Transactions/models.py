# Create your models here.
from django.db import models
import uuid
from Enventory.models import Item,Warehouse,Supplier,Station,Beneficiary # تأكد من استيراد الموديلات المطلوبة
from django.db import transaction
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver

# نموذج Item

class Receiving(models.Model):
    # حقول عملية الاستلام
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE)
    receiving_date = models.DateField()
    document_number = models.CharField(max_length=50)
    supplier = models.ForeignKey('Enventory.Supplier', on_delete=models.CASCADE)
    station = models.ForeignKey('Enventory.Station', on_delete=models.CASCADE)
    supply_receipt_number = models.CharField(max_length=50)
    delivered_by_name = models.CharField(max_length=100)
    delivered_by_id = models.CharField(max_length=50)
    received_by_name = models.CharField(max_length=100)
    received_by_id = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    # حقول العناصر المستوردة
    item = models.ForeignKey('Enventory.Item', on_delete=models.CASCADE, default=1)  # استخدم ID العنصر الموجود
    imported_quantity = models.PositiveIntegerField(default=0)
    item_notes = models.TextField(blank=True, null=True)  # ملاحظات خاصة بالعنصر

    def save(self, *args, **kwargs):
        # تحديث الكمية في المخزون
        self.item.quantity_in_stock += self.imported_quantity
        self.item.save()
        super().save(*args, **kwargs)  # استدعاء الدالة الأصلية لحفظ الكائن

    def __str__(self):
        return f'Receiving {self.document_number} on {self.receiving_date}'




# نموذج Dispatch
class Dispatch(models.Model):
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE)
    dispatch_date = models.DateField()
    beneficiary = models.ForeignKey('Enventory.Beneficiary', on_delete=models.CASCADE)
    deliverer_name = models.CharField(max_length=255)
    deliverer_id = models.CharField(max_length=50)  # الرقم الجهادي للمسلّم
    recipient_name = models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=50)  # الرقم الجهادي للمستلم
    notes = models.TextField(blank=True, null=True)  # ملاحظات
    attached_files = models.FileField(upload_to='dispatch_files/', blank=True, null=True)  # ملفات مرفقة


    # حقول العناصر المستوردة
    item = models.ForeignKey('Enventory.Item', on_delete=models.CASCADE, default=1)  # استخدم ID العنصر الموجود
    imported_quantity = models.PositiveIntegerField(default=0)
    transfer_date = models.DateField()  # تاريخ التحويل
    actual_transfer_date = models.DateField(blank=True, null=True)  # تاريخ التحويل الفعلي
    notes = models.TextField(blank=True, null=True)  # ملاحظات إضافية


    def save(self, *args, **kwargs):
        # تحديث الكمية في المخزون
        self.item.quantity_in_stock -= self.imported_quantity
        self.item.save()
        super().save(*args, **kwargs)  # استدعاء الدالة الأصلية لحفظ الكائن

    def __str__(self):
        return f'Dispatch {self.warehouse.name} on {self.dispatch_date}'


    # def __str__(self):
    #     return f"Dispatch from {self.warehouse.name} on {self.dispatch_date}"

    def __str__(self):
        return f"{self.quantity_dispatched} of {self.item.name} in {self.dispatch.warehouse.name}"
