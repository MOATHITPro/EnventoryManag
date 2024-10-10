from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime
import pandas as pd
from io import BytesIO
from reportlab.pdfgen import canvas
from xhtml2pdf import pisa
from django.template.loader import get_template
from Transactions.models import Receiving, Dispatch, ReceivingReturn, DamageOperation
from Enventory.models import Warehouse  # تأكد من استيراد الموديلات المطلوبة

def inventory_report(request):
    report_data = None
    start_date = None
    end_date = None
    warehouse_id = None

    if request.method == "POST":
        warehouse_id = request.POST.get('warehouse')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # تأكد من تحويل التواريخ
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            # أضف هنا معالجة الأخطاء للتواريخ غير الصحيحة
            pass

        # استرجاع البيانات من النماذج وفقًا للنطاق الزمني والمخزن المحدد
        receiving_data = Receiving.objects.filter(
            warehouse_id=warehouse_id,
            receiving_date__range=[start_date, end_date]
        )
        dispatch_data = Dispatch.objects.filter(
            warehouse_id=warehouse_id,
            dispatch_date__range=[start_date, end_date]
        )
        return_data = ReceivingReturn.objects.filter(
            warehouse_id=warehouse_id,
            return_date__range=[start_date, end_date]
        )
        damage_data = DamageOperation.objects.filter(
            warehouse_id=warehouse_id,
            damage_date__range=[start_date, end_date]
        )

        report_data = {
            'Receiving': receiving_data,
            'Dispatch': dispatch_data,
            'Return': return_data,
            'Damage': damage_data,
        }

        # توليد PDF
        if 'generate_pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
            template = get_template('report/report_template.html')
            html = template.render(report_data)
            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response

        # توليد Excel
        elif 'generate_excel' in request.POST:
            all_rows = []
            for row in receiving_data:
                all_rows.append({
                    "نوع العملية": "Receiving",
                    "التاريخ": row.receiving_date,
                    "رقم الوثيقة": row.document_number,
                    "المورد أو المستفيد": row.supplier.name if row.supplier else "N/A",
                    "الكمية": row.imported_quantity
                })

            for row in dispatch_data:
                all_rows.append({
                    "نوع العملية": "Dispatch",
                    "التاريخ": row.dispatch_date,
                    "رقم الوثيقة": row.document_number,
                    "المورد أو المستفيد": row.beneficiary.name if row.beneficiary else "N/A",
                    "الكمية": row.quantity_dispatched
                })

            for row in return_data:
                all_rows.append({
                    "نوع العملية": "Return",
                    "التاريخ": row.return_date,
                    "رقم الوثيقة": row.document_number,
                    "المورد أو المستفيد": row.supplier.name if row.supplier else "N/A",
                    "الكمية": row.returned_quantity
                })

            for row in damage_data:
                all_rows.append({
                    "نوع العملية": "Damage",
                    "التاريخ": row.damage_date,
                    "رقم الوثيقة": row.document_number,
                    "المورد أو المستفيد": row.item.name if row.item else "N/A",
                    "الكمية": row.damaged_quantity
                })

            df = pd.DataFrame(all_rows)

            # حفظ ملف Excel في الذاكرة
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Inventory Report')
            output.seek(0)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.xlsx"'
            return response

    warehouses = Warehouse.objects.all()  # استرجاع جميع المخازن لعرضها في النموذج
    return render(request, 'report/inventory_report_form.html', {
        'warehouses': warehouses,
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'warehouse_id': warehouse_id,
    })
