"""
Setup script for Trump Promises Tracker.
"""

import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import DatabaseManager
from sample_data import create_sample_data

def main():
    """Main setup function."""
    print("Trump Promises Tracker - Setup")
    print("=" * 40)
    
    # Initialize database
    print("1. Initializing database...")
    db_manager = DatabaseManager()
    print("   ✓ Database initialized successfully!")
    
    # Add sample data
    print("\n2. Adding sample data...")
    added_promises = create_sample_data()
    print(f"   ✓ Added {len(added_promises)} sample promises!")
    
    # Show some statistics
    print("\n3. Database Statistics:")
    analytics_data = db_manager.get_analytics_data()
    print(f"   Total Promises: {analytics_data['total_promises']}")
    print(f"   Fulfillment Rate: {analytics_data['fulfillment_rate']:.1f}%")
    print(f"   Average Progress: {analytics_data['average_progress']:.1f}%")
    
    print("\n4. Next Steps:")
    print("   • Run the web application: python app.py")
    print("   • Use CLI commands: python -m app.cli --help")
    print("   • View analytics: python -m app.cli generate-report")
    
    print("\nSetup completed successfully! 🎉")

if __name__ == '__main__':
    main()
