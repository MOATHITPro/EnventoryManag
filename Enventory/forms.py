
from django import forms
from .models import Warehouse  # تأكد من استيراد النموذج من ملف models.py

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'category', 'manager', 'phone']  # استبدل هذه الحقول بالحقول المناسبة لديك
