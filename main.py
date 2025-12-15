#!/usr/bin/env python3
"""
HTS AI Agent - Main Entry Point
A dual-purpose agent for HTS policy questions and duty calculations
"""

import os
import sys
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent.tariff_bot import TariffBot

def main():
    parser = argparse.ArgumentParser(description='HTS AI Agent - Trade Policy & Duty Calculator')
    parser.add_argument('--mode', choices=['chat', 'query'], default='chat',
                        help='Run in chat mode or single query mode')
    parser.add_argument('--query', type=str, help='Single query to process')
    parser.add_argument('--test', action='store_true', help='Run test queries')
    
    args = parser.parse_args()
    
    # Initialize the bot
    print(f"\n🤖 Starting HTS AI Agent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        bot = TariffBot()
        
        if args.test:
            # Run test queries
            test_queries = [
                "What is the Generalized System of Preferences?",
                "What is the United States-Israel Free Trade Agreement?",
                "Given HTS code 0101.30.00.00, a product cost of $10,000, 500 kg weight, and 5 units — what are all applicable duties?",
                "Calculate duty for HTS 0102.21.00.00 with cost $5000"
            ]
            
            print("\n🧪 Running test queries...")
            for query in test_queries:
                print(f"\n❓ Query: {query}")
                result = bot.process_query(query)
                if isinstance(result, dict) and "answer" in result:
                    print(f"✅ Answer: {result['answer'][:200]}...")
                else:
                    print(f"✅ Result: {result}")
        
        elif args.query:
            # Process single query
            result = bot.process_query(args.query)
            print(result)
        
        else:
            # Interactive chat mode
            bot.chat()
            
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()