"""
Update script to add some real sources for key promises
"""
import sys
import os

# Add the app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import DatabaseManager
from app.models import Source, SourceType
from datetime import datetime

def update_sources():
    """Add real sources for key promises."""
    db = DatabaseManager()
    
    # Real sources for key promises
    real_sources = [
        {
            'promise_id': 1,  # Border wall promise
            'title': 'Trump Border Security Plans - Official Campaign',
            'description': 'Official campaign policy on border security and wall construction',
            'url': 'https://www.donaldjtrump.com/agenda47',
            'source_type': SourceType.CAMPAIGN_WEBSITE,
            'reliability_score': 0.95,
            'date_published': datetime(2024, 11, 15)
        },
        {
            'promise_id': 13,  # Cartel designation  
            'title': 'Terrorist Designation for Cartels - Policy Platform',
            'description': 'Official policy platform on designating drug cartels as terrorist organizations',
            'url': 'https://www.donaldjtrump.com/agenda47',
            'source_type': SourceType.POLICY_DOCUMENT,
            'reliability_score': 0.95,
            'date_published': datetime(2024, 6, 24)
        }
    ]
    
    # Add real sources and link them to promises
    for source_data in real_sources:
        promise_id = source_data.pop('promise_id')
        date_published = source_data.pop('date_published')
        
        # Create source object
        source = Source(
            url=source_data['url'],
            title=source_data['title'],
            description=source_data['description'],
            source_type=source_data['source_type'],
            reliability_score=source_data['reliability_score'],
            date=date_published
        )
        
        # Add source to database and get ID
        source_id = db.add_source(source)
        
        # Link source to promise
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO promise_sources (promise_id, source_id)
                VALUES (?, ?)
            """, (promise_id, source_id))
            conn.commit()
        
        print(f"Added and linked real source for promise {promise_id}: {source.title}")
    
    print(f"Successfully added {len(real_sources)} real sources!")

if __name__ == "__main__":
    update_sources()
