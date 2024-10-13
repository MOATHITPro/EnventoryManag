from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf_item_status(report_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # عنوان التقرير
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "تقرير حالة الصنف في المخازن")

    # معلومات الصنف
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"اسم الصنف: {report_data['Item'].name}")

    # جدول الكميات في المخازن
    p.drawString(100, height - 110, "المخزن")
    p.drawString(300, height - 110, "الوحدة")
    p.drawString(400, height - 110, "الكميات المتوفرة")

    y = height - 130
    for stock in report_data['StockItems']:
        p.drawString(100, y, stock.warehouse.name)
        p.drawString(300, y, stock.unit)
        p.drawString(400, y, str(stock.current_quantity))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()
