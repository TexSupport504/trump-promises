"""
Additional recent Trump campaign promises from 2024 campaign events.
"""

from datetime import datetime, timedelta
from app.database import DatabaseManager
from app.models import Promise, Source, PromiseStatus, SourceType

def add_recent_campaign_promises():
    """Add the most recent 2024 campaign promises."""
    db_manager = DatabaseManager()
    
    # Recent 2024 campaign promises
    recent_promises = [
        {
            'text': 'Create baby bonuses to encourage higher birth rates',
            'category': 'Social Issues',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Family Values Rally 2024',
                    'url': 'https://example.com/baby-bonuses',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to provide financial incentives for families'
                }
            ],
            'tags': ['family', 'babies', 'birth-rate', 'bonuses'],
            'notes': 'Demographic policy to address declining birth rates.'
        },
        {
            'text': 'Ban lab-grown meat to protect American farmers',
            'category': 'Agriculture',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 2,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Iowa Farmer Rally',
                    'url': 'https://example.com/ban-lab-meat',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to prohibit synthetic meat production'
                }
            ],
            'tags': ['lab-meat', 'farmers', 'agriculture', 'ban'],
            'notes': 'Protectionist policy for traditional agriculture industry.'
        },
        {
            'text': 'Eliminate electric vehicle mandates on day one',
            'category': 'Transportation',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Auto Workers Rally Michigan',
                    'url': 'https://example.com/eliminate-ev-mandates',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to end federal EV requirements'
                }
            ],
            'tags': ['electric-vehicles', 'mandates', 'auto-industry'],
            'notes': 'Reversal of Biden administration EV policies.'
        },
        {
            'text': 'Build 10 new Freedom Cities on federal land',
            'category': 'Other',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 2,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Future Cities Policy Video',
                    'url': 'https://example.com/freedom-cities',
                    'source_type': SourceType.CAMPAIGN_WEBSITE,
                    'description': 'Ambitious urban development proposal'
                }
            ],
            'tags': ['freedom-cities', 'urban-development', 'federal-land'],
            'notes': 'Futuristic urban planning proposal with flying cars.'
        },
        {
            'text': 'Create quantum computing initiative to beat China',
            'category': 'Technology',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Technology Leadership Speech',
                    'url': 'https://example.com/quantum-computing',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to lead in quantum technology'
                }
            ],
            'tags': ['quantum-computing', 'china', 'technology', 'innovation'],
            'notes': 'Competition with China in emerging technologies.'
        },
        {
            'text': 'Establish merit-based immigration system like Canada',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Immigration Reform Policy',
                    'url': 'https://example.com/merit-based-immigration',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Points-based immigration system proposal'
                }
            ],
            'tags': ['merit-based', 'immigration', 'canada', 'points-system'],
            'notes': 'Shift from family-based to skills-based immigration.'
        },
        {
            'text': 'Bring back prayer in public schools',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Faith Leaders Summit',
                    'url': 'https://example.com/school-prayer',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to restore prayer in schools'
                }
            ],
            'tags': ['prayer', 'schools', 'religion', 'faith'],
            'notes': 'Constitutional challenges expected regarding separation of church and state.'
        },
        {
            'text': 'Withdraw from World Health Organization permanently',
            'category': 'Foreign Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'WHO Criticism Rally',
                    'url': 'https://example.com/withdraw-who',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to leave WHO over COVID response'
                }
            ],
            'tags': ['who', 'world-health-organization', 'covid', 'withdrawal'],
            'notes': 'Started WHO withdrawal process in first term, rejoined by Biden.'
        },
        {
            'text': 'Ban gain-of-function research in US laboratories',
            'category': 'Healthcare',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Lab Research Policy',
                    'url': 'https://example.com/ban-gain-of-function',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to prohibit certain viral research'
                }
            ],
            'tags': ['gain-of-function', 'laboratories', 'research', 'covid'],
            'notes': 'Response to COVID-19 origin theories and lab leak hypothesis.'
        },
        {
            'text': 'Establish National Garden of American Heroes',
            'category': 'Social Issues',
            'status': PromiseStatus.PARTIALLY_FULFILLED,
            'priority': 2,
            'progress_percentage': 30.0,
            'sources': [
                {
                    'title': 'Heroes Garden Executive Order',
                    'url': 'https://example.com/heroes-garden',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Patriotic statuary garden proposal'
                }
            ],
            'tags': ['heroes-garden', 'statues', 'patriotism', 'history'],
            'notes': 'Executive order signed in first term but not fully implemented.'
        },
        {
            'text': 'Create flying car certification program',
            'category': 'Transportation',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 1,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Transportation Innovation Speech',
                    'url': 'https://example.com/flying-cars',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to enable flying car industry'
                }
            ],
            'tags': ['flying-cars', 'transportation', 'innovation', 'faa'],
            'notes': 'Part of futuristic transportation vision.'
        },
        {
            'text': 'Eliminate federal funding for NPR and PBS',
            'category': 'Media',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Media Bias Rally',
                    'url': 'https://example.com/defund-npr-pbs',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to end public broadcasting funding'
                }
            ],
            'tags': ['npr', 'pbs', 'public-broadcasting', 'defund'],
            'notes': 'Criticism of perceived liberal bias in public media.'
        },
        {
            'text': 'Ban TikTok unless sold to American company',
            'category': 'Technology',
            'status': PromiseStatus.PARTIALLY_FULFILLED,
            'priority': 4,
            'progress_percentage': 40.0,
            'sources': [
                {
                    'title': 'TikTok Ban Executive Order',
                    'url': 'https://example.com/tiktok-ban',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'National security concerns over Chinese ownership'
                }
            ],
            'tags': ['tiktok', 'china', 'national-security', 'ban'],
            'notes': 'Attempted ban in first term, legal challenges ongoing.'
        }
    ]
    
    # Add recent promises to database
    added_promises = []
    for promise_data in recent_promises:
        # Create sources
        sources = []
        for source_data in promise_data['sources']:
            source = Source(
                title=source_data['title'],
                url=source_data['url'],
                source_type=source_data['source_type'],
                description=source_data['description'],
                date=datetime.now() - timedelta(days=60),  # Recent campaign events
                reliability_score=0.85  # High reliability for campaign sources
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
            date_made=datetime.now() - timedelta(days=90),   # Recent campaign dates
            date_updated=datetime.now() - timedelta(days=10)  # Very recent updates
        )
        
        promise_id = db_manager.add_promise(promise)
        added_promises.append(promise_id)
        print(f"Added recent promise {promise_id}: {promise.text[:50]}...")
    
    print(f"\n✅ Added {len(added_promises)} recent campaign promises!")
    return added_promises

if __name__ == '__main__':
    print("Adding recent 2024 Trump campaign promises...")
    print("=" * 50)
    add_recent_campaign_promises()
    
    # Show final stats
    db_manager = DatabaseManager()
    analytics_data = db_manager.get_analytics_data()
    print(f"\n📊 Updated Database Statistics:")
    print(f"   Total Promises: {analytics_data['total_promises']}")
    print(f"   Categories: {', '.join(analytics_data['promises_by_category'].keys())}")
    print(f"   Promise Sources: {sum(len(p.sources) for p in db_manager.get_all_promises())}")
