"""
Sample data for the Trump Promises Tracker.
"""

from datetime import datetime, timedelta
from app.database import DatabaseManager
from app.models import Promise, Source, PromiseStatus, SourceType

def create_sample_data():
    """Create sample promises for demonstration."""
    db_manager = DatabaseManager()
    
    # Sample promises with sources
    sample_promises = [
        {
            'text': 'Build a wall along the entire southern border and make Mexico pay for it',
            'category': 'Immigration',
            'status': PromiseStatus.PARTIALLY_FULFILLED,
            'priority': 5,
            'progress_percentage': 35.0,
            'sources': [
                {
                    'title': 'Campaign Rally - Arizona',
                    'url': 'https://example.com/rally-arizona',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Border wall promise at Arizona rally'
                }
            ],
            'tags': ['border-security', 'immigration', 'infrastructure'],
            'notes': 'Wall construction began in several sections. Mexico did not pay for construction.'
        },
        {
            'text': 'Repeal and replace Obamacare with something much better',
            'category': 'Healthcare',
            'status': PromiseStatus.BROKEN,
            'priority': 5,
            'progress_percentage': 15.0,
            'sources': [
                {
                    'title': 'Campaign Website Policy Page',
                    'url': 'https://example.com/healthcare-policy',
                    'source_type': SourceType.CAMPAIGN_WEBSITE,
                    'description': 'Healthcare reform promises'
                }
            ],
            'tags': ['healthcare', 'obamacare', 'insurance'],
            'notes': 'Multiple attempts to repeal failed in Congress. No replacement plan implemented.'
        },
        {
            'text': 'Create the greatest economy in American history',
            'category': 'Economy',
            'status': PromiseStatus.FULFILLED,
            'priority': 5,
            'progress_percentage': 100.0,
            'sources': [
                {
                    'title': 'Economic Policy Speech',
                    'url': 'https://example.com/economic-speech',
                    'source_type': SourceType.PRESS_CONFERENCE,
                    'description': 'Promise to create economic growth'
                }
            ],
            'tags': ['economy', 'jobs', 'growth'],
            'notes': 'Pre-pandemic economy showed strong growth and low unemployment rates.'
        },
        {
            'text': 'Renegotiate NAFTA to get a better deal for American workers',
            'category': 'Trade',
            'status': PromiseStatus.FULFILLED,
            'priority': 4,
            'progress_percentage': 100.0,
            'sources': [
                {
                    'title': 'Trade Policy Interview',
                    'url': 'https://example.com/trade-interview',
                    'source_type': SourceType.INTERVIEW,
                    'description': 'Discussion of NAFTA renegotiation'
                }
            ],
            'tags': ['trade', 'nafta', 'usmca', 'workers'],
            'notes': 'NAFTA was replaced with USMCA (United States-Mexico-Canada Agreement).'
        },
        {
            'text': 'Move the US Embassy in Israel to Jerusalem',
            'category': 'Foreign Policy',
            'status': PromiseStatus.FULFILLED,
            'priority': 3,
            'progress_percentage': 100.0,
            'sources': [
                {
                    'title': 'Foreign Policy Statement',
                    'url': 'https://example.com/jerusalem-embassy',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Embassy relocation promise'
                }
            ],
            'tags': ['israel', 'embassy', 'jerusalem', 'foreign-policy'],
            'notes': 'Embassy officially moved to Jerusalem in May 2018.'
        },
        {
            'text': 'Eliminate the federal deficit and reduce the national debt',
            'category': 'Economy',
            'status': PromiseStatus.BROKEN,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Economic Plan Document',
                    'url': 'https://example.com/deficit-plan',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to eliminate deficit'
                }
            ],
            'tags': ['deficit', 'debt', 'fiscal-policy'],
            'notes': 'Federal deficit increased during presidency, partly due to tax cuts and pandemic spending.'
        },
        {
            'text': 'Achieve energy independence through domestic oil and gas production',
            'category': 'Energy',
            'status': PromiseStatus.FULFILLED,
            'priority': 4,
            'progress_percentage': 85.0,
            'sources': [
                {
                    'title': 'Energy Independence Rally',
                    'url': 'https://example.com/energy-rally',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise for energy independence'
                }
            ],
            'tags': ['energy', 'oil', 'gas', 'independence'],
            'notes': 'US became net energy exporter for first time in decades.'
        },
        {
            'text': 'Rebuild Americas military and increase defense spending',
            'category': 'Defense',
            'status': PromiseStatus.FULFILLED,
            'priority': 4,
            'progress_percentage': 90.0,
            'sources': [
                {
                    'title': 'Defense Policy Speech',
                    'url': 'https://example.com/defense-speech',
                    'source_type': SourceType.PRESS_CONFERENCE,
                    'description': 'Military rebuilding promise'
                }
            ],
            'tags': ['military', 'defense', 'spending'],
            'notes': 'Defense spending increased significantly during term.'
        },
        {
            'text': 'Impose tariffs on China to protect American manufacturing',
            'category': 'Trade',
            'status': PromiseStatus.FULFILLED,
            'priority': 4,
            'progress_percentage': 100.0,
            'sources': [
                {
                    'title': 'China Trade Policy',
                    'url': 'https://example.com/china-tariffs',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to impose China tariffs'
                }
            ],
            'tags': ['china', 'tariffs', 'manufacturing', 'trade-war'],
            'notes': 'Extensive tariffs imposed on Chinese goods starting in 2018.'
        },
        {
            'text': 'Appoint conservative judges to the Supreme Court',
            'category': 'Judiciary',
            'status': PromiseStatus.FULFILLED,
            'priority': 5,
            'progress_percentage': 100.0,
            'sources': [
                {
                    'title': 'Judicial Nominations Speech',
                    'url': 'https://example.com/judicial-speech',
                    'source_type': SourceType.CAMPAIGN_WEBSITE,
                    'description': 'Promise to appoint conservative judges'
                }
            ],
            'tags': ['supreme-court', 'judges', 'conservative', 'appointments'],
            'notes': 'Appointed three conservative justices: Gorsuch, Kavanaugh, and Barrett.'
        }
    ]
    
    # Add promises to database
    added_promises = []
    for promise_data in sample_promises:
        # Create sources
        sources = []
        for source_data in promise_data['sources']:
            source = Source(
                title=source_data['title'],
                url=source_data['url'],
                source_type=source_data['source_type'],
                description=source_data['description'],
                date=datetime.now() - timedelta(days=1000),  # Simulate older date
                reliability_score=0.8
            )
            sources.append(source)
        
        # Create promise
        promise = Promise(
            text=promise_data['text'],
            category=promise_data['category'],
            status=promise_data['status'],
            priority=promise_data['priority'],
            progress_percentage=promise_data['progress_percentage'],
            sources=sources,
            tags=promise_data['tags'],
            notes=promise_data['notes'],
            date_made=datetime.now() - timedelta(days=1200),  # Simulate campaign date
            date_updated=datetime.now() - timedelta(days=100)   # Simulate recent update
        )
        
        promise_id = db_manager.add_promise(promise)
        added_promises.append(promise_id)
        print(f"Added promise {promise_id}: {promise.text[:50]}...")
    
    print(f"\nAdded {len(added_promises)} sample promises to the database.")
    return added_promises

if __name__ == '__main__':
    create_sample_data()
