#!/usr/bin/env python3
"""
HTS AI Agent - Enhanced Simple CLI Version
Advanced Trade Intelligence & Duty Calculation (No AI Dependencies)
"""

import sys
import json
import csv
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║    🌐 HTS AI AGENT - ENHANCED SIMPLE CLI VERSION                      ║
║                                                                          ║
║    Advanced Trade Intelligence & Duty Calculation Platform              ║
║    Enhanced features without AI dependencies                             ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

class SimpleHTS:
    """Simple HTS Agent without AI dependencies"""
    
    def __init__(self):
        # Sample HTS database
        self.hts_database = {
            "0101.30.00.00": {
                "description": "Live asses",
                "duty_rate": 0.0,
                "category": "Live Animals",
                "units": "Number"
            },
            "0102.21.00.00": {
                "description": "Live cattle, purebred breeding animals",
                "duty_rate": 0.025,
                "category": "Live Animals",
                "units": "Number"
            },
            "0201.10.00.00": {
                "description": "Beef carcasses and half-carcasses, fresh or chilled",
                "duty_rate": 0.044,
                "category": "Meat Products",
                "units": "kg"
            },
            "0301.11.00.00": {
                "description": "Ornamental fish",
                "duty_rate": 0.0,
                "category": "Fish",
                "units": "Number"
            },
            "0401.10.00.00": {
                "description": "Milk, not concentrated, not sweetened, fat content ≤ 1%",
                "duty_rate": 0.038,
                "category": "Dairy",
                "units": "Liter"
            }
        }
        
        # Knowledge base for questions
        self.knowledge_base = {
            "gsp": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
            "generalized system of preferences": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
            "hts": "The Harmonized Tariff Schedule (HTS) is a standardized numerical method of classifying traded products used by customs authorities around the world.",
            "duty": "Import duties are taxes imposed by customs authorities on goods when they are transported across international borders.",
            "cif": "CIF (Cost, Insurance, and Freight) is the total cost of goods including the cost of the goods, insurance, and freight charges.",
            "nafta": "NAFTA (now USMCA) provides preferential tariff treatment for qualifying goods originating in Canada, Mexico, and the United States.",
            "usmca": "The United States-Mexico-Canada Agreement (USMCA) replaced NAFTA and provides preferential tariff treatment for qualifying goods.",
            "fta": "Free Trade Agreements (FTAs) are treaties between countries that reduce or eliminate trade barriers between participating nations."
        }
    
    def answer_question(self, question):
        """Answer trade policy questions"""
        question_lower = question.lower()
        
        # Check knowledge base
        for key, answer in self.knowledge_base.items():
            if key in question_lower:
                return answer
        
        # Check for HTS code specific questions
        for hts_code, info in self.hts_database.items():
            if hts_code in question:
                return f"HTS Code {hts_code}: {info['description']} | Duty Rate: {info['duty_rate']*100:.1f}% | Category: {info['category']}"
        
        return "I don't have specific information about that. Try asking about GSP, HTS codes, duties, CIF, NAFTA/USMCA, or FTA."
    
    def calculate_duty(self, hts_code, product_cost, freight=0, insurance=0, weight=0, quantity=1):
        """Calculate duty for given parameters"""
        # Calculate CIF value
        cif_value = product_cost + freight + insurance
        
        # Get HTS info
        hts_info = self.hts_database.get(hts_code)
        if not hts_info:
            return {
                "error": f"HTS code {hts_code} not found in database",
                "available_codes": list(self.hts_database.keys())
            }
        
        # Calculate duty
        duty_rate = hts_info["duty_rate"]
        duty_amount = cif_value * duty_rate
        landed_cost = cif_value + duty_amount
        
        return {
            "hts_code": hts_code,
            "description": hts_info["description"],
            "category": hts_info["category"],
            "product_cost": product_cost,
            "freight": freight,
            "insurance": insurance,
            "cif_value": cif_value,
            "duty_rate": f"{duty_rate*100:.1f}%",
            "duty_amount": duty_amount,
            "landed_cost": landed_cost,
            "calculation_date": datetime.now().isoformat()
        }
    
    def list_hts_codes(self):
        """List available HTS codes"""
        print("\n📋 Available HTS Codes:")
        print("=" * 80)
        for code, info in self.hts_database.items():
            print(f"{code} | {info['description'][:50]:<50} | {info['duty_rate']*100:>6.1f}%")
        print("=" * 80)
    
    def search_codes(self, search_term: str) -> List[Tuple[str, Dict]]:
        """Search HTS codes by keyword"""
        search_lower = search_term.lower()
        matches = []
        
        for code, info in self.hts_database.items():
            if (search_lower in info['description'].lower() or 
                search_lower in info['category'].lower() or
                search_lower in code.lower()):
                matches.append((code, info))
        
        return matches
    
    def compare_codes(self, codes: List[str]) -> Dict:
        """Compare multiple HTS codes"""
        comparison = {
            "valid_codes": [],
            "invalid_codes": [],
            "comparison_data": []
        }
        
        for code in codes:
            if code in self.hts_database:
                comparison["valid_codes"].append(code)
                info = self.hts_database[code]
                comparison["comparison_data"].append({
                    "code": code,
                    "description": info["description"],
                    "duty_rate": info["duty_rate"],
                    "category": info["category"]
                })
            else:
                comparison["invalid_codes"].append(code)
        
        # Sort by duty rate
        comparison["comparison_data"].sort(key=lambda x: x["duty_rate"])
        return comparison
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        categories = {}
        duty_rates = []
        
        for code, info in self.hts_database.items():
            category = info['category']
            categories[category] = categories.get(category, 0) + 1
            duty_rates.append(info['duty_rate'])
        
        return {
            "total_codes": len(self.hts_database),
            "categories": categories,
            "duty_stats": {
                "average": sum(duty_rates) / len(duty_rates),
                "minimum": min(duty_rates),
                "maximum": max(duty_rates),
                "free_duty_count": len([r for r in duty_rates if r == 0])
            }
        }
    
    def export_database(self, format_type: str = 'json') -> str:
        """Export database to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type.lower() == 'json':
            filename = f"hts_database_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(self.hts_database, f, indent=2)
        
        elif format_type.lower() == 'csv':
            filename = f"hts_database_{timestamp}.csv"
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['HTS_Code', 'Description', 'Duty_Rate_Percent', 'Category', 'Units'])
                for code, info in self.hts_database.items():
                    writer.writerow([
                        code, 
                        info['description'], 
                        f"{info['duty_rate']*100:.2f}", 
                        info['category'], 
                        info['units']
                    ])
        
        return filename
    
    def process_batch_file(self, filename: str) -> Dict:
        """Process batch calculations from CSV"""
        results = {"processed": [], "errors": []}
        
        try:
            with open(filename, 'r', newline='') as f:
                reader = csv.DictReader(f)
                
                for i, row in enumerate(reader, 1):
                    try:
                        hts_code = row['hts_code']
                        product_cost = float(row['product_cost'])
                        freight = float(row.get('freight', 0))
                        insurance = float(row.get('insurance', 0))
                        
                        calc_result = self.calculate_duty(hts_code, product_cost, freight, insurance)
                        
                        if 'error' not in calc_result:
                            calc_result['row'] = i
                            results["processed"].append(calc_result)
                        else:
                            results["errors"].append(f"Row {i}: {calc_result['error']}")
                            
                    except Exception as e:
                        results["errors"].append(f"Row {i}: {str(e)}")
                        
        except FileNotFoundError:
            results["errors"].append(f"File '{filename}' not found")
        except Exception as e:
            results["errors"].append(f"Error reading file: {str(e)}")
        
        return results
    
    def generate_batch_template(self) -> str:
        """Generate CSV template for batch processing"""
        filename = "hts_batch_template.csv"
        sample_codes = list(self.hts_database.keys())[:3]
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['hts_code', 'product_cost', 'freight', 'insurance', 'description'])
            
            for code in sample_codes:
                writer.writerow([code, '10000', '500', '100', f'Sample product for {code}'])
        
        return filename

def main():
    """Main CLI function"""
    print_banner()
    agent = SimpleHTS()
    
    print("Welcome to the Simple HTS Agent CLI!")
    print("Type 'help' for commands, 'exit' to quit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input("\n🌐 HTS Agent> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thank you for using HTS Agent CLI. Goodbye!")
                break
            
            elif user_input.lower() == 'help':
                print_help()
            
            elif user_input.lower() == 'list':
                agent.list_hts_codes()
            
            elif user_input.lower().startswith('calc'):
                handle_calculation(agent, user_input)
            
            elif user_input.lower().startswith('search'):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("❌ Usage: search <keyword>")
                else:
                    matches = agent.search_codes(parts[1])
                    if matches:
                        print(f"\n🔍 Found {len(matches)} matches for '{parts[1]}':")
                        print("-" * 60)
                        for code, info in matches:
                            print(f"  {code} | {info['description'][:50]:<50} | {info['duty_rate']*100:>6.1f}% | {info['category']}")
                    else:
                        print(f"❌ No matches found for '{parts[1]}'")
            
            elif user_input.lower().startswith('compare'):
                parts = user_input.split()[1:]
                if len(parts) < 2:
                    print("❌ Usage: compare <hts_code1> <hts_code2> [more_codes...]")
                else:
                    comparison = agent.compare_codes(parts)
                    if comparison["comparison_data"]:
                        print(f"\n📊 Comparing {len(comparison['comparison_data'])} HTS codes:")
                        print("-" * 80)
                        print(f"{'HTS Code':<15} | {'Description':<40} | {'Duty Rate':<10} | {'Category'}")
                        print("-" * 80)
                        for item in comparison["comparison_data"]:
                            print(f"{item['code']:<15} | {item['description'][:40]:<40} | {item['duty_rate']*100:>8.1f}% | {item['category']}")
                    
                    if comparison["invalid_codes"]:
                        print(f"\n❌ Invalid codes: {', '.join(comparison['invalid_codes'])}")
            
            elif user_input.lower() == 'stats':
                stats = agent.get_statistics()
                print(f"\n📊 HTS Database Statistics")
                print("-" * 40)
                print(f"Total HTS Codes: {stats['total_codes']}")
                print(f"\nCategories:")
                for category, count in stats['categories'].items():
                    print(f"  {category}: {count} codes")
                print(f"\nDuty Rate Statistics:")
                print(f"  Average: {stats['duty_stats']['average']*100:.2f}%")
                print(f"  Minimum: {stats['duty_stats']['minimum']*100:.2f}%")
                print(f"  Maximum: {stats['duty_stats']['maximum']*100:.2f}%")
                print(f"  Free Duty Codes: {stats['duty_stats']['free_duty_count']}")
            
            elif user_input.lower().startswith('export'):
                parts = user_input.split()
                if len(parts) < 2 or parts[1] not in ['json', 'csv']:
                    print("❌ Usage: export <json|csv>")
                else:
                    filename = agent.export_database(parts[1])
                    print(f"📁 Database exported to: {filename}")
            
            elif user_input.lower() == 'template':
                filename = agent.generate_batch_template()
                print(f"📁 Batch template created: {filename}")
                print("Fill in your data and use 'batch <filename>' to process it")
            
            elif user_input.lower().startswith('batch'):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("❌ Usage: batch <csv_filename>")
                else:
                    results = agent.process_batch_file(parts[1])
                    
                    if results["processed"]:
                        print(f"\n📊 Processed {len(results['processed'])} calculations:")
                        for calc in results["processed"]:
                            print(f"  Row {calc['row']}: {calc['hts_code']} - Duty: ${calc['duty_amount']:,.2f}")
                        
                        # Save results
                        output_file = parts[1].replace('.csv', '_results.json')
                        with open(output_file, 'w') as f:
                            json.dump(results["processed"], f, indent=2)
                        print(f"📁 Results saved to: {output_file}")
                    
                    if results["errors"]:
                        print(f"\n❌ Errors encountered:")
                        for error in results["errors"]:
                            print(f"  {error}")
            
            elif user_input.lower().startswith('question') or user_input.startswith('?'):
                question = user_input[8:] if user_input.lower().startswith('question') else user_input[1:]
                answer = agent.answer_question(question.strip())
                print(f"\n💡 Answer: {answer}")
            
            else:
                # Try to answer as a question first
                answer = agent.answer_question(user_input)
                if "don't have specific information" not in answer:
                    print(f"\n💡 Answer: {answer}")
                else:
                    print(f"\n❓ Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def print_help():
    """Print help information"""
    help_text = """
📖 HTS Agent Enhanced CLI Commands:

Basic Commands:
  help                     - Show this help message
  list                     - List all available HTS codes
  search <keyword>         - Search HTS codes by keyword
  compare <code1> <code2>  - Compare duty rates for multiple codes
  stats                    - Show database statistics
  exit, quit, q           - Exit the application

Data Management:
  export <json|csv>        - Export HTS database to file
  template                 - Generate CSV template for batch processing
  batch <filename>         - Process batch calculations from CSV file

Questions:
  question <your question>  - Ask a trade policy question
  ? <your question>        - Ask a trade policy question (shorthand)
  
  Examples:
    question What is GSP?
    ? Tell me about NAFTA
    What is HTS code 0101.30.00.00?

Calculations:
  calc <hts_code> <product_cost> [freight] [insurance] [weight] [quantity]
  
  Examples:
    calc 0101.30.00.00 10000
    calc 0102.21.00.00 10000 500 100
    calc 0201.10.00.00 8000 400 80 500 2

Available HTS Codes:
  0101.30.00.00  - Live asses (Free)
  0102.21.00.00  - Live cattle, purebred (2.5%)
  0201.10.00.00  - Beef carcasses (4.4%)
  0301.11.00.00  - Ornamental fish (Free)
  0401.10.00.00  - Milk ≤1% fat (3.8%)

Sample Questions:
  - What is GSP?
  - What is the Generalized System of Preferences?
  - Tell me about HTS codes
  - What are import duties?
  - What is CIF?
  - Tell me about NAFTA
  - What is USMCA?
    """
    print(help_text)

def handle_calculation(agent, user_input):
    """Handle duty calculation commands"""
    parts = user_input.split()
    
    if len(parts) < 3:
        print("\n❌ Usage: calc <hts_code> <product_cost> [freight] [insurance] [weight] [quantity]")
        print("Example: calc 0101.30.00.00 10000 500 100")
        return
    
    try:
        hts_code = parts[1]
        product_cost = float(parts[2])
        freight = float(parts[3]) if len(parts) > 3 else 0
        insurance = float(parts[4]) if len(parts) > 4 else 0
        weight = float(parts[5]) if len(parts) > 5 else 0
        quantity = int(parts[6]) if len(parts) > 6 else 1
        
        result = agent.calculate_duty(hts_code, product_cost, freight, insurance, weight, quantity)
        
        if "error" in result:
            print(f"\n❌ Error: {result['error']}")
            if "available_codes" in result:
                print("Available codes:", ", ".join(result['available_codes']))
        else:
            print_calculation_result(result)
    
    except ValueError:
        print("\n❌ Error: Please enter valid numbers for cost, freight, insurance, weight, and quantity")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def print_calculation_result(result):
    """Print formatted calculation result"""
    print("\n" + "=" * 70)
    print("📊 DUTY CALCULATION RESULT")
    print("=" * 70)
    print(f"HTS Code:      {result['hts_code']}")
    print(f"Description:   {result['description']}")
    print(f"Category:      {result['category']}")
    print("-" * 70)
    print(f"Product Cost:  ${result['product_cost']:,.2f}")
    print(f"Freight:       ${result['freight']:,.2f}")
    print(f"Insurance:     ${result['insurance']:,.2f}")
    print(f"CIF Value:     ${result['cif_value']:,.2f}")
    print("-" * 70)
    print(f"Duty Rate:     {result['duty_rate']}")
    print(f"Duty Amount:   ${result['duty_amount']:,.2f}")
    print(f"Landed Cost:   ${result['landed_cost']:,.2f}")
    print("-" * 70)
    print(f"Calculated:    {result['calculation_date'][:19]}")
    print("=" * 70)

if __name__ == "__main__":
    main() 