
from django import forms
from .models import Warehouse,Item,StockItem,Station,Supplier,Beneficiary# تأكد من استيراد النموذج من ملف models.py

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'category', 'manager', 'phone']  # استبدل هذه الحقول بالحقول المناسبة لديك


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'quantity_in_stock']

    


class StockItemForm(forms.ModelForm):
    class Meta:
        model = StockItem
        fields = ['item', 'warehouse', 'unit', 'opening_balance', 'current_quantity']

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['station_name', 'address']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['full_name', 'phone_number']

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ['full_name', 'phone_number']

