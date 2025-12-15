import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.rag_tool import RAGTool
from tools.tariff_calculator import TariffCalculator

def test_rag_tool():
    print("Testing RAG Tool...")
    rag = RAGTool()
    
    test_questions = [
        "What is the Generalized System of Preferences?",
        "Tell me about NAFTA",
        "What is the Israel Free Trade Agreement?"
    ]
    
    for question in test_questions:
        print(f"\nQ: {question}")
        result = rag.answer_policy_question(question)
        print(f"A: {result['answer'][:100]}...")

def test_tariff_calculator():
    print("\n\nTesting Tariff Calculator...")
    calc = TariffCalculator()
    
    test_cases = [
        {
            "hts_code": "0101.30.00.00",
            "product_cost": 10000,
            "freight": 500,
            "insurance": 100,
            "unit_weight": 500,
            "quantity": 5
        },
        {
            "hts_code": "0102.21.00.00",
            "product_cost": 5000,
            "freight": 250,
            "insurance": 50,
            "unit_weight": 300,
            "quantity": 2
        }
    ]
    
    for test in test_cases:
        print(f"\nTesting HTS {test['hts_code']}...")
        result = calc.calculate_duty(**test)
        if "error" not in result:
            print(f"CIF: {result['CIF Value']}")
            print(f"Total Duty: {result['Total Duty']}")
            print(f"Landed Cost: {result['Landed Cost']}")

if __name__ == "__main__":
    test_rag_tool()
    test_tariff_calculator()