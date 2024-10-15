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
from Transactions.models import Dispatch,Receiving
from Enventory.models import Beneficiary,Supplier
from reportlab.lib.units import cm

# دالة لمعالجة النصوص العربية
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
        ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
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

# دالة توليد تقرير PDF
def generate_pdf_report_beneficiary(report_data, beneficiary_id, start_date, end_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # مسار الخط
    font_path = os.path.join('static', 'fonts', 'Arial.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        p.setFont('Arial', 12)
    else:
        raise FileNotFoundError("خط Arial لم يتم العثور عليه.")

    # معلومات المستفيد
    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
    title_text = f"تقرير المستفيد: {beneficiary.full_name}"
    date_text = f"فترة التقرير: {start_date} إلى {end_date}"

    # رسم العنوان بشكل صحيح من اليمين لليسار
    title_y_offset = 800
    date_y_offset = 780
    p.drawRightString(550, title_y_offset, reshape_arabic_text(title_text))
    p.drawRightString(550, date_y_offset, reshape_arabic_text(date_text))
    y_offset = 700  # تعريف موضع بداية الجدول

    # إعداد البيانات للجدول
    for section, data in report_data.items():
        if section == 'Dispatch':
            headers = ['التاريخ', 'رقم الوثيقة', 'اسم المسلم', 'المخزن', 'الصنف', 'الكمية المرسلة']
            table_data = [
                [
                    row.dispatch_date,
                    row.document_number,
                    row.recipient_name,
                    row.warehouse.name,
                    row.item.name if row.item else 'N/A',
                    row.quantity_dispatched
                ]
                for row in data
            ]

            y_offset -= 20  # مساحة تحت العنوان
            p.drawRightString(550, y_offset, reshape_arabic_text("  تفاصيل عمليات الصرف:"))

            # تحديد عرض الأعمدة للجدول
            col_widths = [3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm]

            # رسم الجدول والحصول على ارتفاعه
            table_height = create_table(table_data, headers, p, 80, y_offset - 40, col_widths)

            # تعديل موضع y_offset بناءً على ارتفاع الجدول
            y_offset -= (table_height + 60)  # إضافة مسافة بين الجداول

            # إذا كان y_offset أقل من حد معين، أضف صفحة جديدة
            if y_offset < 50:  # 50 هي المسافة الآمنة
                p.showPage()  # الانتقال إلى صفحة جديدة
                p.setFont('Arial', 12)  # إعادة تعيين الخط في الصفحة الجديدة
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











