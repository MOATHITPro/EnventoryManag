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

# Function to reshape Arabic text for right-to-left display
def reshape_arabic_text(text):
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

# Function to create and style the table
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

    # Draw table on the canvas
    table.wrapOn(pdf_canvas, x_offset, y_offset)
    table.drawOn(pdf_canvas, x_offset, y_offset)

    # Calculate table height
    row_height = 20  # Height per row
    total_height = row_height * (len(table_data) + 1)  # Total table height
    return total_height

# Function to generate the PDF
def generate_pdf_item_status(report_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Font setup
    font_path = os.path.join('static', 'fonts', 'sky.ttf')
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('sky', font_path))
        p.setFont('sky', 12)
    else:
        raise FileNotFoundError("Font 'sky' not found.")

    # Report title and item information
    # item_name_text = f"اسم الصنف: {reshape_arabic_text(report_data['Item'].name)}"
    


    title_text = "تقرير حالة الصنف في المخازن"
    item_name_text = f"اسم الصنف: {report_data['Item'].name}"
    p.drawRightString(550, 780, reshape_arabic_text(item_name_text))




    title_y_offset = 800
    item_name_y_offset = 780

    # Draw title and item name
    p.drawRightString(550, title_y_offset, reshape_arabic_text(title_text))
    # p.drawRightString(550, item_name_y_offset, item_name_text)

    # Table headers and data
    headers = ['المخزن', 'الوحدة', 'الكميات المتوفرة']
    table_data = [[stock.warehouse.name, stock.unit, stock.current_quantity] for stock in report_data['StockItems']]
    
    # Table position and column widths
    y_offset = 700
    col_widths = [5 * cm, 3 * cm, 3 * cm]

    # Draw the table and get its height
    table_height = create_table(table_data, headers, p, 80, y_offset, col_widths)

    # Adjust y_offset based on the height of the table
    y_offset -= (table_height + 100)

    # If y_offset is too low, start a new page
    if y_offset < 50:
        p.showPage()
        p.setFont('sky', 12)
        y_offset = 600

        # Redraw title and item name on the new page
        p.drawRightString(550, 800, reshape_arabic_text(title_text))
        p.drawRightString(550, 780, item_name_text)

    # Finish the PDF and return it
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
