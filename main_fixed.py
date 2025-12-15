#!/usr/bin/env python3
"""
HTS AI Agent - Enhanced CLI Interface
Advanced features with no AI dependencies - works immediately
"""

import argparse
import sys
import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional
import re

# Simple HTS database (same as in cli_simple.py)
HTS_DATABASE = {
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
KNOWLEDGE_BASE = {
    "gsp": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
    "generalized system of preferences": "The Generalized System of Preferences (GSP) is a U.S. trade preference program designed to promote economic development by allowing duty-free entry for thousands of products from designated developing countries.",
    "hts": "The Harmonized Tariff Schedule (HTS) is a standardized numerical method of classifying traded products used by customs authorities around the world.",
    "duty": "Import duties are taxes imposed by customs authorities on goods when they are transported across international borders.",
    "cif": "CIF (Cost, Insurance, and Freight) is the total cost of goods including the cost of the goods, insurance, and freight charges.",
    "nafta": "NAFTA (now USMCA) provides preferential tariff treatment for qualifying goods originating in Canada, Mexico, and the United States.",
    "usmca": "The United States-Mexico-Canada Agreement (USMCA) replaced NAFTA and provides preferential tariff treatment for qualifying goods.",
    "fta": "Free Trade Agreements (FTAs) are treaties between countries that reduce or eliminate trade barriers between participating nations."
}

def answer_question(question):
    """Answer trade policy questions using the knowledge base"""
    question_lower = question.lower()
    
    # Check knowledge base
    for key, answer in KNOWLEDGE_BASE.items():
        if key in question_lower:
            return f"💡 {answer}"
    
    # Check for HTS code specific questions
    for hts_code, info in HTS_DATABASE.items():
        if hts_code in question:
            return f"💡 HTS Code {hts_code}: {info['description']} | Duty Rate: {info['duty_rate']*100:.1f}% | Category: {info['category']}"
    
    return "❓ I don't have specific information about that. Try asking about GSP, HTS codes, duties, CIF, NAFTA/USMCA, or FTA."

def calculate_duty(hts_code, product_cost, freight=0, insurance=0):
    """Calculate duty for given HTS code and costs"""
    # Calculate CIF value
    cif_value = product_cost + freight + insurance
    
    # Get HTS info
    hts_info = HTS_DATABASE.get(hts_code)
    if not hts_info:
        return f"❌ HTS code {hts_code} not found. Available codes: {', '.join(HTS_DATABASE.keys())}"
    
    # Calculate duty
    duty_rate = hts_info["duty_rate"]
    duty_amount = cif_value * duty_rate
    landed_cost = cif_value + duty_amount
    
    result = f"""
📊 DUTY CALCULATION RESULT
{'='*50}
HTS Code:      {hts_code}
Description:   {hts_info['description']}
Category:      {hts_info['category']}

Product Cost:  ${product_cost:,.2f}
Freight:       ${freight:,.2f}
Insurance:     ${insurance:,.2f}
CIF Value:     ${cif_value:,.2f}

Duty Rate:     {duty_rate*100:.1f}%
Duty Amount:   ${duty_amount:,.2f}
Landed Cost:   ${landed_cost:,.2f}

Calculated:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}
"""
    return result

def batch_calculate(csv_file: str) -> None:
    """Process batch calculations from CSV file"""
    try:
        results = []
        with open(csv_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            
            print(f"\n📊 Processing batch file: {csv_file}")
            print("-" * 60)
            
            for i, row in enumerate(reader, 1):
                try:
                    hts_code = row['hts_code']
                    product_cost = float(row['product_cost'])
                    freight = float(row.get('freight', 0))
                    insurance = float(row.get('insurance', 0))
                    
                    # Calculate duty
                    if hts_code in HTS_DATABASE:
                        duty_info = HTS_DATABASE[hts_code]
                        cif_value = product_cost + freight + insurance
                        duty_amount = cif_value * duty_info['duty_rate']
                        total_cost = cif_value + duty_amount
                        
                        result = {
                            'row': i,
                            'hts_code': hts_code,
                            'description': duty_info['description'],
                            'product_cost': product_cost,
                            'cif_value': cif_value,
                            'duty_rate': duty_info['duty_rate'],
                            'duty_amount': duty_amount,
                            'total_cost': total_cost
                        }
                        results.append(result)
                        
                        print(f"✅ Row {i}: {hts_code} - Duty: ${duty_amount:,.2f} | Total: ${total_cost:,.2f}")
                    else:
                        print(f"❌ Row {i}: Unknown HTS code {hts_code}")
                        
                except Exception as e:
                    print(f"❌ Row {i}: Error - {e}")
            
            # Export results
            if results:
                output_file = csv_file.replace('.csv', '_results.csv')
                with open(output_file, 'w', newline='') as outfile:
                    fieldnames = ['row', 'hts_code', 'description', 'product_cost', 
                                'cif_value', 'duty_rate', 'duty_amount', 'total_cost']
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(results)
                
                print(f"\n📁 Results exported to: {output_file}")
                print(f"✅ Processed {len(results)} successful calculations")
            
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
    except Exception as e:
        print(f"❌ Error processing batch file: {e}")

def export_hts_database(format_type: str = 'json') -> None:
    """Export HTS database in various formats"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format_type.lower() == 'json':
        filename = f"hts_database_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(HTS_DATABASE, f, indent=2)
        print(f"📁 HTS database exported to: {filename}")
    
    elif format_type.lower() == 'csv':
        filename = f"hts_database_{timestamp}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['HTS Code', 'Description', 'Duty Rate (%)', 'Category', 'Units'])
            for code, info in HTS_DATABASE.items():
                writer.writerow([
                    code, 
                    info['description'], 
                    f"{info['duty_rate']*100:.2f}", 
                    info['category'], 
                    info['units']
                ])
        print(f"📁 HTS database exported to: {filename}")
    
    else:
        print("❌ Unsupported format. Use 'json' or 'csv'")

def search_hts_codes(search_term: str) -> None:
    """Search HTS codes by description or category"""
    print(f"\n🔍 Searching for: '{search_term}'")
    print("-" * 60)
    
    matches = []
    search_lower = search_term.lower()
    
    for code, info in HTS_DATABASE.items():
        if (search_lower in info['description'].lower() or 
            search_lower in info['category'].lower() or
            search_lower in code.lower()):
            matches.append((code, info))
    
    if matches:
        print(f"Found {len(matches)} matches:")
        for code, info in matches:
            print(f"  {code} | {info['description'][:50]:<50} | {info['duty_rate']*100:>6.1f}% | {info['category']}")
    else:
        print("No matches found")

def compare_rates(codes: List[str]) -> None:
    """Compare duty rates for multiple HTS codes"""
    print(f"\n📊 Comparing {len(codes)} HTS codes:")
    print("-" * 80)
    
    valid_codes = []
    for code in codes:
        if code in HTS_DATABASE:
            valid_codes.append(code)
        else:
            print(f"❌ Unknown HTS code: {code}")
    
    if valid_codes:
        # Sort by duty rate
        sorted_codes = sorted(valid_codes, key=lambda x: HTS_DATABASE[x]['duty_rate'])
        
        print(f"{'HTS Code':<15} | {'Description':<40} | {'Duty Rate':<10} | {'Category'}")
        print("-" * 80)
        
        for code in sorted_codes:
            info = HTS_DATABASE[code]
            print(f"{code:<15} | {info['description'][:40]:<40} | {info['duty_rate']*100:>8.1f}% | {info['category']}")

def generate_template() -> None:
    """Generate CSV template for batch processing"""
    filename = "hts_batch_template.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['hts_code', 'product_cost', 'freight', 'insurance', 'description'])
        
        # Add sample data
        sample_codes = list(HTS_DATABASE.keys())[:3]
        for code in sample_codes:
            writer.writerow([code, '10000', '500', '100', f'Sample product for {code}'])
    
    print(f"📁 Batch template created: {filename}")
    print("Fill in your data and use --batch to process it")

def show_statistics() -> None:
    """Show database statistics"""
    print("\n📊 HTS Database Statistics")
    print("-" * 40)
    print(f"Total HTS Codes: {len(HTS_DATABASE)}")
    
    # Category breakdown
    categories = {}
    duty_rates = []
    
    for code, info in HTS_DATABASE.items():
        category = info['category']
        categories[category] = categories.get(category, 0) + 1
        duty_rates.append(info['duty_rate'])
    
    print(f"\nCategories:")
    for category, count in categories.items():
        print(f"  {category}: {count} codes")
    
    print(f"\nDuty Rate Statistics:")
    print(f"  Average: {sum(duty_rates)/len(duty_rates)*100:.2f}%")
    print(f"  Minimum: {min(duty_rates)*100:.2f}%")
    print(f"  Maximum: {max(duty_rates)*100:.2f}%")
    
    # Free duty codes
    free_codes = [code for code, info in HTS_DATABASE.items() if info['duty_rate'] == 0]
    print(f"  Free Duty Codes: {len(free_codes)}")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='HTS AI Agent - Fixed Version (No AI Dependencies)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main_fixed.py --query "What is GSP?"
  python main_fixed.py --chat
  python main_fixed.py --calc 0101.30.00.00 10000 500 100
  python main_fixed.py --list

Available HTS Codes:
  0101.30.00.00  - Live asses (Free)
  0102.21.00.00  - Live cattle, purebred (2.5%)
  0201.10.00.00  - Beef carcasses (4.4%)
  0301.11.00.00  - Ornamental fish (Free)
  0401.10.00.00  - Milk ≤1% fat (3.8%)
        '''
    )
    
    parser.add_argument('--query', '-q', help='Ask a question about trade policies')
    parser.add_argument('--chat', '-c', action='store_true', help='Start interactive chat mode')
    parser.add_argument('--calc', nargs='+', help='Calculate duty: HTS_CODE PRODUCT_COST [FREIGHT] [INSURANCE]')
    parser.add_argument('--list', '-l', action='store_true', help='List available HTS codes')
    parser.add_argument('--search', '-s', help='Search HTS codes by keyword')
    parser.add_argument('--compare', nargs='+', help='Compare duty rates for multiple HTS codes')
    parser.add_argument('--batch', '-b', help='Process batch calculations from CSV file')
    parser.add_argument('--export', choices=['json', 'csv'], help='Export HTS database')
    parser.add_argument('--template', action='store_true', help='Generate CSV template for batch processing')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    
    args = parser.parse_args()
    
    # Print banner
    print("""
🌐 HTS AI Agent - Enhanced CLI Interface
Advanced Trade Intelligence & Duty Calculation Platform
(No AI dependencies - works immediately!)
""")
    
    if args.query:
        # Handle single query
        response = answer_question(args.query)
        print(f"\nQuestion: {args.query}")
        print(f"Answer: {response}")
    
    elif args.calc:
        # Handle duty calculation
        if len(args.calc) < 2:
            print("❌ Usage: --calc HTS_CODE PRODUCT_COST [FREIGHT] [INSURANCE]")
            sys.exit(1)
        
        try:
            hts_code = args.calc[0]
            product_cost = float(args.calc[1])
            freight = float(args.calc[2]) if len(args.calc) > 2 else 0
            insurance = float(args.calc[3]) if len(args.calc) > 3 else 0
            
            result = calculate_duty(hts_code, product_cost, freight, insurance)
            print(result)
        except ValueError:
            print("❌ Error: Please provide valid numbers for costs")
            sys.exit(1)
    
    elif args.list:
        # List HTS codes
        print("\n📋 Available HTS Codes:")
        print("=" * 80)
        for code, info in HTS_DATABASE.items():
            print(f"{code} | {info['description'][:50]:<50} | {info['duty_rate']*100:>6.1f}%")
        print("=" * 80)
    
    elif args.search:
        # Search HTS codes
        search_hts_codes(args.search)
    
    elif args.compare:
        # Compare duty rates
        compare_rates(args.compare)
    
    elif args.batch:
        # Process batch file
        batch_calculate(args.batch)
    
    elif args.export:
        # Export database
        export_hts_database(args.export)
    
    elif args.template:
        # Generate template
        generate_template()
    
    elif args.stats:
        # Show statistics
        show_statistics()
    
    elif args.chat:
        # Interactive chat mode
        print("Starting interactive chat mode...")
        print("Type 'exit' to quit, 'help' for commands")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n🌐 HTS Agent> ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thank you for using HTS Agent. Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    print("""
📖 Available Commands:
  help                        - Show this help
  list                        - List HTS codes
  calc <code> <cost>          - Calculate duty
  search <keyword>            - Search HTS codes
  compare <code1> <code2>     - Compare rates
  stats                       - Show statistics
  template                    - Generate CSV template
  export <json|csv>           - Export database
  exit/quit/q                 - Exit chat
  
  Or just ask any question about trade policies!
                    """)
                
                elif user_input.lower() == 'list':
                    print("\n📋 Available HTS Codes:")
                    for code, info in HTS_DATABASE.items():
                        print(f"  {code} - {info['description']} ({info['duty_rate']*100:.1f}%)")
                
                elif user_input.lower().startswith('calc'):
                    parts = user_input.split()
                    if len(parts) < 3:
                        print("❌ Usage: calc <hts_code> <product_cost> [freight] [insurance]")
                    else:
                        try:
                            hts_code = parts[1]
                            product_cost = float(parts[2])
                            freight = float(parts[3]) if len(parts) > 3 else 0
                            insurance = float(parts[4]) if len(parts) > 4 else 0
                            
                            result = calculate_duty(hts_code, product_cost, freight, insurance)
                            print(result)
                        except ValueError:
                            print("❌ Error: Please provide valid numbers")
                
                elif user_input.lower().startswith('search'):
                    parts = user_input.split(maxsplit=1)
                    if len(parts) < 2:
                        print("❌ Usage: search <keyword>")
                    else:
                        search_hts_codes(parts[1])
                
                elif user_input.lower().startswith('compare'):
                    parts = user_input.split()[1:]
                    if len(parts) < 2:
                        print("❌ Usage: compare <hts_code1> <hts_code2> [more_codes...]")
                    else:
                        compare_rates(parts)
                
                elif user_input.lower() == 'stats':
                    show_statistics()
                
                elif user_input.lower() == 'template':
                    generate_template()
                
                elif user_input.lower().startswith('export'):
                    parts = user_input.split()
                    if len(parts) < 2 or parts[1] not in ['json', 'csv']:
                        print("❌ Usage: export <json|csv>")
                    else:
                        export_hts_database(parts[1])
                
                else:
                    # Answer as question
                    response = answer_question(user_input)
                    print(f"\n{response}")
            
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    else:
        # No arguments provided
        parser.print_help()
        print(f"\n💡 Quick start: python {sys.argv[0]} --query \"What is GSP?\"")

if __name__ == "__main__":
    main() 