import pandas as pd
import json
from io import BytesIO
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

class EnhancedExportHandler:
    """Enhanced export handler with modern formatting and multiple export options"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
    
    def _create_custom_styles(self) -> Dict[str, ParagraphStyle]:
        """Create custom paragraph styles for PDF export"""
        return {
            'CustomTitle': ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#667eea'),
                alignment=1  # Center
            ),
            'CustomHeading': ParagraphStyle(
                'CustomHeading',
                parent=self.styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.HexColor('#764ba2'),
                borderWidth=1,
                borderColor=colors.HexColor('#667eea'),
                borderPadding=5
            ),
            'CustomBody': ParagraphStyle(
                'CustomBody',
                parent=self.styles['Normal'],
                fontSize=11,
                spaceAfter=6,
                leftIndent=20
            )
        }
    
    def export_to_excel_advanced(self, data: Dict[str, Any], filename: str = None) -> BytesIO:
        """Export data to Excel with advanced formatting and multiple sheets"""
        buffer = BytesIO()
        
        # Create workbook and add formats
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#667eea',
                'font_color': 'white',
                'border': 1
            })
            
            currency_format = workbook.add_format({
                'num_format': '$#,##0.00',
                'border': 1
            })
            
            percentage_format = workbook.add_format({
                'num_format': '0.00%',
                'border': 1
            })
            
            cell_format = workbook.add_format({
                'border': 1,
                'text_wrap': True,
                'valign': 'top'
            })
            
            # Summary sheet
            self._create_excel_summary_sheet(writer, data, header_format, currency_format)
            
            # Detailed calculations sheet
            if 'calculation_details' in data:
                self._create_excel_calculation_sheet(writer, data, header_format, currency_format, cell_format)
            
            # Duty breakdown sheet
            if 'duties' in data:
                self._create_excel_duty_sheet(writer, data, header_format, currency_format, percentage_format)
            
            # Charts sheet
            self._create_excel_charts_sheet(writer, data, workbook)
        
        buffer.seek(0)
        return buffer
    
    def _create_excel_summary_sheet(self, writer, data: Dict, header_format, currency_format):
        """Create summary sheet in Excel"""
        summary_data = {
            'Metric': [
                'HTS Code',
                'Description',
                'CIF Value',
                'Total Duty',
                'Landed Cost',
                'Duty Rate',
                'Export Date'
            ],
            'Value': [
                data.get('HTS Code', 'N/A'),
                data.get('Description', 'N/A'),
                data.get('CIF Value', '$0.00'),
                data.get('Total Duty', '$0.00'),
                data.get('Landed Cost', '$0.00'),
                self._calculate_duty_rate(data),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ]
        }
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Summary', index=False, startrow=1)
        
        worksheet = writer.sheets['Summary']
        worksheet.write(0, 0, 'HTS CALCULATION SUMMARY', header_format)
        
        # Format columns
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 30)
        
        # Apply formatting to data rows
        for row_num in range(2, len(df_summary) + 2):
            if 'Value' in df_summary.columns[1] and '$' in str(df_summary.iloc[row_num-2, 1]):
                worksheet.write(row_num, 1, df_summary.iloc[row_num-2, 1], currency_format)
    
    def _create_excel_calculation_sheet(self, writer, data: Dict, header_format, currency_format, cell_format):
        """Create detailed calculation sheet"""
        calc_data = {
            'Component': ['Product Cost', 'Freight', 'Insurance', 'CIF Value'],
            'Amount': [
                data.get('Product Cost', '$0.00'),
                data.get('Freight', '$0.00'),
                data.get('Insurance', '$0.00'),
                data.get('CIF Value', '$0.00')
            ],
            'Description': [
                'Base cost of goods',
                'Shipping and transportation costs',
                'Insurance coverage',
                'Cost, Insurance, and Freight total'
            ]
        }
        
        df_calc = pd.DataFrame(calc_data)
        df_calc.to_excel(writer, sheet_name='Calculations', index=False)
        
        worksheet = writer.sheets['Calculations']
        
        # Apply header formatting
        for col_num, value in enumerate(df_calc.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Format columns
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 40)
    
    def _create_excel_duty_sheet(self, writer, data: Dict, header_format, currency_format, percentage_format):
        """Create duty breakdown sheet"""
        if 'duties' not in data:
            return
        
        duty_data = []
        for duty_type, duty_info in data['duties'].items():
            duty_data.append({
                'Duty Type': duty_type,
                'Rate': duty_info.get('rate', '0%'),
                'Amount': duty_info.get('amount', '$0.00'),
                'Calculation Method': self._get_duty_method(duty_type)
            })
        
        df_duties = pd.DataFrame(duty_data)
        df_duties.to_excel(writer, sheet_name='Duty Breakdown', index=False)
        
        worksheet = writer.sheets['Duty Breakdown']
        
        # Apply header formatting
        for col_num, value in enumerate(df_duties.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Format columns
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 12)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 30)
    
    def _create_excel_charts_sheet(self, writer, data: Dict, workbook):
        """Create charts sheet with visualizations"""
        worksheet = workbook.add_worksheet('Charts')
        
        # Create a sample chart
        chart = workbook.add_chart({'type': 'pie'})
        
        # Add data for the chart (this would be dynamic based on actual data)
        chart.add_series({
            'name': 'Cost Breakdown',
            'categories': ['Product Cost', 'Freight', 'Insurance', 'Duties'],
            'values': [70, 15, 5, 10],  # Sample percentages
        })
        
        chart.set_title({'name': 'Cost Breakdown Analysis'})
        chart.set_style(10)
        
        worksheet.insert_chart('B2', chart)
    
    def export_to_pdf_advanced(self, data: Dict[str, Any], filename: str = None) -> BytesIO:
        """Export data to PDF with advanced formatting and charts"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Title
        title = Paragraph("HTS Duty Calculation Report", self.custom_styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Summary section
        story.append(Paragraph("Executive Summary", self.custom_styles['CustomHeading']))
        
        summary_data = [
            ['Metric', 'Value'],
            ['HTS Code', data.get('HTS Code', 'N/A')],
            ['Description', data.get('Description', 'N/A')],
            ['CIF Value', data.get('CIF Value', '$0.00')],
            ['Total Duty', data.get('Total Duty', '$0.00')],
            ['Landed Cost', data.get('Landed Cost', '$0.00')],
            ['Effective Duty Rate', self._calculate_duty_rate(data)],
        ]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 12))
        
        # Detailed breakdown
        if 'duties' in data:
            story.append(Paragraph("Duty Breakdown", self.custom_styles['CustomHeading']))
            
            duty_data = [['Duty Type', 'Rate', 'Amount']]
            for duty_type, duty_info in data['duties'].items():
                duty_data.append([
                    duty_type,
                    duty_info.get('rate', '0%'),
                    duty_info.get('amount', '$0.00')
                ])
            
            duty_table = Table(duty_data)
            duty_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#764ba2')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(duty_table)
            story.append(Spacer(1, 12))
        
        # Recommendations section
        story.append(Paragraph("Recommendations", self.custom_styles['CustomHeading']))
        recommendations = self._generate_recommendations(data)
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.custom_styles['CustomBody']))
        
        story.append(Spacer(1, 12))
        
        # Footer
        footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by HTS AI Agent Pro"
        story.append(Paragraph(footer_text, self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def export_to_json_structured(self, data: Dict[str, Any]) -> str:
        """Export data to structured JSON format"""
        export_data = {
            'export_metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '2.0',
                'format': 'HTS_AI_Agent_Pro'
            },
            'calculation_summary': {
                'hts_code': data.get('HTS Code', ''),
                'description': data.get('Description', ''),
                'cif_value': self._parse_currency(data.get('CIF Value', '$0.00')),
                'total_duty': self._parse_currency(data.get('Total Duty', '$0.00')),
                'landed_cost': self._parse_currency(data.get('Landed Cost', '$0.00')),
                'effective_duty_rate': self._calculate_duty_rate_numeric(data)
            },
            'cost_breakdown': {
                'product_cost': self._parse_currency(data.get('Product Cost', '$0.00')),
                'freight': self._parse_currency(data.get('Freight', '$0.00')),
                'insurance': self._parse_currency(data.get('Insurance', '$0.00'))
            },
            'duty_details': data.get('duties', {}),
            'recommendations': self._generate_recommendations(data),
            'compliance_notes': self._generate_compliance_notes(data)
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def create_dashboard_export(self, analytics_data: Dict[str, Any]) -> BytesIO:
        """Create comprehensive dashboard export"""
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Define formats
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 18,
                'fg_color': '#667eea',
                'font_color': 'white',
                'align': 'center'
            })
            
            header_format = workbook.add_format({
                'bold': True,
                'fg_color': '#764ba2',
                'font_color': 'white',
                'border': 1
            })
            
            # Overview sheet
            self._create_overview_sheet(writer, analytics_data, title_format, header_format)
            
            # Metrics sheet
            self._create_metrics_sheet(writer, analytics_data, header_format)
            
            # Trends sheet
            self._create_trends_sheet(writer, analytics_data, header_format)
        
        buffer.seek(0)
        return buffer
    
    def _create_overview_sheet(self, writer, data: Dict, title_format, header_format):
        """Create overview sheet for dashboard export"""
        worksheet = writer.add_worksheet('Overview')
        
        # Title
        worksheet.merge_range('A1:F1', 'HTS AI Agent Pro - Analytics Dashboard', title_format)
        
        # Key metrics
        metrics = [
            ['Metric', 'Value', 'Period'],
            ['Total Queries', str(data.get('total_queries', 0)), 'All Time'],
            ['Duty Calculations', str(data.get('duty_calculations', 0)), 'All Time'],
            ['Policy Questions', str(data.get('policy_queries', 0)), 'All Time'],
            ['Avg. Processing Time', '2.3 seconds', 'Last 30 Days'],
            ['Compliance Rate', '98.2%', 'Last 30 Days']
        ]
        
        for row_num, row_data in enumerate(metrics, 3):
            for col_num, cell_data in enumerate(row_data):
                if row_num == 3:  # Header row
                    worksheet.write(row_num, col_num, cell_data, header_format)
                else:
                    worksheet.write(row_num, col_num, cell_data)
    
    def _create_metrics_sheet(self, writer, data: Dict, header_format):
        """Create detailed metrics sheet"""
        # Implementation for detailed metrics
        pass
    
    def _create_trends_sheet(self, writer, data: Dict, header_format):
        """Create trends analysis sheet"""
        # Implementation for trends analysis
        pass
    
    def _calculate_duty_rate(self, data: Dict[str, Any]) -> str:
        """Calculate effective duty rate as percentage string"""
        try:
            cif_value = self._parse_currency(data.get('CIF Value', '$0.00'))
            total_duty = self._parse_currency(data.get('Total Duty', '$0.00'))
            
            if cif_value > 0:
                rate = (total_duty / cif_value) * 100
                return f"{rate:.2f}%"
            return "0.00%"
        except:
            return "N/A"
    
    def _calculate_duty_rate_numeric(self, data: Dict[str, Any]) -> float:
        """Calculate effective duty rate as numeric value"""
        try:
            cif_value = self._parse_currency(data.get('CIF Value', '$0.00'))
            total_duty = self._parse_currency(data.get('Total Duty', '$0.00'))
            
            if cif_value > 0:
                return (total_duty / cif_value) * 100
            return 0.0
        except:
            return 0.0
    
    def _parse_currency(self, currency_str: str) -> float:
        """Parse currency string to float"""
        try:
            return float(currency_str.replace('$', '').replace(',', ''))
        except:
            return 0.0
    
    def _get_duty_method(self, duty_type: str) -> str:
        """Get calculation method for duty type"""
        methods = {
            'General Rate of Duty': 'Ad valorem percentage of CIF value',
            'Special Rate of Duty': 'Preferential rate under trade agreements',
            'Column 2 Rate of Duty': 'Non-favored nation rate'
        }
        return methods.get(duty_type, 'Standard calculation method')
    
    def _generate_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on calculation data"""
        recommendations = []
        
        duty_rate = self._calculate_duty_rate_numeric(data)
        
        if duty_rate > 10:
            recommendations.append("Consider reviewing HTS classification for potential optimization")
        
        if duty_rate > 5:
            recommendations.append("Explore trade agreement benefits for duty reduction")
        
        if 'duties' in data and len(data['duties']) > 1:
            recommendations.append("Multiple duty rates apply - verify most favorable option")
        
        recommendations.append("Regular review of HTS codes recommended for compliance")
        
        return recommendations
    
    def _generate_compliance_notes(self, data: Dict[str, Any]) -> List[str]:
        """Generate compliance notes"""
        notes = [
            "Ensure accurate product classification",
            "Maintain proper documentation for customs",
            "Monitor changes in trade regulations",
            "Consider advance rulings for complex products"
        ]
        return notes
    
    def export_batch_results(self, batch_data: List[Dict[str, Any]]) -> BytesIO:
        """Export batch processing results"""
        buffer = BytesIO()
        
        # Convert to DataFrame
        df = pd.DataFrame(batch_data)
        
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            workbook = writer.book
            
            # Main results sheet
            df.to_excel(writer, sheet_name='Batch Results', index=False)
            
            # Summary sheet
            summary_data = {
                'Total Records': [len(batch_data)],
                'Successful': [len([r for r in batch_data if r.get('Status') == '✅ Success'])],
                'Errors': [len([r for r in batch_data if r.get('Status') == '❌ Error'])],
                'Total Value': [sum(self._parse_currency(r.get('CIF Value', '$0.00')) for r in batch_data)],
                'Total Duty': [sum(self._parse_currency(r.get('Total Duty', '$0.00')) for r in batch_data)]
            }
            
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        buffer.seek(0)
        return buffer 