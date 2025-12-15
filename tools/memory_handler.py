import json
import os
from datetime import datetime
from typing import List, Dict, Any
import sqlite3

class MemoryHandler:
    def __init__(self, db_path="data/query_history.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize the database for storing query history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                query TEXT,
                query_type TEXT,
                response TEXT,
                hts_code TEXT,
                landed_cost REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_query(self, query: str, response: Dict[str, Any] = None):
        """Add a query to history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        query_type = self._determine_query_type(query)
        response_json = json.dumps(response) if response else ""
        
        # Extract HTS code and landed cost if it's a duty calculation
        hts_code = ""
        landed_cost = 0.0
        if response and isinstance(response, dict):
            hts_code = response.get('HTS Code', '')
            if 'Landed Cost' in response:
                try:
                    landed_cost = float(response['Landed Cost'].replace('$', '').replace(',', ''))
                except:
                    landed_cost = 0.0
        
        cursor.execute('''
            INSERT INTO queries (timestamp, query, query_type, response, hts_code, landed_cost)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, query, query_type, response_json, hts_code, landed_cost))
        
        conn.commit()
        conn.close()
    
    def _determine_query_type(self, query: str) -> str:
        """Determine if query is policy or duty calculation"""
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in ['calculate', 'duty', 'hts code', 'cost']):
            return 'duty_calculation'
        else:
            return 'policy_question'
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent queries"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, query, query_type, response 
            FROM queries 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'timestamp': row[0],
                'query': row[1],
                'query_type': row[2],
                'response': json.loads(row[3]) if row[3] else None
            })
        
        conn.close()
        return results
    
    def get_recent_calculations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent duty calculations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp, hts_code, landed_cost, response 
            FROM queries 
            WHERE query_type = 'duty_calculation' AND hts_code != ''
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
        
        results = []
        for row in cursor.fetchall():
            response = json.loads(row[3]) if row[3] else {}
            results.append({
                'Timestamp': row[0][:19],
                'HTS Code': row[1],
                'Landed Cost': f"${row[2]:,.2f}",
                'CIF Value': response.get('CIF Value', 'N/A'),
                'Total Duty': response.get('Total Duty', 'N/A')
            })
        
        conn.close()
        return results
    
    def get_statistics(self) -> Dict[str, int]:
        """Get query statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM queries')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM queries WHERE query_type = "policy_question"')
        policy = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM queries WHERE query_type = "duty_calculation"')
        duty = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_queries': total,
            'policy_queries': policy,
            'duty_calculations': duty
        }