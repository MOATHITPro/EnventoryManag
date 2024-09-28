from django import forms
from .models import Receiving,Dispatch
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
            'imported_quantity',
            'transfer_date',
            'actual_transfer_date',
            'notes'
        ]
