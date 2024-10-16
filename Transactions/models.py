# Create your models here.
from django.db import models
import uuid
from Enventory.models import Item,Warehouse,Supplier,Station,Beneficiary ,StockItem# تأكد من استيراد الموديلات المطلوبة
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
    document_number = models.CharField(max_length=50, unique=True, blank=True)
    supplier = models.ForeignKey('Enventory.Supplier', on_delete=models.CASCADE)
    station = models.ForeignKey('Enventory.Station', on_delete=models.CASCADE)
    supply_receipt_number = models.CharField(max_length=50)
    delivered_by_name = models.CharField(max_length=100)
    delivered_by_id = models.CharField(max_length=50)
    received_by_name = models.CharField(max_length=100)
    received_by_id = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    stock_item = models.ForeignKey('Enventory.StockItem', on_delete=models.CASCADE, null=True)
    imported_quantity = models.PositiveIntegerField(default=0)
    item_notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # تعيين الرقم التلقائي للمستند
        if not self.document_number:  # إذا لم يكن هناك رقم مستند معين
            last_receiving = Receiving.objects.aggregate(Max('id'))  # الحصول على الرقم الأخير
            if last_receiving['id__max'] is not None:
                self.document_number = str(last_receiving['id__max'] + 1)  # زيادة الرقم بواحد
            else:
                self.document_number = '1'  # إذا لم توجد أي مستندات سابقة

        # تحديث الكمية في StockItem
        self.stock_item.current_quantity += self.imported_quantity
        self.stock_item.save()
        
        super().save(*args, **kwargs)  # استدعاء الدالة الأصلية لحفظ الكائن

    def __str__(self):
        return f'Receiving {self.document_number} from {self.supplier} at {self.warehouse} on {self.receiving_date} (Station: {self.station})'






class Dispatch(models.Model):
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE)
    dispatch_date = models.DateField(default=timezone.now)
    document_number = models.CharField(max_length=50)
    beneficiary = models.ForeignKey('Enventory.Beneficiary', on_delete=models.CASCADE)
    deliverer_name = models.CharField(max_length=255)
    deliverer_id = models.CharField(max_length=50)  # الرقم الجهادي للمسلّم
    recipient_name = models.CharField(max_length=255)
    recipient_id = models.CharField(max_length=50)  # الرقم الجهادي للمستلم
    notes = models.TextField(blank=True, null=True)  # ملاحظات
    attached_files = models.FileField(upload_to='dispatch_files/', blank=True, null=True)  # ملفات مرفقة

    # حقول العناصر المستوردة
    stock_item = models.ForeignKey('Enventory.StockItem', on_delete=models.CASCADE, null=True)
    quantity_dispatched = models.PositiveIntegerField(default=0)
    transfer_date = models.DateField(default=timezone.now)  # حقل غير قابل لـ null بقيمة افتراضية
    actual_transfer_date = models.DateField(default=timezone.now)  # تاريخ التحويل الفعلي
    notes = models.TextField(blank=True, null=True)  # ملاحظات إضافية

    def save(self, *args, **kwargs):
        # تحقق من الكمية المتاحة في المخزن
        if self.quantity_dispatched > self.stock_item.current_quantity:
            # بدلاً من رفع استثناء، نستخدم add_error لإضافة الخطأ إلى النموذج
            raise ValidationError("الكمية المطلوبة للصرف أكبر من الكمية المتاحة في المخزن.")

        # تحديث رقم المستند
        if not self.document_number:  # إذا لم يكن هناك رقم مستند معين
            last_dispatch = Dispatch.objects.aggregate(Max('id'))  # الحصول على الرقم الأخير
            if last_dispatch['id__max'] is not None:
                self.document_number = str(last_dispatch['id__max'] + 1)  # زيادة الرقم بواحد
            else:
                self.document_number = '1'  # إذا لم توجد أي مستندات سابقة

        # تحديث الكمية في المخزون
        self.stock_item.current_quantity -= self.quantity_dispatched
        self.stock_item.save()
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
    
    stock_item = models.ForeignKey('Enventory.StockItem', on_delete=models.CASCADE,editable=False, null=True )
    returned_quantity = models.PositiveIntegerField(default=0)  # الكمية المرتجعة
    expected_return_date = models.DateField(blank=True, null=True)  # تاريخ الرد المفترض
    actual_return_date = models.DateField(blank=True, null=True)  # تاريخ الرد الفعلي
    item_notes = models.TextField(blank=True, null=True)  # ملاحظات

    def save(self, *args, **kwargs):
        # عند اختيار عملية الوارد، يتم تعبئة الحقول المرتبطة بها تلقائيًا
        
        if not self.document_number:  # إذا لم يكن هناك رقم مستند معين
            last_receivingreturn = ReceivingReturn.objects.aggregate(Max('id'))  # الحصول على الرقم الأخير
            if last_receivingreturn['id__max'] is not None:
                self.document_number = str(last_receivingreturn['id__max'] + 1)  # زيادة الرقم بواحد
            else:
                self.document_number = '1'  # إذا لم توجد أي مستندات سابقة

        
        if self.receiving:
            self.receiving_date = self.receiving.receiving_date
            self.warehouse = self.receiving.warehouse
            self.supplier = self.receiving.supplier
            self.station = self.receiving.station
            self.stock_item = self.receiving.stock_item

        # تحقق من الكمية المتاحة
        if self.returned_quantity > self.stock_item.current_quantity:
            raise ValidationError("الكمية المرتجعة تتجاوز الكمية المتاحة في المخزون")

        # خصم الكمية المرتجعة من المخزون باستخدام F expressions
        self.stock_item.current_quantity = F('current_quantity') - self.returned_quantity
        self.stock_item.save()

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
        document_number = models.CharField(max_length=50)  # الرقم الورقي للمرتجع
        delivered_by_name = models.CharField(max_length=100)  # اسم المسلم
        delivered_by_id = models.CharField(max_length=50, )  # الرقم الجهادي للمسلم
        received_by_name = models.CharField(max_length=100)  # اسم المستلم
        received_by_id = models.CharField(max_length=50, )  # الرقم الجهادي للمستلم
        notes = models.TextField(blank=True, null=True)  # البيان
        attachments = models.FileField(upload_to='return_attachments/', blank=True, null=True)  # ملفات مرفقة مع عملية المرتجع

      # حقل الأصناف المرتجعة (يجب أن يكون من الأصناف المرتبطة بعملية الصادر)
        stock_item = models.ForeignKey('Enventory.StockItem', on_delete=models.CASCADE,editable=False, null=True )
        returned_quantity = models.PositiveIntegerField(default=0)  # الكمية المرتجعة
        expected_return_date = models.DateField(default=timezone.now, blank=True, null=True)  # تاريخ الرد المفترض
        actual_return_date = models.DateField(default=timezone.now, blank=True, null=True)  # تاريخ الرد الفعلي
        item_notes = models.TextField(blank=True, null=True)  # ملاحظات
          
     
        def save(self, *args, **kwargs):
        # تحقق من أن الكمية المرتجعة لا يمكن أن تكون أقل من الصفر
         if self.returned_quantity < 0:
            raise ValidationError("Returned quantity cannot be negative.")
        
        # تعبئة الحقول المرتبطة تلقائيًا إذا كانت العملية مرتبطة
         if self.dispatch:
            self.dispatch_date = self.dispatch.dispatch_date
            self.warehouse = self.dispatch.warehouse
            self.beneficiary = self.dispatch.beneficiary
            self.stock_item = self.dispatch.stock_item


        # تحديث المخزون إذا كانت الكمية المرتجعة أقل من أو تساوي الكمية المصروفة
         if self.returned_quantity > 0 and self.returned_quantity <= self.dispatch.quantity_dispatched:
            self.stock_item.current_quantity += self.returned_quantity
            self.stock_item.save()  # حفظ التغييرات في المخزون
            
            # تحديث الكمية المتبقية في عملية الصادر
            self.dispatch.quantity_dispatched -= self.returned_quantity
            self.dispatch.save()  # حفظ التغييرات في عملية الصادر

        # استدعاء super().save لحفظ الكائن الحالي
         super().save(*args, **kwargs)

        def __str__(self):
         return f"Return from Dispatch {self.dispatch.id} on {self.return_date}"
       




class DamageOperation(models.Model):
    # الحقول العامة لعملية التلف
    warehouse = models.ForeignKey('Enventory.Warehouse', on_delete=models.CASCADE)  # المخزن الذي يحتوي على الأصناف التالفة
    damage_date = models.DateField(default=timezone.now)  # تاريخ التلف
    document_number = models.CharField(max_length=50, unique=True, blank=True)  # الرقم الورقي
    delivered_by_name = models.CharField(max_length=100)  # اسم المسلم
    delivered_by_id = models.CharField(max_length=50)  # الرقم الجهادي للمسلّم
    received_by_name = models.CharField(max_length=100)  # اسم المستلم
    received_by_id = models.CharField(max_length=50)  # الرقم الجهادي للمستلم
    notes = models.TextField(blank=True, null=True)  # البيان
    attachments = models.FileField(upload_to='damage_attachments/', blank=True, null=True)  # ملفات مرفقة مع عملية التلف

    # الأصناف التالفة
    stock_item = models.ForeignKey('Enventory.StockItem', on_delete=models.CASCADE , null=True)
    damaged_quantity = models.PositiveIntegerField()  # الكمية التالفة
    reason = models.TextField(blank=True, null=True)  # سبب التلف
    item_notes = models.TextField(blank=True, null=True)  # ملاحظات على الصنف التالف

    def save(self, *args, **kwargs):

        if not self.document_number:  # إذا لم يكن هناك رقم مستند معين
            last_damageoperation = DamageOperation.objects.aggregate(Max('id'))  # الحصول على الرقم الأخير
            if last_damageoperation['id__max'] is not None:
                self.document_number = str(last_damageoperation['id__max'] + 1)  # زيادة الرقم بواحد
            else:
                self.document_number = '1'  # إذا لم توجد أي مستندات سابقة

        # تحقق من أن الكمية التالفة لا تتجاوز الكمية المتاحة في المخزون
        if self.damaged_quantity > self.stock_item.current_quantity:
            raise ValidationError(f"The damaged quantity ({self.damaged_quantity}) cannot exceed the available stock ({self.item.quantity_in_stock}).")
        
        # خصم الكمية التالفة من المخزون
        self.stock_item.current_quantity -= self.damaged_quantity
        self.stock_item.save()

        # تنفيذ الحفظ
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Damage Operation {self.document_number} - {self.warehouse.name} - {self.stock_item.item.name}"


  # تأكد من تعديل الاستيراد حسب هيكل مشروعك

class TransferOperation(models.Model):
    source_warehouse = models.ForeignKey(Warehouse, related_name='transfers_out', on_delete=models.CASCADE)
    destination_warehouse = models.ForeignKey(Warehouse, related_name='transfers_in', on_delete=models.CASCADE)
    transfer_date = models.DateTimeField(auto_now_add=True)
    paper_number = models.CharField(max_length=100)
    sender_name = models.CharField(max_length=255)
    sender_job_number = models.CharField(max_length=50)
    receiver_name = models.CharField(max_length=255)
    receiver_job_number = models.CharField(max_length=50)
    statement = models.TextField(blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f'Transfer from {self.source_warehouse} to {self.destination_warehouse} on {self.transfer_date}'


class TransferItem(models.Model):
    transfer_operation = models.ForeignKey(TransferOperation, related_name='transfer_items', on_delete=models.CASCADE)
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, null=True)
    quantity_transferred = models.PositiveIntegerField()  # الكمية المحولة
    reason = models.TextField(blank=True, null=True)  # السبب
    notes = models.TextField(blank=True, null=True)  # ملاحظات

    def __str__(self):
        return f'{self.stock_item.item.name} - {self.quantity_transferred}'

# إشارة لتحديث المخزون بعد حفظ عنصر التحويل
@receiver(post_save, sender=TransferItem)
def update_stock_on_transfer(sender, instance, **kwargs):
    transfer_item = instance
    transfer_operation = transfer_item.transfer_operation

    # خصم الكمية من المخزن المصدر
    try:
        source_item = StockItem.objects.get(item=transfer_item.stock_item.item, warehouse=transfer_operation.source_warehouse)
        if source_item.current_quantity >= transfer_item.quantity_transferred:
            source_item.current_quantity -= transfer_item.quantity_transferred
            source_item.save()
        else:
            raise ValueError(f"Insufficient stock for item {transfer_item.stock_item.item.name} in source warehouse.")
    except StockItem.DoesNotExist:
        raise ValueError(f"Item {transfer_item.stock_item.item.name} does not exist in source warehouse.")

    # إضافة الكمية إلى المخزن الوجهة
    destination_item, created = StockItem.objects.get_or_create(
        item=transfer_item.stock_item.item,
        warehouse=transfer_operation.destination_warehouse
    )
    destination_item.current_quantity += transfer_item.quantity_transferred
    destination_item.save()
