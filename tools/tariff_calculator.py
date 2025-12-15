import sqlite3
import pandas as pd
import re
import json

class TariffCalculator:
    def __init__(self, db_path="data/hts.db"):
        self.db_path = db_path
    
    def parse_duty_advanced(self, duty_str, unit_weight=None, quantity=None, cif_value=1.0):
        """Parse duty strings and calculate rates"""
        if pd.isna(duty_str) or duty_str.strip() == "":
            return 0.0
        
        duty_str = duty_str.strip().lower()
        
        if "free" in duty_str:
            return 0.0
        
        # Percentage duty (e.g., '5%')
        match = re.search(r"([\d.]+)\s*%", duty_str)
        if match:
            return float(match.group(1)) / 100
        
        # Weight-based duty (e.g., '2.5¢/kg')
        match = re.search(r"([\d.]+)\s*¢/kg", duty_str)
        if match and unit_weight is not None:
            cents_per_kg = float(match.group(1))
            return (cents_per_kg * unit_weight) / (100 * cif_value)
        
        # Unit-based duty (e.g., '$1.00/unit')
        match = re.search(r"\$([\d.]+)/unit", duty_str)
        if match and quantity is not None:
            dollars_per_unit = float(match.group(1))
            return (dollars_per_unit * quantity) / cif_value
        
        return 0.0
    
    def calculate_duty(self, hts_code, product_cost, freight, insurance, unit_weight, quantity):
        """Calculate duties for a given HTS code and product details"""
        cif_value = product_cost + freight + insurance
        
        # Query database
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"SELECT * FROM hts_data WHERE \"HTS Number\" = '{hts_code}'"
            df = pd.read_sql_query(query, conn)
            conn.close()
        except Exception as e:
            return {"error": f"Database error: {str(e)}. Run process_hts.py first."}
        
        if df.empty:
            return {"error": f"No data found for HTS code {hts_code}"}
        
        # Calculate duties
        row = df.iloc[0]
        result = {
            "HTS Code": hts_code,
            "Description": row.get("Description", "N/A"),
            "CIF Value": f"${cif_value:,.2f}",
            "Product Cost": f"${product_cost:,.2f}",
            "Freight": f"${freight:,.2f}",
            "Insurance": f"${insurance:,.2f}",
            "duties": {}
        }
        
        total_duty = 0.0
        duty_columns = ["General Rate of Duty", "Special Rate of Duty", "Column 2 Rate of Duty"]
        
        for col in duty_columns:
            if col in row:
                duty_rate = self.parse_duty_advanced(
                    row[col], unit_weight, quantity, cif_value
                )
                duty_amount = duty_rate * cif_value
                result["duties"][col] = {
                    "rate": f"{duty_rate * 100:.2f}%" if duty_rate > 0 else "Free",
                    "amount": f"${duty_amount:,.2f}"
                }
                if col == "General Rate of Duty":  # Use general rate for calculation
                    total_duty = duty_amount
        
        result["Total Duty"] = f"${total_duty:,.2f}"
        result["Landed Cost"] = f"${(cif_value + total_duty):,.2f}"
        
        return result

if __name__ == "__main__":
    # Test the calculator
    calc = TariffCalculator()
    
    # Test calculation
    result = calc.calculate_duty(
        hts_code="0101.30.00.00",
        product_cost=10000,
        freight=500,
        insurance=100,
        unit_weight=500,
        quantity=5
    )
    
    print(json.dumps(result, indent=2))