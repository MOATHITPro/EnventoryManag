from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TransferItem  # تأكد من استيراد الموديلات الصحيحة
from Enventory.models import Item


@receiver(post_save, sender=TransferItem)
def update_stock(sender, instance, **kwargs):
    transfer_operation = instance.transfer_operation
    # خصم الكمية من المخزن المصدر
    source_item = Item.objects.get(name=instance.item.name, warehouse=transfer_operation.source_warehouse)
    source_item.quantity_in_stock -= instance.quantity_transferred
    source_item.save()

    # إضافة الكمية إلى المخزن الوجهة
    destination_item, created = Item.objects.get_or_create(
        name=instance.item.name,
        warehouse=transfer_operation.destination_warehouse
    )
    destination_item.quantity_in_stock += instance.quantity_transferred
    destination_item.save()
