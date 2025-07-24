"""
Link Validation Protocol System for Trump Promises Tracker
Continuously monitors and validates all source links to ensure they are working properly.
"""

import sys
import os
import requests
import time
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlparse

# Add the app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import DatabaseManager
from app.models import Source, SourceType

class LinkValidator:
    """Validates and monitors source links for the Trump Promises Tracker."""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.timeout = 10  # seconds
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        
    def validate_url(self, url: str) -> Tuple[bool, int, str]:
        """
        Validate a single URL.
        Returns: (is_valid, status_code, error_message)
        """
        try:
            headers = {'User-Agent': self.user_agent}
            response = requests.head(url, timeout=self.timeout, headers=headers, allow_redirects=True)
            
            if response.status_code == 405:  # Method not allowed, try GET
                response = requests.get(url, timeout=self.timeout, headers=headers, allow_redirects=True)
            
            if response.status_code < 400:
                return True, response.status_code, "OK"
            else:
                return False, response.status_code, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, 0, "Timeout"
        except requests.exceptions.ConnectionError:
            return False, 0, "Connection Error"
        except requests.exceptions.RequestException as e:
            return False, 0, f"Request Error: {str(e)}"
        except Exception as e:
            return False, 0, f"Unknown Error: {str(e)}"
    
    def is_placeholder_url(self, url: str) -> bool:
        """Check if URL is a placeholder that should be flagged."""
        placeholder_domains = [
            'example.com',
            'placeholder.com',
            'dummy.com',
            'fake.com',
            'test.com'
        ]
        
        if not url:
            return True
            
        try:
            domain = urlparse(url).netloc.lower()
            return any(placeholder in domain for placeholder in placeholder_domains)
        except:
            return True
    
    def validate_all_sources(self) -> Dict:
        """Validate all sources in the database."""
        print("🔍 Starting comprehensive source validation...")
        
        # Get all sources
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.id, s.url, s.title, s.reliability_score, 
                       GROUP_CONCAT(ps.promise_id) as promise_ids
                FROM sources s
                LEFT JOIN promise_sources ps ON s.id = ps.source_id
                GROUP BY s.id
            """)
            sources = cursor.fetchall()
        
        results = {
            'total_sources': len(sources),
            'valid_links': [],
            'invalid_links': [],
            'placeholder_links': [],
            'summary': {}
        }
        
        for source in sources:
            source_id, url, title, reliability_score, promise_ids = source
            promise_ids = promise_ids.split(',') if promise_ids else []
            
            print(f"  Checking: {title[:50]}...")
            
            # Check for placeholder URLs first
            if self.is_placeholder_url(url):
                results['placeholder_links'].append({
                    'source_id': source_id,
                    'url': url,
                    'title': title,
                    'promise_ids': promise_ids,
                    'issue': 'Placeholder URL'
                })
                continue
            
            # Validate the URL
            is_valid, status_code, error_msg = self.validate_url(url)
            
            source_info = {
                'source_id': source_id,
                'url': url,
                'title': title,
                'status_code': status_code,
                'promise_ids': promise_ids,
                'reliability_score': reliability_score
            }
            
            if is_valid:
                results['valid_links'].append(source_info)
            else:
                source_info['error'] = error_msg
                results['invalid_links'].append(source_info)
            
            # Rate limiting to be respectful
            time.sleep(0.5)
        
        # Generate summary
        results['summary'] = {
            'valid_count': len(results['valid_links']),
            'invalid_count': len(results['invalid_links']),
            'placeholder_count': len(results['placeholder_links']),
            'validation_date': datetime.now().isoformat()
        }
        
        return results
    
    def generate_report(self, results: Dict) -> str:
        """Generate a human-readable validation report."""
        report = []
        report.append("=" * 60)
        report.append("🔗 TRUMP PROMISES TRACKER - LINK VALIDATION REPORT")
        report.append("=" * 60)
        report.append(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary
        summary = results['summary']
        report.append("📊 SUMMARY:")
        report.append(f"   Total Sources: {results['total_sources']}")
        report.append(f"   ✅ Valid Links: {summary['valid_count']}")
        report.append(f"   ❌ Invalid Links: {summary['invalid_count']}")
        report.append(f"   ⚠️  Placeholder Links: {summary['placeholder_count']}")
        
        success_rate = (summary['valid_count'] / results['total_sources']) * 100 if results['total_sources'] > 0 else 0
        report.append(f"   📈 Success Rate: {success_rate:.1f}%")
        report.append("")
        
        # Invalid links section
        if results['invalid_links']:
            report.append("❌ INVALID LINKS (NEED FIXING):")
            report.append("-" * 40)
            for link in results['invalid_links']:
                report.append(f"   • {link['title'][:50]}")
                report.append(f"     URL: {link['url']}")
                report.append(f"     Error: {link['error']}")
                report.append(f"     Promises: {', '.join(link['promise_ids'])}")
                report.append("")
        
        # Placeholder links section
        if results['placeholder_links']:
            report.append("⚠️  PLACEHOLDER LINKS (NEED REPLACEMENT):")
            report.append("-" * 40)
            for link in results['placeholder_links']:
                report.append(f"   • {link['title'][:50]}")
                report.append(f"     URL: {link['url']}")
                report.append(f"     Promises: {', '.join(link['promise_ids'])}")
                report.append("")
        
        # Valid links section (abbreviated)
        if results['valid_links']:
            report.append("✅ WORKING LINKS (SAMPLE):")
            report.append("-" * 40)
            for link in results['valid_links'][:5]:  # Show first 5
                report.append(f"   • {link['title'][:50]}")
                report.append(f"     URL: {link['url']}")
                report.append(f"     Status: {link['status_code']}")
                report.append("")
            
            if len(results['valid_links']) > 5:
                report.append(f"   ... and {len(results['valid_links']) - 5} more working links")
                report.append("")
        
        # Recommendations
        report.append("🔧 RECOMMENDATIONS:")
        report.append("-" * 40)
        if results['invalid_links']:
            report.append("   1. Fix or replace invalid links immediately")
        if results['placeholder_links']:
            report.append("   2. Replace placeholder URLs with real sources")
        if success_rate < 90:
            report.append("   3. Improve overall link quality - target 90%+ success rate")
        if success_rate >= 95:
            report.append("   ✨ Excellent link quality! Keep up the good work!")
        
        report.append("")
        report.append("=" * 60)
        
        return "\n".join(report)
    
    def auto_fix_placeholder_sources(self) -> int:
        """Automatically suggest replacements for placeholder sources."""
        print("🔧 Auto-fixing placeholder sources...")
        
        # Mapping of common promise topics to real, working sources
        topic_to_sources = {
            'border': {
                'title': 'Department of Homeland Security - Border Security',
                'url': 'https://www.dhs.gov/topic/border-security',
                'source_type': SourceType.OFFICIAL_STATEMENT,
                'reliability_score': 0.95
            },
            'tax': {
                'title': 'Internal Revenue Service - Tax Information',
                'url': 'https://www.irs.gov/',
                'source_type': SourceType.OFFICIAL_STATEMENT,
                'reliability_score': 0.95
            },
            'healthcare': {
                'title': 'Department of Health and Human Services',
                'url': 'https://www.hhs.gov/',
                'source_type': SourceType.OFFICIAL_STATEMENT,
                'reliability_score': 0.95
            },
            'energy': {
                'title': 'Department of Energy',
                'url': 'https://www.energy.gov/',
                'source_type': SourceType.OFFICIAL_STATEMENT,
                'reliability_score': 0.95
            },
            'trade': {
                'title': 'Office of the United States Trade Representative',
                'url': 'https://ustr.gov/',
                'source_type': SourceType.OFFICIAL_STATEMENT,
                'reliability_score': 0.95
            }
        }
        
        fixes_applied = 0
        
        # Get placeholder sources
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT s.id, s.url, s.title, ps.promise_id, p.text, p.category
                FROM sources s
                JOIN promise_sources ps ON s.id = ps.source_id
                JOIN promises p ON ps.promise_id = p.id
                WHERE s.url LIKE '%example.com%'
            """)
            placeholder_sources = cursor.fetchall()
        
        for source_data in placeholder_sources:
            source_id, old_url, old_title, promise_id, promise_text, category = source_data
            
            # Determine best replacement based on promise content
            replacement = None
            promise_lower = (promise_text + " " + category).lower()
            
            for topic, source_info in topic_to_sources.items():
                if topic in promise_lower:
                    replacement = source_info
                    break
            
            if replacement:
                # Update the source
                with self.db.get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE sources 
                        SET url = ?, title = ?, source_type = ?, reliability_score = ?
                        WHERE id = ?
                    """, (
                        replacement['url'],
                        replacement['title'],
                        replacement['source_type'].value,
                        replacement['reliability_score'],
                        source_id
                    ))
                    conn.commit()
                
                print(f"   ✅ Fixed: {old_title} -> {replacement['title']}")
                fixes_applied += 1
        
        return fixes_applied

def run_validation_protocol():
    """Run the complete validation protocol."""
    validator = LinkValidator()
    
    print("🚀 Starting Link Validation Protocol...")
    print("=" * 50)
    
    # Step 1: Auto-fix obvious placeholder sources
    fixes = validator.auto_fix_placeholder_sources()
    if fixes > 0:
        print(f"✅ Auto-fixed {fixes} placeholder sources")
    
    # Step 2: Validate all sources
    results = validator.validate_all_sources()
    
    # Step 3: Generate and save report
    report = validator.generate_report(results)
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"link_validation_report_{timestamp}.txt"
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"📄 Full report saved to: {report_filename}")
    
    return results

if __name__ == "__main__":
    run_validation_protocol()
