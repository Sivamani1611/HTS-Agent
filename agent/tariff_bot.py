import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rag_tool import RAGTool
from tools.tariff_calculator import TariffCalculator
from tools.memory_handler import MemoryHandler
import re
import json

class TariffBot:
    def __init__(self):
        print("Initializing TariffBot...")
        self.rag_tool = RAGTool()
        self.tariff_calculator = TariffCalculator()
        self.memory = MemoryHandler()
        print("TariffBot ready!")
    
    def process_query(self, query):
        """Route queries to appropriate tool"""
        query_lower = query.lower()
        
        # Check if it's a tariff calculation query
        hts_pattern = r'\b\d{4}\.\d{2}\.\d{2}\.\d{2}\b'
        if re.search(hts_pattern, query) or any(keyword in query_lower for keyword in ['calculate', 'duty', 'cost', 'tariff']):
            response = self._handle_tariff_query(query)
        else:
            # It's a policy/general question
            response = self._handle_policy_query(query)
        
        # Save to memory
        self.memory.add_query(query, response)
        
        return response
    
    def _handle_policy_query(self, query):
        """Handle policy-related questions using RAG"""
        result = self.rag_tool.answer_policy_question(query)
        return result
    
    def _handle_tariff_query(self, query):
        """Extract parameters and calculate tariff"""
        # Try to extract HTS code
        hts_match = re.search(r'\b(\d{4}\.\d{2}\.\d{2}\.\d{2})\b', query)
        if not hts_match:
            return {"error": "No valid HTS code found in query. Please provide a code in format XXXX.XX.XX.XX"}
        
        hts_code = hts_match.group(1)
        
        # Extract numeric values from query
        numbers = re.findall(r'\$?([\d,]+(?:\.\d+)?)', query)
        
        # Default values
        product_cost = 10000
        freight = 500
        insurance = 100
        unit_weight = 100
        quantity = 1
        
        # Try to parse values from query
        if len(numbers) >= 1:
            product_cost = float(numbers[0].replace(',', ''))
        
        # Look for weight
        weight_match = re.search(r'(\d+\.?\d*)\s*(kg|lbs?)', query.lower())
        if weight_match:
            unit_weight = float(weight_match.group(1))
            if 'lb' in weight_match.group(2):
                unit_weight *= 0.453592  # Convert to kg
        
        # Look for quantity
        qty_match = re.search(r'(\d+)\s*(units?|pieces?|items?)', query.lower())
        if qty_match:
            quantity = int(qty_match.group(1))
        
        # Calculate duties
        result = self.tariff_calculator.calculate_duty(
            hts_code=hts_code,
            product_cost=product_cost,
            freight=freight,
            insurance=insurance,
            unit_weight=unit_weight,
            quantity=quantity
        )
        
        return result
    
    def get_similar_queries(self, query):
        """Get similar past queries from memory"""
        recent = self.memory.get_recent_queries(20)
        similar = []
        
        query_words = set(query.lower().split())
        for past_query in recent:
            past_words = set(past_query['query'].lower().split())
            if len(query_words.intersection(past_words)) >= 2:
                similar.append(past_query)
        
        return similar[:5]
    
    def chat(self):
        """Interactive chat interface with memory"""
        print("\n" + "="*60)
        print("Welcome to TariffBot!")
        print("I can help you with:")
        print("1. Trade policy questions (e.g., 'What is GSP?')")
        print("2. Duty calculations (e.g., 'Calculate duty for HTS 0101.30.00.00')")
        print("\nI also remember our conversation history!")
        print("="*60 + "\n")
        
        while True:
            query = input("\nYour question (or 'exit' to quit, 'history' to see past queries): ").strip()
            
            if query.lower() in ['exit', 'quit', 'bye']:
                print("Thank you for using TariffBot. Goodbye!")
                break
            
            if query.lower() == 'history':
                self._show_history()
                continue
            
            if not query:
                continue
            
            # Check for similar past queries
            similar = self.get_similar_queries(query)
            if similar:
                print("\n💡 Similar past queries:")
                for sq in similar[:3]:
                    print(f"  - {sq['query'][:60]}...")
            
            try:
                result = self.process_query(query)
                
                if isinstance(result, dict):
                    if "error" in result:
                        print(f"\n❌ Error: {result['error']}")
                    elif "answer" in result:
                        # Policy question response
                        print(f"\n📚 Answer: {result['answer']}")
                        if "sources" in result:
                            print(f"📄 {result['sources']}")
                    else:
                        # Tariff calculation response
                        self._print_tariff_result(result)
                else:
                    print(f"\n{result}")
                    
            except Exception as e:
                print(f"\n❌ An error occurred: {str(e)}")
                print("Please try rephrasing your question.")
    
    def _show_history(self):
        """Show query history"""
        recent = self.memory.get_recent_queries(10)
        stats = self.memory.get_statistics()
        
        print("\n" + "="*50)
        print("📊 QUERY STATISTICS")
        print("="*50)
        print(f"Total Queries: {stats['total_queries']}")
        print(f"Policy Questions: {stats['policy_queries']}")
        print(f"Duty Calculations: {stats['duty_calculations']}")
        print("\n📝 Recent Queries:")
        print("-"*50)
        
        for i, query in enumerate(recent, 1):
            print(f"{i}. [{query['timestamp'][:16]}] {query['query'][:50]}...")
            print(f"   Type: {query['query_type']}")
    
    def _print_tariff_result(self, result):
        """Pretty print tariff calculation results"""
        print("\n" + "="*50)
        print("📊 TARIFF CALCULATION RESULT")
        print("="*50)
        print(f"HTS Code: {result.get('HTS Code', 'N/A')}")
        print(f"Description: {result.get('Description', 'N/A')}")
        print("-"*50)
        print(f"Product Cost: {result.get('Product Cost', 'N/A')}")
        print(f"Freight: {result.get('Freight', 'N/A')}")
        print(f"Insurance: {result.get('Insurance', 'N/A')}")
        print(f"CIF Value: {result.get('CIF Value', 'N/A')}")
        print("-"*50)
        
        if "duties" in result:
            print("DUTY RATES:")
            for duty_type, duty_info in result["duties"].items():
                print(f"  {duty_type}: {duty_info['rate']} = {duty_info['amount']}")
        
        print("-"*50)
        print(f"Total Duty: {result.get('Total Duty', 'N/A')}")
        print(f"Landed Cost: {result.get('Landed Cost', 'N/A')}")
        print("="*50)

if __name__ == "__main__":
    bot = TariffBot()
    bot.chat()