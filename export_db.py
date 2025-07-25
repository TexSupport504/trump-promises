"""
Database Export Tool for Trump Promises Tracker
"""

import sqlite3
import csv
import os
from datetime import datetime
from config import Config

def export_to_csv():
    """Export database tables to CSV files."""
    
    db_path = Config.DATABASE_URL
    export_dir = "e:\\OneDrive\\Documents\\GitHub\\github_files\\database_exports"
    
    # Create export directory
    os.makedirs(export_dir, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Tables to export
    tables = ['promises', 'sources', 'promise_sources', 'progress_updates']
    
    print(f"📁 Exporting database to: {export_dir}")
    print("=" * 50)
    
    for table in tables:
        try:
            # Get all data from table
            cursor.execute(f"SELECT * FROM {table}")
            data = cursor.fetchall()
            
            # Get column names
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Export to CSV
            csv_filename = f"{table}_{timestamp}.csv"
            csv_path = os.path.join(export_dir, csv_filename)
            
            with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(columns)
                
                # Write data
                writer.writerows(data)
            
            print(f"✅ {table}: {len(data)} records → {csv_filename}")
            
        except Exception as e:
            print(f"❌ Error exporting {table}: {e}")
    
    # Create a comprehensive summary report
    summary_file = os.path.join(export_dir, f"database_summary_{timestamp}.txt")
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("TRUMP PROMISES TRACKER - DATABASE SUMMARY\n")
        f.write("=" * 50 + "\n")
        f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Database: {db_path}\n\n")
        
        # Add table summaries
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            f.write(f"{table}: {count} records\n")
        
        f.write("\n" + "=" * 50 + "\n")
        f.write("PROMISE STATISTICS\n")
        f.write("=" * 50 + "\n")
        
        # Add detailed statistics
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(progress_percentage) as avg_progress,
                COUNT(CASE WHEN status = 'Fulfilled' THEN 1 END) as fulfilled,
                COUNT(CASE WHEN status = 'Broken' THEN 1 END) as broken,
                COUNT(CASE WHEN status = 'Partially Fulfilled' THEN 1 END) as partial
            FROM promises
        """)
        
        stats = cursor.fetchone()
        total, avg_progress, fulfilled, broken, partial = stats
        
        f.write(f"Total Promises: {total}\n")
        f.write(f"Average Progress: {avg_progress:.2f}%\n")
        f.write(f"Fulfilled: {fulfilled} ({fulfilled/total*100:.1f}%)\n")
        f.write(f"Broken: {broken} ({broken/total*100:.1f}%)\n")
        f.write(f"Partially Fulfilled: {partial} ({partial/total*100:.1f}%)\n")
        
        # Category breakdown
        f.write(f"\nCATEGORY BREAKDOWN\n")
        f.write("-" * 30 + "\n")
        
        cursor.execute("""
            SELECT category, COUNT(*), AVG(progress_percentage)
            FROM promises 
            GROUP BY category 
            ORDER BY AVG(progress_percentage) DESC
        """)
        
        for category, count, avg_prog in cursor.fetchall():
            f.write(f"{category}: {count} promises, {avg_prog:.1f}% avg progress\n")
    
    conn.close()
    
    print(f"\n✅ Summary report: database_summary_{timestamp}.txt")
    print(f"📁 All files saved to: {export_dir}")
    print("\n💡 You can now open these CSV files in Excel or any spreadsheet application!")

if __name__ == "__main__":
    export_to_csv()
