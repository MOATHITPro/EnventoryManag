from django import forms
from .models import Receiving,Dispatch, ReceivingReturn
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# forms.py

class ReceivingForm(forms.ModelForm):
    class Meta:
        model = Receiving
        fields = [
            'warehouse', 
            'receiving_date', 
            'document_number', 
            'supplier', 
            'station', 
            'supply_receipt_number', 
            'delivered_by_name', 
            'delivered_by_id', 
            'received_by_name', 
            'received_by_id', 
            'notes', 
            'attachments', 
            'item', 
            'imported_quantity', 
            'item_notes'
        ]



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
            'item',
            'quantity_dispatched',
            'transfer_date',
            'actual_transfer_date',
            'notes'
        ]




class ReceivingReturnForm(forms.ModelForm):
    class Meta:
        model = ReceivingReturn
        fields = ['receiving', 'return_date', 'document_number', 'delivered_by_name', 
                  'delivered_by_id', 'received_by_name', 'received_by_id', 
                  'notes', 'attachments',  'returned_quantity', 
                  'expected_return_date', 'actual_return_date', 'item_notes']
        widgets = {
            'receiving': forms.Select(attrs={'id': 'id'}),  # تخصيص الـ id هنا ليكون "id"
        }