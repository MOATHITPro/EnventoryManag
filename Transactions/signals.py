from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TransferItem  # تأكد من استيراد الموديلات الصحيحة
from Enventory.models import Item,StockItem


@receiver(post_save, sender=TransferItem)
def update_stock(sender, instance, **kwargs):
    transfer_operation = instance.transfer_operation
    
    # خصم الكمية من المخزن المصدر
    source_item = StockItem.objects.get(item=instance.stock_item.item, warehouse=transfer_operation.source_warehouse)
    source_item.current_quantity -= instance.quantity_transferred
    source_item.save()

    # إضافة الكمية إلى المخزن الوجهة
    destination_item, created = StockItem.objects.get_or_create(
        item=instance.stock_item.item,  # استخدم كائن item مباشرة
        warehouse=transfer_operation.destination_warehouse
    )
    destination_item.current_quantity += instance.quantity_transferred
    destination_item.save()
