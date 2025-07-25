"""
Interactive Database Query Tool for Trump Promises Tracker
"""

import sqlite3
import sys
import os
from config import Config

def interactive_query():
    """Interactive database query session."""
    db_path = Config.DATABASE_URL
    
    print("🔍 Interactive Database Query Tool")
    print("=" * 50)
    print(f"Connected to: {db_path}")
    print("\nCommon queries:")
    print("  1. SELECT * FROM promises;")
    print("  2. SELECT * FROM sources;")
    print("  3. SELECT category, COUNT(*) FROM promises GROUP BY category;")
    print("  4. SELECT status, AVG(progress_percentage) FROM promises GROUP BY status;")
    print("\nType 'quit' to exit, 'tables' to see all tables")
    print("-" * 50)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    while True:
        try:
            query = input("\nSQL> ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
            elif query.lower() == 'tables':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                print("\n📋 Available tables:")
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
                    count = cursor.fetchone()[0]
                    print(f"  - {table[0]} ({count} records)")
                continue
            elif not query:
                continue
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            if results:
                # Get column names
                columns = [desc[0] for desc in cursor.description]
                
                # Print header
                print("\n" + " | ".join(f"{col:15}" for col in columns))
                print("-" * (len(columns) * 18))
                
                # Print results (limit to 20 rows for readability)
                for i, row in enumerate(results[:20]):
                    print(" | ".join(f"{str(val)[:15]:15}" for val in row))
                
                if len(results) > 20:
                    print(f"\n... and {len(results) - 20} more rows")
                
                print(f"\n📊 {len(results)} total rows")
            else:
                print("✅ Query executed successfully (no results)")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.close()
    print("\n👋 Database session ended")

if __name__ == "__main__":
    interactive_query()
