from django import forms
from .models import Receiving,Dispatch, ReceivingReturn,DispatchReturn,DamageOperation,TransferOperation, TransferItem
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# forms.py


class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = [
            'warehouse', 
            'receiving_date', 
            'supplier', 
            'station', 
            'supply_receipt_number', 
            'delivered_by_name', 
            'delivered_by_id', 
            'received_by_name', 
            'received_by_id', 
            'notes', 
            'attachments', 
            'stock_item', 
            'imported_quantity', 
            'item_notes'
        ]

        labels = {
            'warehouse': 'اسم المخزن',
            'receiving_date': 'تاريخ الاستلام',
            'supplier': 'المورد',
            'station': 'المحطة',
            'supply_receipt_number': 'رقم إيصال التوريد',
            'delivered_by_name': 'اسم الشخص الذي قام بالتسليم',
            'delivered_by_id': 'معرف الشخص الذي قام بالتسليم',
            'received_by_name': 'اسم الشخص الذي استلم',
            'received_by_id': 'معرف الشخص الذي استلم',
            'notes': 'ملاحظات',
            'attachments': 'المرفقات',
            'stock_item': 'العنصر',
            'imported_quantity': 'الكمية المستوردة',
            'item_notes': 'ملاحظات العنصر',
        }




class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = [
            'warehouse',
            'dispatch_date',
            'beneficiary',
            'deliverer_name',
            'deliverer_id',
            'recipient_name',
            'recipient_id',
            'notes',
            'attached_files',
            'stock_item',
            'quantity_dispatched',
            'transfer_date',
            'actual_transfer_date',
            'notes'
        ]

        labels = {
            'warehouse': 'اسم المخزن',
            'dispatch_date': 'تاريخ التوزيع',
            'beneficiary': 'المستفيد',
            'deliverer_name': 'اسم المرسل',
            'deliverer_id': 'معرف المرسل',
            'recipient_name': 'اسم المستلم',
            'recipient_id': 'معرف المستلم',
            'notes': 'ملاحظات',
            'attached_files': 'الملفات المرفقة',
            'stock_item': 'العنصر',
            'quantity_dispatched': 'الكمية المرسلة',
            'transfer_date': 'تاريخ النقل',
            'actual_transfer_date': 'تاريخ النقل الفعلي',
        }




class ReceivingReturnForm(forms.ModelForm):
    class Meta:
        model = ReceivingReturn
        fields = [
            'receiving', 
            'return_date', 
            'delivered_by_name', 
            'delivered_by_id', 
            'received_by_name', 
            'received_by_id', 
            'notes', 
            'attachments',  
            'returned_quantity', 
            'expected_return_date', 
            'actual_return_date', 
            'item_notes'
        ]
        widgets = {
            'receiving': forms.Select(attrs={'id': 'id'}),  # تخصيص الـ id هنا ليكون "id"
        }
        labels = {
            'receiving': 'استلام',
            'return_date': 'تاريخ الإرجاع',
            'delivered_by_name': 'اسم المرسل',
            'delivered_by_id': 'معرف المرسل',
            'received_by_name': 'اسم المستلم',
            'received_by_id': 'معرف المستلم',
            'notes': 'ملاحظات',
            'attachments': 'الملفات المرفقة',
            'returned_quantity': 'الكمية المعادة',
            'expected_return_date': 'تاريخ الإرجاع المتوقع',
            'actual_return_date': 'تاريخ الإرجاع الفعلي',
            'item_notes': 'ملاحظات العنصر',
        }



        
class DispatchReturnForm(forms.ModelForm):
    class Meta:
        model = DispatchReturn
        fields = [
            'dispatch', 
            'return_date', 
            'delivered_by_name', 
            'delivered_by_id', 
            'received_by_name', 
            'received_by_id', 
            'notes', 
            'attachments',  
            'returned_quantity', 
            'expected_return_date', 
            'actual_return_date', 
            'item_notes'
        ]
        widgets = {
            'dispatch': forms.Select(attrs={'id': 'id'}),
        }
        labels = {
            'dispatch': 'إرجاع الشحنة',
            'return_date': 'تاريخ الإرجاع',
            'delivered_by_name': 'اسم المرسل',
            'delivered_by_id': 'معرف المرسل',
            'received_by_name': 'اسم المستلم',
            'received_by_id': 'معرف المستلم',
            'notes': 'ملاحظات',
            'attachments': 'الملفات المرفقة',
            'returned_quantity': 'الكمية المعادة',
            'expected_return_date': 'تاريخ الإرجاع المتوقع',
            'actual_return_date': 'تاريخ الإرجاع الفعلي',
            'item_notes': 'ملاحظات العنصر',
        }




class DamageOperationForm(forms.ModelForm):
    class Meta:
        model = DamageOperation
        fields = [
            'warehouse',
            'damage_date',
            'delivered_by_name',
            'delivered_by_id',
            'received_by_name',
            'received_by_id',
            'notes',
            'attachments',
            'stock_item',
            'damaged_quantity',
            'reason',
            'item_notes',
        ]
        widgets = {
            'damage_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'warehouse': 'اسم المخزن',
            'damage_date': 'تاريخ الضرر',
            'delivered_by_name': 'اسم المرسل',
            'delivered_by_id': 'معرف المرسل',
            'received_by_name': 'اسم المستلم',
            'received_by_id': 'معرف المستلم',
            'notes': 'ملاحظات',
            'attachments': 'الملفات المرفقة',
            'stock_item': 'العنصر',
            'damaged_quantity': 'الكمية المتضررة',
            'reason': 'السبب',
            'item_notes': 'ملاحظات العنصر',
        }



class TransferOperationForm(forms.ModelForm):
    class Meta:
        model = TransferOperation
        fields = [
            'source_warehouse', 
            'destination_warehouse', 
            'sender_name', 
            'sender_job_number', 
            'receiver_name', 
            'receiver_job_number', 
            'statement', 
            'attachments',
        ]
        labels = {
            'source_warehouse': 'المخزن المصدر',
            'destination_warehouse': 'المخزن الوجهة',
            'sender_name': 'اسم المرسل',
            'sender_job_number': 'رقم وظيفة المرسل',
            'receiver_name': 'اسم المستلم',
            'receiver_job_number': 'رقم وظيفة المستلم',
            'statement': 'بيان',
            'attachments': 'الملفات المرفقة',
        }

class TransferItemForm(forms.ModelForm):
    class Meta:
        model = TransferItem
        fields = [
            'stock_item', 
            'quantity_transferred', 
            'reason', 
            'notes',
        ]
        labels = {
            'stock_item': 'العنصر',
            'quantity_transferred': 'الكمية المنقولة',
            'reason': 'السبب',
            'notes': 'ملاحظات',
        }
