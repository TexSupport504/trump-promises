"""
Truth Social and interview promises from Trump's 2024 campaign.
"""

from datetime import datetime, timedelta
from app.database import DatabaseManager
from app.models import Promise, Source, PromiseStatus, SourceType

def add_truth_social_promises():
    """Add promises from Truth Social posts and recent interviews."""
    db_manager = DatabaseManager()
    
    # Truth Social and interview promises
    truth_social_promises = [
        {
            'text': 'Investigate and prosecute election fraud from 2020',
            'category': 'Judiciary',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Truth Social Post - Election Investigation',
                    'url': 'https://truthsocial.com/election-fraud',
                    'source_type': SourceType.SOCIAL_MEDIA,
                    'description': 'Promise to investigate 2020 election claims'
                }
            ],
            'tags': ['election-fraud', '2020-election', 'investigation'],
            'notes': 'Central theme of 2024 campaign regarding 2020 election.'
        },
        {
            'text': 'Cancel all student debt relief programs',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Education Policy Interview',
                    'url': 'https://example.com/cancel-student-debt-relief',
                    'source_type': SourceType.INTERVIEW,
                    'description': 'Opposition to Biden student debt programs'
                }
            ],
            'tags': ['student-debt', 'education', 'cancel'],
            'notes': 'Reversal of Biden administration student debt policies.'
        },
        {
            'text': 'Reinstate all military members fired for vaccine refusal',
            'category': 'Defense',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Military Policy Statement',
                    'url': 'https://example.com/reinstate-military-unvaccinated',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Promise to reinstate discharged service members'
                }
            ],
            'tags': ['military', 'vaccine-mandate', 'reinstate'],
            'notes': 'Response to COVID-19 vaccine requirements in military.'
        },
        {
            'text': 'Create tent cities for homeless in major Democrat cities',
            'category': 'Social Issues',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Homelessness Policy Speech',
                    'url': 'https://example.com/tent-cities-homeless',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Solution for urban homelessness problem'
                }
            ],
            'tags': ['homelessness', 'tent-cities', 'democrat-cities'],
            'notes': 'Controversial approach to addressing urban homelessness.'
        },
        {
            'text': 'Ban trans athletes from women\'s sports nationwide',
            'category': 'Social Issues',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Women\'s Sports Rally',
                    'url': 'https://example.com/ban-trans-athletes',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to protect women\'s sports'
                }
            ],
            'tags': ['transgender', 'sports', 'women', 'ban'],
            'notes': 'Culture war issue with state vs federal jurisdiction questions.'
        },
        {
            'text': 'Revoke China\'s Most Favored Nation trade status',
            'category': 'Trade',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'China Trade Policy',
                    'url': 'https://example.com/revoke-china-mfn',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to end favorable trade status'
                }
            ],
            'tags': ['china', 'most-favored-nation', 'trade-status'],
            'notes': 'Major escalation in trade war with China.'
        },
        {
            'text': 'End all climate change regulations on day one',
            'category': 'Environment',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Energy Independence Speech',
                    'url': 'https://example.com/end-climate-regulations',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to eliminate environmental regulations'
                }
            ],
            'tags': ['climate-change', 'regulations', 'environment'],
            'notes': 'Broad rollback of environmental protections.'
        },
        {
            'text': 'Create American Iron Dome missile defense system',
            'category': 'Defense',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Missile Defense Policy',
                    'url': 'https://example.com/american-iron-dome',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Domestic missile defense system proposal'
                }
            ],
            'tags': ['iron-dome', 'missile-defense', 'homeland-security'],
            'notes': 'Inspired by Israeli Iron Dome system.'
        },
        {
            'text': 'Restore school choice and education savings accounts',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'School Choice Policy Platform',
                    'url': 'https://example.com/school-choice-esa',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Educational voucher and choice programs'
                }
            ],
            'tags': ['school-choice', 'education-savings-accounts', 'vouchers'],
            'notes': 'Private school voucher system expansion.'
        },
        {
            'text': 'Ban federal employees from working for Big Tech after government service',
            'category': 'Technology',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Revolving Door Reform',
                    'url': 'https://example.com/ban-tech-revolving-door',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Ethics reform for tech industry'
                }
            ],
            'tags': ['revolving-door', 'big-tech', 'ethics', 'federal-employees'],
            'notes': 'Anti-corruption measure targeting tech industry influence.'
        },
        {
            'text': 'Establish patriotic education curriculum in schools',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Patriotic Education Commission',
                    'url': 'https://example.com/patriotic-education',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Counter to critical race theory in education'
                }
            ],
            'tags': ['patriotic-education', 'curriculum', 'history'],
            'notes': 'Response to debates over how American history is taught.'
        },
        {
            'text': 'Withdraw from Paris Climate Agreement again',
            'category': 'Environment',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Climate Policy Statement',
                    'url': 'https://example.com/paris-withdrawal-again',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Second withdrawal from climate accord'
                }
            ],
            'tags': ['paris-agreement', 'climate', 'withdrawal'],
            'notes': 'Withdrew in first term, rejoined by Biden, would withdraw again.'
        },
        {
            'text': 'Create new category of visa for skilled immigrants who buy homes',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 2,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Real Estate Investment Immigration',
                    'url': 'https://example.com/visa-home-buyers',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Investment-based immigration pathway'
                }
            ],
            'tags': ['immigration', 'skilled-workers', 'real-estate', 'visa'],
            'notes': 'Economic incentive for skilled immigration through real estate.'
        },
        {
            'text': 'Designate Mexican cartels as foreign terrorist organizations',
            'category': 'Foreign Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Border Security Policy',
                    'url': 'https://example.com/cartels-terrorist-designation',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Terrorist designation for drug cartels'
                }
            ],
            'tags': ['mexican-cartels', 'terrorism', 'border-security'],
            'notes': 'Would enable military action against cartels.'
        },
        {
            'text': 'Eliminate income tax and replace with tariffs only',
            'category': 'Tax Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 2,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Tax Reform Interview',
                    'url': 'https://example.com/eliminate-income-tax',
                    'source_type': SourceType.INTERVIEW,
                    'description': 'Radical tax system overhaul proposal'
                }
            ],
            'tags': ['income-tax', 'tariffs', 'tax-reform'],
            'notes': 'Return to pre-1913 tax system with tariff-based revenue.'
        }
    ]
    
    # Add Truth Social promises to database
    added_promises = []
    for promise_data in truth_social_promises:
        # Create sources
        sources = []
        for source_data in promise_data['sources']:
            source = Source(
                title=source_data['title'],
                url=source_data['url'],
                source_type=source_data['source_type'],
                description=source_data['description'],
                date=datetime.now() - timedelta(days=30),  # Very recent posts/interviews
                reliability_score=0.8   # Slightly lower for social media sources
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
            date_made=datetime.now() - timedelta(days=45),   # Recent campaign dates
            date_updated=datetime.now() - timedelta(days=5)   # Very recent updates
        )
        
        promise_id = db_manager.add_promise(promise)
        added_promises.append(promise_id)
        print(f"Added Truth Social promise {promise_id}: {promise.text[:45]}...")
    
    print(f"\n✅ Added {len(added_promises)} Truth Social/interview promises!")
    return added_promises

if __name__ == '__main__':
    print("Adding Truth Social and interview Trump promises...")
    print("=" * 60)
    add_truth_social_promises()
    
    # Show final stats
    db_manager = DatabaseManager()
    analytics_data = db_manager.get_analytics_data()
    print(f"\n📊 Final Comprehensive Database Statistics:")
    print(f"   Total Promises: {analytics_data['total_promises']}")
    print(f"   Categories: {len(analytics_data['promises_by_category'])}")
    print(f"   Highest Priority Promises: {sum(1 for p in db_manager.get_all_promises() if p.priority == 5)}")
    print(f"   Most Common Status: {max(analytics_data['promises_by_status'], key=analytics_data['promises_by_status'].get)}")
