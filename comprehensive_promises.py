"""
Comprehensive Trump campaign promises data for the tracker.
"""

from datetime import datetime, timedelta
from app.database import DatabaseManager
from app.models import Promise, Source, PromiseStatus, SourceType

def add_comprehensive_promises():
    """Add a comprehensive list of Trump campaign promises."""
    db_manager = DatabaseManager()
    
    # Comprehensive list of Trump campaign promises
    comprehensive_promises = [
        # Immigration Promises
        {
            'text': 'Complete the border wall and make it 500 feet tall',
            'category': 'Immigration',
            'status': PromiseStatus.IN_PROGRESS,
            'priority': 5,
            'progress_percentage': 25.0,
            'sources': [
                {
                    'title': '2024 Campaign Rally - Texas',
                    'url': 'https://example.com/border-wall-2024',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to complete and enhance border wall'
                }
            ],
            'tags': ['border-security', 'wall', 'immigration'],
            'notes': 'Expanded promise from first term to make wall higher and complete remaining sections.'
        },
        {
            'text': 'Conduct the largest deportation operation in US history',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': '2024 Campaign Announcement',
                    'url': 'https://example.com/deportation-operation',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Mass deportation promise for second term'
                }
            ],
            'tags': ['deportation', 'immigration', 'enforcement'],
            'notes': 'Major campaign promise for second term involving mass deportations.'
        },
        {
            'text': 'End birthright citizenship through executive action',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Immigration Policy Speech',
                    'url': 'https://example.com/birthright-citizenship',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to end birthright citizenship'
                }
            ],
            'tags': ['birthright', 'citizenship', 'constitution'],
            'notes': 'Constitutional challenge expected for this promise.'
        },
        {
            'text': 'Restore and expand Remain in Mexico policy',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Border Security Plan',
                    'url': 'https://example.com/remain-in-mexico',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to restore asylum policies'
                }
            ],
            'tags': ['asylum', 'mexico', 'border'],
            'notes': 'Policy was in place during first term, ended by Biden administration.'
        },
        
        # Economy & Tax Promises
        {
            'text': 'Make the Trump tax cuts permanent',
            'category': 'Tax Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Economic Policy Platform',
                    'url': 'https://example.com/tax-cuts-permanent',
                    'source_type': SourceType.CAMPAIGN_WEBSITE,
                    'description': 'Promise to make TCJA provisions permanent'
                }
            ],
            'tags': ['taxes', 'tcja', 'permanent'],
            'notes': 'Tax Cuts and Jobs Act provisions set to expire in 2025.'
        },
        {
            'text': 'Eliminate taxes on tips for service workers',
            'category': 'Tax Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Nevada Campaign Rally',
                    'url': 'https://example.com/no-tax-tips',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to eliminate federal taxes on tips'
                }
            ],
            'tags': ['tips', 'service-workers', 'taxes'],
            'notes': 'Popular promise among service industry workers.'
        },
        {
            'text': 'Reduce corporate tax rate to 15% for companies that make products in America',
            'category': 'Tax Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Manufacturing Policy Speech',
                    'url': 'https://example.com/corporate-tax-15',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Conditional corporate tax reduction'
                }
            ],
            'tags': ['corporate-tax', 'manufacturing', 'america-first'],
            'notes': 'Would reduce rate from current 21% for domestic manufacturers.'
        },
        {
            'text': 'Implement 10% universal tariff on all foreign goods',
            'category': 'Trade',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Trade Policy Platform',
                    'url': 'https://example.com/universal-tariff',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Universal baseline tariff proposal'
                }
            ],
            'tags': ['tariffs', 'trade', 'universal'],
            'notes': 'Broad tariff policy beyond targeted country/product tariffs.'
        },
        
        # Energy Promises
        {
            'text': 'Drill, baby, drill - expand oil and gas production on day one',
            'category': 'Energy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Energy Independence Rally',
                    'url': 'https://example.com/drill-baby-drill',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to maximize domestic energy production'
                }
            ],
            'tags': ['drilling', 'oil', 'gas', 'day-one'],
            'notes': 'Signature energy policy promise for second term.'
        },
        {
            'text': 'Approve the Keystone XL pipeline immediately',
            'category': 'Energy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Energy Policy Document',
                    'url': 'https://example.com/keystone-xl',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to revive cancelled pipeline'
                }
            ],
            'tags': ['keystone', 'pipeline', 'energy'],
            'notes': 'Pipeline was approved in first term, cancelled by Biden.'
        },
        {
            'text': 'End the war on coal and restore coal mining jobs',
            'category': 'Energy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Coal Country Rally',
                    'url': 'https://example.com/coal-mining',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to revive coal industry'
                }
            ],
            'tags': ['coal', 'mining', 'jobs'],
            'notes': 'Coal industry continues to face market challenges.'
        },
        
        # Healthcare Promises
        {
            'text': 'Replace Obamacare with Trump Care - better and cheaper healthcare',
            'category': 'Healthcare',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Healthcare Policy Platform',
                    'url': 'https://example.com/trump-care',
                    'source_type': SourceType.CAMPAIGN_WEBSITE,
                    'description': 'Renewed promise to replace ACA'
                }
            ],
            'tags': ['healthcare', 'obamacare', 'replacement'],
            'notes': 'Continues promise from first term with new branding.'
        },
        {
            'text': 'Protect Social Security and Medicare with no cuts',
            'category': 'Healthcare',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Senior Citizens Rally',
                    'url': 'https://example.com/social-security-medicare',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to protect entitlement programs'
                }
            ],
            'tags': ['social-security', 'medicare', 'seniors'],
            'notes': 'Important promise for senior voter base.'
        },
        
        # Foreign Policy & Defense
        {
            'text': 'End the war in Ukraine within 24 hours',
            'category': 'Foreign Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 5,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Foreign Policy Interview',
                    'url': 'https://example.com/ukraine-24-hours',
                    'source_type': SourceType.INTERVIEW,
                    'description': 'Promise to quickly end Ukraine conflict'
                }
            ],
            'tags': ['ukraine', 'war', '24-hours', 'peace'],
            'notes': 'Bold promise regarding ongoing international conflict.'
        },
        {
            'text': 'Rebuild the military to be the strongest in the world',
            'category': 'Defense',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Military Policy Speech',
                    'url': 'https://example.com/strongest-military',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to continue military buildup'
                }
            ],
            'tags': ['military', 'defense', 'strongest'],
            'notes': 'Continuation of first-term military investment.'
        },
        {
            'text': 'Move Space Force headquarters to Florida',
            'category': 'Defense',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 2,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Florida Campaign Event',
                    'url': 'https://example.com/space-force-florida',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to relocate Space Force HQ'
                }
            ],
            'tags': ['space-force', 'florida', 'headquarters'],
            'notes': 'Space Force was created during first term.'
        },
        
        # Law & Order
        {
            'text': 'Deploy National Guard to restore order in crime-ridden cities',
            'category': 'Social Issues',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Law and Order Policy',
                    'url': 'https://example.com/national-guard-cities',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to use federal forces for local crime'
                }
            ],
            'tags': ['law-and-order', 'national-guard', 'crime'],
            'notes': 'Federal intervention in local law enforcement.'
        },
        {
            'text': 'Defund sanctuary cities and jurisdictions',
            'category': 'Immigration',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Immigration Enforcement Plan',
                    'url': 'https://example.com/defund-sanctuary-cities',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to cut federal funding to sanctuary jurisdictions'
                }
            ],
            'tags': ['sanctuary-cities', 'funding', 'immigration'],
            'notes': 'Attempted in first term, faced legal challenges.'
        },
        
        # Government Reform
        {
            'text': 'Fire all corrupt deep state bureaucrats on day one',
            'category': 'Other',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Government Reform Rally',
                    'url': 'https://example.com/deep-state-firing',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to purge federal bureaucracy'
                }
            ],
            'tags': ['deep-state', 'bureaucrats', 'government-reform'],
            'notes': 'Broad promise to restructure federal workforce.'
        },
        {
            'text': 'Implement Schedule F to make federal employees fireable',
            'category': 'Other',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Civil Service Reform Plan',
                    'url': 'https://example.com/schedule-f',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to reclassify federal employees'
                }
            ],
            'tags': ['schedule-f', 'federal-employees', 'reform'],
            'notes': 'Policy attempted at end of first term, reversed by Biden.'
        },
        
        # Education
        {
            'text': 'Eliminate the Department of Education',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Education Policy Platform',
                    'url': 'https://example.com/eliminate-education-dept',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to abolish federal education department'
                }
            ],
            'tags': ['education', 'department', 'eliminate'],
            'notes': 'Would require Congressional approval.'
        },
        {
            'text': 'Ban critical race theory and transgender ideology in schools',
            'category': 'Education',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Education Reform Speech',
                    'url': 'https://example.com/ban-crt-transgender',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to restrict certain educational content'
                }
            ],
            'tags': ['critical-race-theory', 'transgender', 'schools'],
            'notes': 'Culture war issue with state vs federal jurisdiction questions.'
        },
        
        # Technology & Free Speech
        {
            'text': 'Break up Big Tech monopolies and restore free speech',
            'category': 'Technology',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Big Tech Policy Speech',
                    'url': 'https://example.com/break-up-big-tech',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to use antitrust against tech companies'
                }
            ],
            'tags': ['big-tech', 'monopolies', 'free-speech'],
            'notes': 'Antitrust enforcement against major tech platforms.'
        },
        {
            'text': 'Create a Truth Social competitor to Twitter/X',
            'category': 'Technology',
            'status': PromiseStatus.PARTIALLY_FULFILLED,
            'priority': 2,
            'progress_percentage': 60.0,
            'sources': [
                {
                    'title': 'Truth Social Launch',
                    'url': 'https://example.com/truth-social',
                    'source_type': SourceType.OFFICIAL_STATEMENT,
                    'description': 'Social media platform launch'
                }
            ],
            'tags': ['truth-social', 'social-media', 'platform'],
            'notes': 'Truth Social exists but has limited market share compared to major platforms.'
        },
        
        # Additional Specific Promises
        {
            'text': 'Pardon all January 6th protesters on day one',
            'category': 'Judiciary',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'January 6th Rally',
                    'url': 'https://example.com/j6-pardons',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to pardon January 6th defendants'
                }
            ],
            'tags': ['january-6', 'pardons', 'protesters'],
            'notes': 'Controversial promise regarding Capitol riot participants.'
        },
        {
            'text': 'Ban Chinese ownership of US farmland and infrastructure',
            'category': 'Foreign Policy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 3,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'China Policy Speech',
                    'url': 'https://example.com/ban-chinese-ownership',
                    'source_type': SourceType.POLICY_DOCUMENT,
                    'description': 'Promise to restrict Chinese investments'
                }
            ],
            'tags': ['china', 'farmland', 'infrastructure', 'ownership'],
            'notes': 'National security justification for investment restrictions.'
        },
        {
            'text': 'Bring back all manufacturing jobs from China',
            'category': 'Economy',
            'status': PromiseStatus.NOT_STARTED,
            'priority': 4,
            'progress_percentage': 0.0,
            'sources': [
                {
                    'title': 'Manufacturing Rally',
                    'url': 'https://example.com/bring-back-manufacturing',
                    'source_type': SourceType.RALLY_SPEECH,
                    'description': 'Promise to reshore manufacturing from China'
                }
            ],
            'tags': ['manufacturing', 'china', 'jobs', 'reshoring'],
            'notes': 'Ambitious promise to reverse decades of offshoring.'
        }
    ]
    
    # Add all comprehensive promises to database
    added_promises = []
    for promise_data in comprehensive_promises:
        # Create sources
        sources = []
        for source_data in promise_data['sources']:
            source = Source(
                title=source_data['title'],
                url=source_data['url'],
                source_type=source_data['source_type'],
                description=source_data['description'],
                date=datetime.now() - timedelta(days=200),  # Simulate campaign dates
                reliability_score=0.9  # High reliability for official sources
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
            date_made=datetime.now() - timedelta(days=300),  # Simulate campaign dates
            date_updated=datetime.now() - timedelta(days=50)   # Simulate recent updates
        )
        
        promise_id = db_manager.add_promise(promise)
        added_promises.append(promise_id)
        print(f"Added promise {promise_id}: {promise.text[:60]}...")
    
    print(f"\n✅ Added {len(added_promises)} comprehensive campaign promises!")
    return added_promises

if __name__ == '__main__':
    print("Adding comprehensive Trump campaign promises...")
    print("=" * 50)
    add_comprehensive_promises()
    
    # Show final stats
    db_manager = DatabaseManager()
    analytics_data = db_manager.get_analytics_data()
    print(f"\n📊 Final Database Statistics:")
    print(f"   Total Promises: {analytics_data['total_promises']}")
    print(f"   Categories Covered: {len(analytics_data['promises_by_category'])}")
    print(f"   Most Active Category: {list(analytics_data['promises_by_category'].keys())[0] if analytics_data['promises_by_category'] else 'None'}")
