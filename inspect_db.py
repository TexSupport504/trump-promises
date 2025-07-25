#!/usr/bin/env python3
"""
Database Inspector for Trump Promises Tracker

This script provides tools to inspect and analyze the SQLite database.
"""

import sqlite3
import os
import sys
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import DatabaseManager
from app.models import Promise, ProgressUpdate, PromiseStatus
from config import Config

def inspect_database():
    """Inspect the database structure and contents."""
    
    print("=" * 60)
    print("TRUMP PROMISES TRACKER - DATABASE INSPECTOR")
    print("=" * 60)
    
    # Check if database exists
    db_path = Config.DATABASE_URL
    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"📁 Database location: {db_path}")
    print(f"📊 Database size: {os.path.getsize(db_path):,} bytes")
    print()
    
    # Connect to database
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📋 Database Tables:")
        print("-" * 30)
        for table in tables:
            table_name = table[0]
            
            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            # Get record count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            
            print(f"\n🔸 Table: {table_name}")
            print(f"   Records: {count:,}")
            print("   Columns:")
            for col in columns:
                col_id, col_name, col_type, not_null, default, pk = col
                pk_marker = " (PK)" if pk else ""
                null_marker = " NOT NULL" if not_null else ""
                default_marker = f" DEFAULT {default}" if default else ""
                print(f"     - {col_name}: {col_type}{pk_marker}{null_marker}{default_marker}")
        
        print("\n" + "=" * 60)
        print("RECENT DATA OVERVIEW")
        print("=" * 60)
        
        # Show recent promises
        print("\n🎯 Recent Promises (Top 5 by Progress):")
        print("-" * 50)
        cursor.execute("""
            SELECT id, text, category, status, progress_percentage, created_at 
            FROM promises 
            ORDER BY progress_percentage DESC, created_at DESC 
            LIMIT 5
        """)
        
        promises = cursor.fetchall()
        for promise in promises:
            p_id, text, category, status, progress, created = promise
            # Truncate long titles
            short_text = text[:50] + "..." if len(text) > 50 else text
            print(f"   {p_id:3d}. [{progress:3.0f}%] {short_text}")
            print(f"        Category: {category} | Status: {status}")
            print()
        
        # Show recent updates
        print("📈 Recent Progress Updates (Last 5):")
        print("-" * 50)
        cursor.execute("""
            SELECT pu.id, pu.promise_id, p.text, pu.update_text, pu.date, pu.impact_score
            FROM progress_updates pu
            JOIN promises p ON pu.promise_id = p.id
            ORDER BY pu.date DESC, pu.id DESC
            LIMIT 5
        """)
        
        updates = cursor.fetchall()
        for update in updates:
            u_id, p_id, text, update_text, date, impact = update
            short_text = text[:30] + "..." if len(text) > 30 else text
            short_update = update_text[:60] + "..." if len(update_text) > 60 else update_text
            print(f"   Update {u_id} (Promise {p_id}): {short_text}")
            print(f"   📝 {short_update}")
            print(f"   📅 {date} | Impact: {impact}/10")
            print()
        
        # Summary statistics
        print("📊 Summary Statistics:")
        print("-" * 30)
        
        # Progress distribution
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                AVG(progress_percentage) as avg_progress,
                MIN(progress_percentage) as min_progress,
                MAX(progress_percentage) as max_progress
            FROM promises
        """)
        stats = cursor.fetchone()
        total, avg_progress, min_progress, max_progress = stats
        
        print(f"   Total Promises: {total:,}")
        print(f"   Average Progress: {avg_progress:.1f}%")
        print(f"   Progress Range: {min_progress:.0f}% - {max_progress:.0f}%")
        
        # Status breakdown
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM promises 
            GROUP BY status 
            ORDER BY count DESC
        """)
        status_counts = cursor.fetchall()
        
        print("\n   Status Breakdown:")
        for status, count in status_counts:
            percentage = (count / total) * 100
            print(f"     {status}: {count:,} ({percentage:.1f}%)")
        
        # Category breakdown
        cursor.execute("""
            SELECT category, COUNT(*) as count, AVG(progress_percentage) as avg_progress
            FROM promises 
            GROUP BY category 
            ORDER BY count DESC
        """)
        category_stats = cursor.fetchall()
        
        print("\n   Category Performance:")
        for category, count, avg_prog in category_stats:
            print(f"     {category}: {count:,} promises, {avg_prog:.1f}% avg progress")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error inspecting database: {e}")
        return
    
    print("\n" + "=" * 60)
    print("✅ Database inspection complete!")
    print("\n💡 Next steps:")
    print("   1. Install SQLite Viewer extension in VS Code")
    print("   2. Open the database file: data/promises.db")
    print("   3. Use VS Code's SQLite tools to query and explore")
    print("=" * 60)

def quick_query(query):
    """Execute a quick SQL query on the database."""
    db_path = Config.DATABASE_URL
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"🔍 Executing: {query}")
        print("-" * 50)
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Print header
        print(" | ".join(f"{col:20}" for col in column_names))
        print("-" * (len(column_names) * 23))
        
        # Print results
        for row in results:
            print(" | ".join(f"{str(val)[:20]:20}" for val in row))
        
        print(f"\n📊 {len(results)} rows returned")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Query error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Execute custom query
        query = " ".join(sys.argv[1:])
        quick_query(query)
    else:
        # Run full inspection
        inspect_database()
