from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
import os
import arabic_reshaper
from bidi.algorithm import get_display
from Transactions.models import Dispatch
from Enventory.models import Beneficiary

# دالة لمعالجة النصوص العربية
def process_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# دالة لرسم النص من اليمين إلى اليسار
def draw_right_to_left_text(p, text, x, y, font_name='Arial', font_size=12):
    reshaped_text = process_arabic_text(text)
    p.setFont(font_name, font_size)
    p.drawRightString(x, y, reshaped_text)

# دالة توليد تقرير PDF بدون جدول، عرض البيانات بشكل أفقي
def generate_pdf_report_beneficiary(report_data, beneficiary_id, start_date, end_date):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # مسار الخط
    font_path = os.path.join('static', 'fonts', 'Arial.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Arial', font_path))
        p.setFont('Arial', 12)
    else:
        raise FileNotFoundError("خط sky لم يتم العثور عليه.")

    # معلومات المستفيد
    beneficiary = Beneficiary.objects.get(id=beneficiary_id)
    draw_right_to_left_text(p, f"المستفيد: {beneficiary.full_name}", 550, 800)
    draw_right_to_left_text(p, f"فترة التقرير: {start_date} إلى {end_date}", 550, 780)
    draw_right_to_left_text(p, f"فترة التقرير: {start_date} إلى {end_date}", 550, 780)

    draw_right_to_left_text(p, "تفاصيل العمليات:", 550, 760)

    y_offset = 700

   # عرض تفاصيل العمليات
    for section, data in report_data.items():
     if section == 'Dispatch':
        for row in data:
            # معالجة البيانات
            dispatch_date = process_arabic_text(str(row.dispatch_date))
            document_number = process_arabic_text(str(row.document_number))
            recipient_name = process_arabic_text(str(row.recipient_name))
            warehouse_name = process_arabic_text(row.warehouse.name)
            item_name = process_arabic_text(row.item.name if row.item else 'N/A')
            quantity_dispatched = process_arabic_text(str(row.quantity_dispatched))

            # عرض البيانات بنفس تنسيق معلومات المستفيد
            draw_right_to_left_text(p, f"التاريخ: {dispatch_date}", 550, 800 )
            # draw_right_to_left_text(p, dispatch_date, 350, y_offset)
            # draw_right_to_left_text(p, f"المستفيد: {beneficiary.full_name}", 550, 800)

            y_offset -= 20  # الانتقال للسطر التالي

            draw_right_to_left_text(p, f"رقم الوثيقة:", 550, y_offset)
            draw_right_to_left_text(p, document_number, 350, y_offset)

            y_offset -= 20  # الانتقال للسطر التالي

            draw_right_to_left_text(p, f"اسم المسلم:", 550, y_offset)
            draw_right_to_left_text(p, recipient_name, 350, y_offset)

            y_offset -= 20  # الانتقال للسطر التالي

            draw_right_to_left_text(p, f"المخزن:", 550, y_offset)
            draw_right_to_left_text(p, warehouse_name, 350, y_offset)

            y_offset -= 20  # الانتقال للسطر التالي
            draw_right_to_left_text(p, f"الصنف: {item_name}", 350, 550 )

            # draw_right_to_left_text(p, f"الصنف:", 550, y_offset)
            # draw_right_to_left_text(p, item_name, 350, y_offset)

            y_offset -= 20  # الانتقال للسطر التالي

            draw_right_to_left_text(p, f"الكمية المرسلة:", 550, y_offset)
            draw_right_to_left_text(p, quantity_dispatched, 350, y_offset)

            y_offset -= 40  # مسافة بين كل عملية


    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
