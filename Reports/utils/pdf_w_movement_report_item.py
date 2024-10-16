



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from io import BytesIO
import os
import arabic_reshaper
from bidi.algorithm import get_display
from Enventory.models import Warehouse,Item,StockItem
from reportlab.lib.units import cm

# دالة لرسم النص من اليمين لليسار باستخدام Arabic Reshaper و Bidi
def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# دالة لإنشاء الجدول
def create_table(data, headers, pdf_canvas, x_offset, y_offset, col_widths):
    reshaped_headers = [reshape_arabic_text(header) for header in headers]
    
    reshaped_data = []
    for row in data:
        reshaped_row = [reshape_arabic_text(str(cell)) for cell in row]
        reshaped_data.append(reshaped_row)
    
    table_data = [reshaped_headers] + reshaped_data
    table = Table(table_data, colWidths=col_widths)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'sky'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    # رسم الجدول في مكانه
    table.wrapOn(pdf_canvas, x_offset, y_offset)
    table.drawOn(pdf_canvas, x_offset, y_offset)

    # حساب ارتفاع الجدول
    row_height = 20  # ارتفاع الصف الواحد
    total_height = row_height * (len(table_data) + 1)  # حساب ارتفاع الجدول
    return total_height  # إرجاع ارتفاع الجدول

# دالة توليد ملف PDF
def generate_pdf_item(report_data, item_id, start_date, end_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    font_path = os.path.join('static', 'fonts', 'sky.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('sky', font_path))
        p.setFont('sky', 12)
    else:
        raise FileNotFoundError("خط sky لم يتم العثور عليه.")

    # عرض عنوان التقرير
    title_text = f"تقرير الصنف: {Item.objects.get(id=item_id).name}"
    date_text = f"من تاريخ: {start_date} إلى تاريخ: {end_date}"
    date_tex = f"تفاصيل العمليات:"

    # تحديد موضع العنوان
    title_y_offset = 800
    date_y_offset = 780

    # رسم العنوان بشكل صحيح من اليمين لليسار
    p.drawRightString(550, title_y_offset, reshape_arabic_text(title_text))
    p.drawRightString(550, date_y_offset, reshape_arabic_text(date_text))
    y_offset = 700  # تعريف موضع بداية الجدول

    
    # عرض البيانات كجداول لكل عملية
    for section, data in report_data.items():
        title = ""

        if section == 'Receiving':
            title = "عمليات الاستلام"

            headers = ['التاريخ', 'الكميةالمستوردة','الصنف','المخزن', 'المورد']
            table_data = [[row.receiving_date, row.imported_quantity,row.stock_item.item.name,row.warehouse.name, row.supplier.full_name if row.supplier else 'N/A'] for row in data]
        elif section == 'Dispatch':
            title = "عمليات الشحن"

            headers = ['التاريخ', 'الكميةالصادر','الصنف','المخزن', 'المستفيد']
            table_data = [[row.dispatch_date, row.quantity_dispatched,row.stock_item.item.name,row.warehouse.name, row.beneficiary.full_name if row.beneficiary else 'N/A'] for row in data]
        elif section == 'Return':
            title = "عمليات الإرجاع"

            headers = ['التاريخ', 'الكميةالمرتجع','الصنف','المخزن', 'المورد']
            table_data = [[row.return_date, row.returned_quantity,row.stock_item.item.name,row.warehouse.name, row.supplier.full_name if row.supplier else 'N/A'] for row in data]
        elif section == 'Damage':
            title = "عمليات التلف"

            headers = ['التاريخ', 'الكمية التالفة', 'المخزن ','الصنف']
            table_data = [[row.damage_date, row.damaged_quantity,row.warehouse.name, row.stock_item.item.name if row.stock_item else 'N/A'] for row in data]


        p.drawRightString(550, y_offset, reshape_arabic_text(title))

    # تعديل y_offset بعد رسم العنوان لتجنب التداخل مع الجدول
        y_offset -= 100  # مساحة صغيرة تحت العنوان

        # تحديد عرض الأعمدة لكل جدول
        col_widths = [3 * cm, 3 * cm, 3 * cm,3 * cm]
        
        # رسم الجدول والحصول على ارتفاعه
        table_height = create_table(table_data, headers, p, 80, y_offset, col_widths)

        # تعديل موضع y_offset بناءً على ارتفاع الجدول
        y_offset -= (table_height + 100)  # إضافة مسافة بين الجداول

        # إذا كان y_offset أقل من حد معين، أضف صفحة جديدة
        if y_offset < 50:  # 50 هي المسافة الآمنة
            p.showPage()  # الانتقال إلى صفحة جديدة
            p.setFont('sky', 12)  # إعادة تعيين الخط في الصفحة الجديدة
            title_y_offset = 800
            date_y_offset = 780
            y_offset = 600  # إعادة تعيين موضع y_offset في الصفحة الجديدة
            
            # إعادة عرض العنوان في الصفحة الجديدة
            p.drawRightString(550, title_y_offset, reshape_arabic_text(title_text))
            p.drawRightString(550, date_y_offset, reshape_arabic_text(date_text))

            # إضافة مسافة أعلى الجدول في الصفحة الجديدة
            y_offset -= 20  # مسافة إضافية فوق الجدول

    # إنهاء الصفحة وحفظ الملف
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
