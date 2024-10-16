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
def generate_pdf_warehouse_status(report_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    font_path = os.path.join('static', 'fonts', 'sky.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('sky', font_path))
        p.setFont('sky', 12)
    else:
        raise FileNotFoundError("خط sky لم يتم العثور عليه.")

    # عرض عنوان التقرير
    title_text = "تقرير حالة مخزن"
    p.drawRightString(550, 800, reshape_arabic_text(title_text))
    
    warehouse_name_text = f"اسم المخزن: {report_data['Warehouse'].name}"
    p.drawRightString(550, 780, reshape_arabic_text(warehouse_name_text))
    
    y_offset = 700  # تحديد موضع الجدول

    # جدول الكميات في الأصناف
    headers = ['اسم الصنف', 'الكميات المتوفرة']
    table_data = [(stock_item.item, stock_item.current_quantity) for stock_item in report_data['StockItems']]
    



    
    col_widths = [8 * cm, 3 * cm]
    table_height = create_table(table_data, headers, p, 80, y_offset, col_widths)

    # إنهاء الصفحة وحفظ الملف
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf






