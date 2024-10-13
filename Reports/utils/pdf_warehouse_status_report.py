from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf_warehouse_status(report_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # عنوان التقرير
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "تقرير حالة مخزن")

    # معلومات المخزن
    p.setFont("Helvetica", 12)
    p.drawString(100, height - 80, f"اسم المخزن: {report_data['Warehouse'].name}")

    # جدول الكميات في الأصناف
    p.drawString(100, height - 110, "اسم الصنف")
    p.drawString(400, height - 110, "الكميات المتوفرة")

    y = height - 130
    for item in report_data['Items']:
        p.drawString(100, y, item.name)
        p.drawString(400, y, str(item.quantity_in_stock))
        y -= 20
        if y < 50:
            p.showPage()
            y = height - 50

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer.getvalue()






