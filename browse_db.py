"""
Terminal Database Browser for Trump Promises Tracker
"""

import sqlite3
import sys
from config import Config

def browse_table(table_name, limit=10):
    """Browse a specific table with pagination."""
    db_path = Config.DATABASE_URL
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get table info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Get total count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_records = cursor.fetchone()[0]
        
        print(f"\n📊 Table: {table_name}")
        print(f"📈 Total Records: {total_records}")
        print("-" * 60)
        
        if total_records == 0:
            print("No records found.")
            return
        
        # Show column info
        print("Columns:")
        for col in columns:
            col_id, col_name, col_type, not_null, default, pk = col
            pk_marker = " (PK)" if pk else ""
            print(f"  - {col_name}: {col_type}{pk_marker}")
        
        print(f"\nFirst {min(limit, total_records)} records:")
        print("-" * 60)
        
        # Get data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
        records = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Print header
        header = " | ".join(f"{col[:15]:15}" for col in column_names)
        print(header)
        print("-" * len(header))
        
        # Print records
        for record in records:
            row = " | ".join(f"{str(val)[:15]:15}" for val in record)
            print(row)
        
        if total_records > limit:
            print(f"\n... and {total_records - limit} more records")
            
    except Exception as e:
        print(f"❌ Error browsing table {table_name}: {e}")
    
    finally:
        conn.close()

def main():
    """Main browser interface."""
    
    if len(sys.argv) > 1:
        table_name = sys.argv[1]
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        browse_table(table_name, limit)
        return
    
    # Interactive mode
    db_path = Config.DATABASE_URL
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🗄️ Trump Promises Database Browser")
    print("=" * 50)
    print(f"Database: {db_path}")
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [table[0] for table in cursor.fetchall()]
    
    print(f"\n📋 Available Tables ({len(tables)}):")
    for i, table in enumerate(tables, 1):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {i}. {table} ({count} records)")
    
    print("\nCommands:")
    print("  - Enter table number or name to browse")
    print("  - 'quit' or 'q' to exit")
    print("  - 'refresh' to reload table list")
    
    while True:
        try:
            choice = input("\nBrowser> ").strip()
            
            if choice.lower() in ['quit', 'q', 'exit']:
                break
            elif choice.lower() == 'refresh':
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [table[0] for table in cursor.fetchall()]
                print(f"\n📋 Tables refreshed: {tables}")
                continue
            elif choice.isdigit():
                table_idx = int(choice) - 1
                if 0 <= table_idx < len(tables):
                    browse_table(tables[table_idx])
                else:
                    print(f"❌ Invalid table number. Choose 1-{len(tables)}")
            elif choice in tables:
                browse_table(choice)
            elif choice:
                print(f"❌ Table '{choice}' not found. Available: {', '.join(tables)}")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    conn.close()
    print("\n👋 Database browser closed")

if __name__ == "__main__":
    main()
