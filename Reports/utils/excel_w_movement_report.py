import pandas as pd
from io import BytesIO
from openpyxl import Workbook

def generate_excel(report_data):
    all_rows = []

    for row in report_data['Receiving']:
        all_rows.append({
            "نوع العملية": "Receiving",
            "التاريخ": row.receiving_date,
            "رقم الوثيقة": row.document_number,
            "المورد أو المستفيد": row.supplier.full_name if row.supplier else "N/A",
            "الكمية": row.imported_quantity
        })

    for row in report_data['Dispatch']:
        all_rows.append({
            "نوع العملية": "Dispatch",
            "التاريخ": row.dispatch_date,
            "رقم الوثيقة": row.document_number,
            "المورد أو المستفيد": row.beneficiary.full_name if row.beneficiary else "N/A",
            "الكمية": row.quantity_dispatched
        })

    for row in report_data['Return']:
        all_rows.append({
            "نوع العملية": "Return",
            "التاريخ": row.return_date,
            "رقم الوثيقة": row.document_number,
            "المورد أو المستفيد": row.supplier.full_name if row.supplier else "N/A",
            "الكمية": row.returned_quantity
        })

    for row in report_data['Damage']:
        all_rows.append({
            "نوع العملية": "Damage",
            "التاريخ": row.damage_date,
            "رقم الوثيقة": row.document_number,
            "الصنف": row.stock_item.item.name if row.stock_item and row.stock_item.item else "N/A",  # الصنف من StockItem
            "الكمية": row.damaged_quantity
        })

    df = pd.DataFrame(all_rows)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Inventory Report')
    output.seek(0)
    return output
