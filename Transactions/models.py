# Create your models here.
from django.db import models
import uuid
from Enventory.models import Item,Warehouse,Supplier,Station,Beneficiary # تأكد من استيراد الموديلات المطلوبة
from django.db import transaction
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import F
from django.forms import ModelChoiceField
from django import forms
from django.db.models import Max

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

    # def __str__(self):
    #     return f'Receiving {self.document_number} on {self.receiving_date}'
    def __str__(self):
        return f'Receiving {self.document_number} from {self.supplier} at {self.warehouse} on {self.receiving_date} (Station: {self.station})'




# نموذج Dispatch
class Dispatch(models.Model):
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE)
    dispatch_date = models.DateField(default=timezone.now)
    beneficiary = models.ForeignKey('Enventory.Beneficiary', on_delete=models.CASCADE)
    deliverer_name = models.CharField(max_length=255)
    deliverer_id = models.CharField(max_length=50)  # الرقم الجهادي للمسلّم
    recipient_name = models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=50)  # الرقم الجهادي للمستلم
    notes = models.TextField(blank=True, null=True)  # ملاحظات
    attached_files = models.FileField(upload_to='dispatch_files/', blank=True, null=True)  # ملفات مرفقة


    # حقول العناصر المستوردة
    item = models.ForeignKey('Enventory.Item', on_delete=models.CASCADE)  # استخدم ID العنصر الموجود
    quantity_dispatched = models.PositiveIntegerField(default=0)
    transfer_date = models.DateField(default=timezone.now)  # حقل غير قابل لـ null بقيمة افتراضية
    actual_transfer_date = models.DateField(default=timezone.now)  # تاريخ التحويل الفعلي
    notes = models.TextField(blank=True, null=True)  # ملاحظات إضافية


    def save(self, *args, **kwargs):
        # تحديث الكمية في المخزون
        self.item.quantity_in_stock -= self.quantity_dispatched
        self.item.save()
        super().save(*args, **kwargs)  # استدعاء الدالة الأصلية لحفظ الكائن


    def __str__(self):
        return f"Dispatch from {self.warehouse.name} on {self.dispatch_date}"

  




class ReceivingReturn(models.Model):
    receiving = models.ForeignKey('Receiving', on_delete=models.CASCADE)  # عملية الوارد الأصلية المراد الإرجاع منها
    return_date = models.DateField()  # تاريخ المرتجع
    document_number = models.CharField(max_length=50)  # الرقم الورقي للمرتجع
    delivered_by_name = models.CharField(max_length=100)  # اسم المسلم
    delivered_by_id = models.CharField(max_length=50)  # الرقم الجهادي للمسلم
    received_by_name = models.CharField(max_length=100)  # اسم المستلم
    received_by_id = models.CharField(max_length=50)  # الرقم الجهادي للمستلم
    notes = models.TextField(blank=True, null=True)  # البيان
    attachments = models.FileField(upload_to='return_attachments/', blank=True, null=True)  # ملفات مرفقة مع عملية المرتجع

    # حقول مرتبطة بعملية الوارد الأصلية (تعبأ تلقائيًا)
    receiving_date = models.DateField(editable=False)  # تاريخ الوارد (يعبأ تلقائيًا)
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE, editable=False)  # المخزن (يعبأ تلقائيًا)
    supplier = models.ForeignKey('Enventory.Supplier', on_delete=models.CASCADE, editable=False)  # المورد (يعبأ تلقائيًا)
    station = models.ForeignKey('Enventory.Station', on_delete=models.CASCADE, editable=False)  # المحطة (يعبأ تلقائيًا)

    # حقل الأصناف المرتجعة (يجب أن يكون من الأصناف المرتبطة بعملية الوارد)
    item = models.ForeignKey('Enventory.Item', on_delete=models.CASCADE, editable=False )  # الصنف المرتجع
    returned_quantity = models.PositiveIntegerField(default=0)  # الكمية المرتجعة
    expected_return_date = models.DateField(blank=True, null=True)  # تاريخ الرد المفترض
    actual_return_date = models.DateField(blank=True, null=True)  # تاريخ الرد الفعلي
    item_notes = models.TextField(blank=True, null=True)  # ملاحظات

    def save(self, *args, **kwargs):
        # عند اختيار عملية الوارد، يتم تعبئة الحقول المرتبطة بها تلقائيًا
        if self.receiving:
            self.receiving_date = self.receiving.receiving_date
            self.warehouse = self.receiving.warehouse
            self.supplier = self.receiving.supplier
            self.station = self.receiving.station
            self.item = self.receiving.item

        # تحقق من الكمية المتاحة
        if self.returned_quantity > self.item.quantity_in_stock:
            raise ValueError("الكمية المرتجعة تتجاوز الكمية المتاحة في المخزون")

        # خصم الكمية المرتجعة من المخزون باستخدام F expressions
        self.item.quantity_in_stock = F('quantity_in_stock') - self.returned_quantity
        self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Return {self.document_number} for Receiving {self.receiving.document_number} on {self.return_date}'

    class Meta:
        verbose_name = 'Receiving Return'
        verbose_name_plural = 'Receiving Returns'




class DispatchReturn(models.Model):
    # الحقول المرتبطة بالصادر
        dispatch = models.ForeignKey('Dispatch', on_delete=models.CASCADE)  # عملية الصادر الأصلية المراد الإرجاع منها
        return_date = models.DateField(default=timezone.now)  # تاريخ المرتجع
        dispatch_date = models.DateField(editable=False)
        warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE, editable=False)
        beneficiary = models.ForeignKey('Enventory.Beneficiary', on_delete=models.CASCADE, editable=False)
       
           # الحقول الخاصة بعملية المرتجع
        document_number = models.CharField(max_length=50, unique=True, blank=False)  # الرقم الورقي للمرتجع
        delivered_by_name = models.CharField(max_length=100)  # اسم المسلم
        delivered_by_id = models.CharField(max_length=50, unique=True)  # الرقم الجهادي للمسلم
        received_by_name = models.CharField(max_length=100)  # اسم المستلم
        received_by_id = models.CharField(max_length=50, unique=True)  # الرقم الجهادي للمستلم
        notes = models.TextField(blank=True, null=True)  # البيان
        attachments = models.FileField(upload_to='return_attachments/', blank=True, null=True)  # ملفات مرفقة مع عملية المرتجع

      # حقل الأصناف المرتجعة (يجب أن يكون من الأصناف المرتبطة بعملية الصادر)
        item = models.ForeignKey('Enventory.Item', on_delete=models.CASCADE, editable=False )  # الصنف المرتجع
        returned_quantity = models.PositiveIntegerField(default=0)  # الكمية المرتجعة
        expected_return_date = models.DateField(default=timezone.now, blank=True, null=True)  # تاريخ الرد المفترض
        actual_return_date = models.DateField(default=timezone.now, blank=True, null=True)  # تاريخ الرد الفعلي
        item_notes = models.TextField(blank=True, null=True)  # ملاحظات


        def save(self, *args, **kwargs):

                # تحقق من أن الكمية المرتجعة لا يمكن أن تكون أقل من الصفر
            if self.returned_quantity < 0:
                raise ValidationError("Returned quantity cannot be negative.")

        # عند اختيار عملية الوارد، يتم تعبئة الحقول المرتبطة بها تلقائيًا
            if self.dispatch:
                self.dispatch_date = self.dispatch.dispatch_date
                self.warehouse = self.dispatch.warehouse
                self.beneficiary = self.dispatch.beneficiary
                self.item = self.dispatch.item

             # توليد رقم ورقي (document_number) فريد إذا لم يتم تقديمه
            if not self.document_number:
             # الحصول على آخر رقم ورقي موجود في قاعدة البيانات
               last_document_number = DispatchReturn.objects.aggregate(Max('document_number'))['document_number__max']
    
            # إذا كان هناك رقم ورقي سابق، نزيده بقيمة 1
            if last_document_number and last_document_number.isdigit():
                self.document_number = str(int(last_document_number) + 1)
            else:
              # إذا لم يكن هناك أرقام سابقة، نبدأ من 1001 (أو أي رقم تبدأ منه)
             self.document_number = "1001"

            # تحقق من أن الكمية المرتجعة لا تتجاوز الكمية المصروفة في عملية الصادر
            if self.returned_quantity > self.dispatch.quantity_dispatched:
                raise ValidationError(f"The returned quantity ({self.returned_quantity}) cannot exceed the dispatched quantity ({self.dispatch.quantity_dispatched}).")
                        
                     # إذا كانت الكمية المرتجعة أقل من أو تساوي الكمية المصروفة، تحديث المخزون
            if self.returned_quantity <= self.dispatch.quantity_dispatched:
            # أضف الكمية المرتجعة إلى المخزون
                self.item.quantity_in_stock += self.returned_quantity
                self.item.save()          
                       
             # قم بتحديث الكمية المتبقية في الصادر (لإظهار الكمية التي لم تُرجع)
                self.dispatch.quantity_dispatched -= self.returned_quantity
                self.dispatch.save()     
                       
                        # تحقق من الكمية المتاحة
                super().save(*args, **kwargs)
      
        def __str__(self):
             return f"Return from Dispatch {self.dispatch.id} on {self.return_date}"
       
       
       
       
       
    