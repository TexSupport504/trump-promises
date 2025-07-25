"""
Predefined Database Queries for Trump Promises Tracker
"""

import sqlite3
from config import Config

def run_predefined_queries():
    """Run a set of useful predefined queries."""
    
    db_path = Config.DATABASE_URL
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    queries = {
        "📊 All Promises by Progress": """
            SELECT id, text, category, status, progress_percentage
            FROM promises 
            ORDER BY progress_percentage DESC, category
        """,
        
        "🏆 Top Performing Categories": """
            SELECT 
                category,
                COUNT(*) as total_promises,
                ROUND(AVG(progress_percentage), 2) as avg_progress,
                COUNT(CASE WHEN status = 'Fulfilled' THEN 1 END) as fulfilled
            FROM promises 
            GROUP BY category 
            ORDER BY avg_progress DESC
        """,
        
        "🚨 Promises Needing Attention": """
            SELECT id, text, category, progress_percentage, status
            FROM promises 
            WHERE progress_percentage < 50 AND status NOT IN ('Fulfilled', 'Broken')
            ORDER BY progress_percentage ASC
        """,
        
        "📈 Status Distribution": """
            SELECT 
                status,
                COUNT(*) as count,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM promises), 2) as percentage
            FROM promises 
            GROUP BY status 
            ORDER BY count DESC
        """,
        
        "🔗 Promises with Sources": """
            SELECT p.id, p.text, s.title as source_title, s.url
            FROM promises p
            JOIN promise_sources ps ON p.id = ps.promise_id
            JOIN sources s ON ps.source_id = s.id
            ORDER BY p.id
        """,
        
        "📋 Source Reliability": """
            SELECT 
                title,
                source_type,
                reliability_score,
                url
            FROM sources 
            ORDER BY reliability_score DESC, source_type
        """
    }
    
    print("🗄️ Trump Promises Database - Predefined Query Results")
    print("=" * 70)
    
    for title, query in queries.items():
        print(f"\n{title}")
        print("-" * 50)
        
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            if results:
                # Print header
                header = " | ".join(f"{col:20}" for col in columns)
                print(header)
                print("-" * len(header))
                
                # Print results
                for row in results:
                    formatted_row = " | ".join(f"{str(val)[:20]:20}" for val in row)
                    print(formatted_row)
                
                print(f"\n📊 Total: {len(results)} records")
            else:
                print("No results found")
                
        except Exception as e:
            print(f"❌ Error executing query: {e}")
        
        print()
    
    conn.close()

if __name__ == "__main__":
    run_predefined_queries()
