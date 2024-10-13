# forms.py
from django import forms
from Enventory.models import Warehouse  # تأكد من استيراد الموديلات المطلوبة


class WarehouseReportForm(forms.Form):
    warehouse = forms.ModelChoiceField(queryset=Warehouse.objects.all(), label="اختر المخزن")
    report_type = forms.ChoiceField(choices=[('pdf', 'PDF'), ('excel', 'Excel')], label="نوع التقرير")



