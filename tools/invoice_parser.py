import pandas as pd
import json
import PyPDF2
import re
from typing import Dict, Any, Optional

class InvoiceParser:
    def __init__(self):
        self.patterns = {
            'hts_code': r'\b\d{4}\.\d{2}\.\d{2}\.\d{2}\b',
            'amount': r'\$?([\d,]+\.?\d*)',
            'weight': r'(\d+\.?\d*)\s*(kg|lbs?|pounds?)',
            'quantity': r'(\d+)\s*(units?|pieces?|pcs?|items?)'
        }
    
    def parse_file(self, uploaded_file) -> Optional[Dict[str, Any]]:
        """Parse uploaded file and extract relevant data"""
        file_type = uploaded_file.type
        
        if 'csv' in file_type:
            return self.parse_csv(uploaded_file)
        elif 'excel' in file_type or 'spreadsheet' in file_type:
            return self.parse_excel(uploaded_file)
        elif 'pdf' in file_type:
            return self.parse_pdf(uploaded_file)
        elif 'json' in file_type:
            return self.parse_json(uploaded_file)
        else:
            return None
    
    def parse_csv(self, file) -> Dict[str, Any]:
        """Parse CSV file"""
        df = pd.read_csv(file)
        
        # Try to identify columns
        result = {}
        
        # Map common column names
        column_mapping = {
            'hts': ['hts', 'hts code', 'tariff', 'hs code'],
            'product_cost': ['cost', 'price', 'value', 'amount', 'fob'],
            'freight': ['freight', 'shipping', 'transport'],
            'insurance': ['insurance', 'ins'],
            'weight': ['weight', 'kg', 'lbs'],
            'quantity': ['quantity', 'qty', 'units', 'pieces']
        }
        
        for key, possible_names in column_mapping.items():
            for col in df.columns:
                if any(name in col.lower() for name in possible_names):
                    result[key] = df[col].iloc[0] if not df.empty else None
                    break
        
        return self._clean_parsed_data(result)
    
    def parse_excel(self, file) -> Dict[str, Any]:
        """Parse Excel file"""
        df = pd.read_excel(file, sheet_name=0)
        return self.parse_csv(file)  # Reuse CSV logic
    
    def parse_pdf(self, file) -> Dict[str, Any]:
        """Parse PDF file and extract data"""
        result = {}
        
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Extract HTS code
            hts_match = re.search(self.patterns['hts_code'], text)
            if hts_match:
                result['hts_code'] = hts_match.group()
            
            # Extract amounts (take first few as cost, freight, insurance)
            amounts = re.findall(self.patterns['amount'], text)
            if amounts:
                result['product_cost'] = float(amounts[0].replace(',', ''))
                if len(amounts) > 1:
                    result['freight'] = float(amounts[1].replace(',', ''))
                if len(amounts) > 2:
                    result['insurance'] = float(amounts[2].replace(',', ''))
            
            # Extract weight
            weight_match = re.search(self.patterns['weight'], text)
            if weight_match:
                weight = float(weight_match.group(1))
                unit = weight_match.group(2).lower()
                if 'lb' in unit:
                    weight = weight * 0.453592  # Convert to kg
                result['unit_weight'] = weight
            
            # Extract quantity
            qty_match = re.search(self.patterns['quantity'], text)
            if qty_match:
                result['quantity'] = int(qty_match.group(1))
            
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        
        return self._clean_parsed_data(result)
    
    def parse_json(self, file) -> Dict[str, Any]:
        """Parse JSON file"""
        try:
            data = json.load(file)
            return self._clean_parsed_data(data)
        except:
            return {}
    
    def _clean_parsed_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate parsed data"""
        cleaned = {}
        
        # Ensure required fields have default values
        defaults = {
            'hts_code': '0101.30.00.00',
            'product_cost': 0,
            'freight': 0,
            'insurance': 0,
            'unit_weight': 0,
            'quantity': 1
        }
        
        for key, default in defaults.items():
            if key in data and data[key] is not None:
                cleaned[key] = data[key]
            else:
                cleaned[key] = default
        
        return cleaned