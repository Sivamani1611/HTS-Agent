import pandas as pd
from io import BytesIO
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

class ExportHandler:
    @staticmethod
    def to_excel(data: dict) -> bytes:
        """Export calculation results to Excel"""
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Summary sheet
            summary_data = {
                'Field': ['HTS Code', 'Description', 'CIF Value', 'Total Duty', 'Landed Cost'],
                'Value': [
                    data.get('HTS Code', ''),
                    data.get('Description', ''),
                    data.get('CIF Value', ''),
                    data.get('Total Duty', ''),
                    data.get('Landed Cost', '')
                ]
            }
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Detailed breakdown
            if 'duties' in data:
                duties_data = []
                for duty_type, duty_info in data['duties'].items():
                    duties_data.append({
                        'Duty Type': duty_type,
                        'Rate': duty_info['rate'],
                        'Amount': duty_info['amount']
                    })
                duties_df = pd.DataFrame(duties_data)
                duties_df.to_excel(writer, sheet_name='Duty Breakdown', index=False)
            
            # Cost breakdown
            costs_data = {
                'Component': ['Product Cost', 'Freight', 'Insurance', 'CIF Value', 'Total Duty', 'Landed Cost'],
                'Amount': [
                    data.get('Product Cost', ''),
                    data.get('Freight', ''),
                    data.get('Insurance', ''),
                    data.get('CIF Value', ''),
                    data.get('Total Duty', ''),
                    data.get('Landed Cost', '')
                ]
            }
            costs_df = pd.DataFrame(costs_data)
            costs_df.to_excel(writer, sheet_name='Cost Breakdown', index=False)
            
            # Format the Excel file
            workbook = writer.book
            money_format = workbook.add_format({'num_format': '$#,##0.00'})
            
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_column('A:A', 30)
                worksheet.set_column('B:B', 40)
        
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def to_pdf(data: dict) -> bytes:
        """Export calculation results to PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"HTS Duty Calculation Report", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Timestamp
        timestamp = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(timestamp)
        story.append(Spacer(1, 20))
        
        # HTS Information
        hts_info = [
            ['HTS Code:', data.get('HTS Code', 'N/A')],
            ['Description:', data.get('Description', 'N/A')]
        ]
        hts_table = Table(hts_info, colWidths=[100, 400])
        hts_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(hts_table)
        story.append(Spacer(1, 20))
        
        # Cost Breakdown
        cost_heading = Paragraph("Cost Breakdown", styles['Heading2'])
        story.append(cost_heading)
        
        cost_data = [
            ['Component', 'Amount'],
            ['Product Cost', data.get('Product Cost', 'N/A')],
            ['Freight', data.get('Freight', 'N/A')],
            ['Insurance', data.get('Insurance', 'N/A')],
            ['CIF Value', data.get('CIF Value', 'N/A')]
        ]
        
        cost_table = Table(cost_data, colWidths=[200, 200])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cost_table)
        story.append(Spacer(1, 20))
        
        # Duty Breakdown
        if 'duties' in data:
            duty_heading = Paragraph("Duty Breakdown", styles['Heading2'])
            story.append(duty_heading)
            
            duty_data = [['Duty Type', 'Rate', 'Amount']]
            for duty_type, duty_info in data['duties'].items():
                duty_data.append([duty_type, duty_info['rate'], duty_info['amount']])
            
            duty_table = Table(duty_data, colWidths=[200, 100, 100])
            duty_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(duty_table)
            story.append(Spacer(1, 20))
        
        # Final Summary
        summary_heading = Paragraph("Summary", styles['Heading2'])
        story.append(summary_heading)
        
        summary_data = [
            ['Total Duty', data.get('Total Duty', 'N/A')],
            ['Landed Cost', data.get('Landed Cost', 'N/A')]
        ]
        
        if 'Final Total Cost' in data:
            summary_data.append(['Final Total Cost', data.get('Final Total Cost', 'N/A')])
        
        summary_table = Table(summary_data, colWidths=[200, 200])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(summary_table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()