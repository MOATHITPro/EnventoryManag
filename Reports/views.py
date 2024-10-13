
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from Transactions.models import Receiving, Dispatch, ReceivingReturn, DamageOperation
from Enventory.models import Warehouse,Item,StockItem ,Beneficiary

from .utils.pdf_w_movement_report import generate_pdf  # استيراد دالة PDF
from .utils.excel_w_movement_report import generate_excel
from .utils.pdf_w_movement_report_item import generate_pdf_item  # استيراد دالة PDF
from .utils.excel_w_movement_report_item import generate_excel_item

from .utils.pdf_item_status_report import generate_pdf_item_status  # تأكد من إنشاء هذه الدالة
from .utils.excel_item_status_report import generate_excel_item_status  # تأكد من إنشاء هذه الدالة
from .utils.pdf_warehouse_status_report import generate_pdf_warehouse_status  # تأكد من إنشاء هذه الدالة
from .utils.excel_warehouse_status_report import generate_excel_warehouse_status  # تأكد من إنشاء هذه الدالة

from .utils.generate_pdf_report_beneficiary import generate_pdf_report_beneficiary  # تأكد من إنشاء هذه الدالة
from .utils.generate_excel_report_beneficiary import generate_excel_report_beneficiary  # تأكد من إنشاء هذه الدالة

from django.contrib import messages




def inventory_report(request):
    report_data = None
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get('end_date', None)
    warehouse_id = request.POST.get('warehouse', None)

    if request.method == "POST" and (start_date and end_date and warehouse_id):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            pass

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

        if 'generate_pdf' in request.POST:
            pdf = generate_pdf(report_data, warehouse_id, start_date, end_date)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'
            response.write(pdf)
            return response

        elif 'generate_excel' in request.POST:
            output = generate_excel(report_data)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="inventory_report.xlsx"'
            return response

    warehouses = Warehouse.objects.all()
    return render(request, 'report/inventory_report_form.html', {
        'warehouses': warehouses,
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'warehouse_id': warehouse_id,
    })










def inventory_report_item(request):
    report_data = None
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get('end_date', None)
    item_id = request.POST.get('item', None)

    if request.method == "POST" and (start_date and end_date and item_id):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            pass

        receiving_data = Receiving.objects.filter(
            item_id=item_id,
            receiving_date__range=[start_date, end_date]
        )
        dispatch_data = Dispatch.objects.filter(
            item_id=item_id,
            dispatch_date__range=[start_date, end_date]
        )
        return_data = ReceivingReturn.objects.filter(
            item_id=item_id,
            return_date__range=[start_date, end_date]
        )
        damage_data = DamageOperation.objects.filter(
            item_id=item_id,
            damage_date__range=[start_date, end_date]
        )

        report_data = {
            'Receiving': receiving_data,
            'Dispatch': dispatch_data,
            'Return': return_data,
            'Damage': damage_data,
        }

        if 'generate_pdf_item' in request.POST:
            pdf = generate_pdf_item(report_data, item_id, start_date, end_date)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="inventory_report_item.pdf"'
            response.write(pdf)
            return response

        elif 'generate_excel_item' in request.POST:
            output = generate_excel_item(report_data)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="inventory_report_item.xlsx"'
            return response

    items= Item.objects.all()
    return render(request, 'report/inventory_report_form_item.html', {
        'items': items,
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'item_id': item_id,
    })




def warehouse_status_report(request):
    report_data = None
    warehouse_id = request.POST.get('warehouse', None)

    if request.method == "POST" and warehouse_id:
        # جلب بيانات الأصناف المتوفرة في المخزن المحدد
        warehouse = Warehouse.objects.get(id=warehouse_id)
        items_in_warehouse = Item.objects.filter(warehouse_id=warehouse_id)

        report_data = {
            'Warehouse': warehouse,
            'Items': items_in_warehouse,
        }

        # توليد تقرير PDF
        
        if 'generate_pdf_warehouse_status' in request.POST:
            pdf = generate_pdf_warehouse_status(report_data)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="warehouse_status_report.pdf"'
            response.write(pdf)
            return response

        # توليد تقرير Excel
        elif 'generate_excel_warehouse_status' in request.POST:
            output = generate_excel_warehouse_status(report_data)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="warehouse_status_report.xlsx"'
            return response

    # جلب قائمة المخازن لعرضها في النموذج
    warehouses = Warehouse.objects.all()
    return render(request, 'report/warehouse_status_report_form.html', {
        'warehouses': warehouses,
        'report_data': report_data,
        'warehouse_id': warehouse_id,
    })




def item_status_report(request):
    report_data = None
    item_id = request.POST.get('item', None)

    if request.method == "POST" and item_id:
        try:
            # جلب بيانات الصنف المحدد
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            messages.error(request, "الصنف غير موجود.")
            return redirect('item_status_report')

        # جلب بيانات الكميات المتوفرة للصنف في جميع المخازن
        stock_items = StockItem.objects.filter(item=item)

        report_data = {
            'Item': item,
            'StockItems': stock_items,
        }

        # توليد تقرير PDF
        if 'generate_pdf_item_status' in request.POST:
            pdf = generate_pdf_item_status(report_data)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="item_status_report.pdf"'
            response.write(pdf)
            return response

        # توليد تقرير Excel
        elif 'generate_excel_item_status' in request.POST:
            output = generate_excel_item_status(report_data)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="item_status_report.xlsx"'
            return response

    # جلب قائمة الأصناف لعرضها في النموذج
    items = Item.objects.all()
    return render(request, 'report/item_status_report_form.html', {
        'items': items,
        'report_data': report_data,
        'item_id': item_id,
    })




 
def inventory_report_beneficiary(request):
    report_data = None
    start_date = request.POST.get('start_date', None)
    end_date = request.POST.get('end_date', None)
    beneficiary_id = request.POST.get('beneficiary', None)

    if request.method == "POST" and (start_date and end_date and beneficiary_id):
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            pass

        # تصفية عمليات الصادر بناءً على المستفيد والفترة الزمنية
        dispatch_data = Dispatch.objects.filter(
            dispatch_date__range=[start_date, end_date],
            beneficiary_id=beneficiary_id
        )

        # إعداد البيانات التي سيتم عرضها في التقرير
        report_data = {
            'Dispatch': dispatch_data,
        }

        # توليد تقرير PDF
        if 'generate_pdf_report_beneficiary' in request.POST:
            pdf = generate_pdf_report_beneficiary(report_data, beneficiary_id, start_date, end_date)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="dispatch_report.pdf"'
            response.write(pdf)
            return response
        # توليد تقرير Excel
        elif 'generate_excel_report_beneficiary' in request.POST:
            output = generate_excel_report_beneficiary(report_data)
            response = HttpResponse(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="dispatch_report.xlsx"'
            return response

    # جلب المستفيدين لعرضهم في النموذج
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'report/inventory_report_form_beneficiary.html', {
        'beneficiaries': beneficiaries,
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
        'beneficiary_id': beneficiary_id,
    })
