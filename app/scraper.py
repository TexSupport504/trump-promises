"""
Web scraping utilities for collecting Trump's campaign promises from various sources.
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from urllib.parse import urljoin, urlparse
import feedparser
from dataclasses import dataclass

from .models import Promise, Source, SourceType, PromiseStatus


@dataclass
class ScrapedPromise:
    """Represents a scraped promise before processing."""
    text: str
    source_url: str
    source_title: str
    date_found: Optional[datetime] = None
    context: str = ""
    confidence_score: float = 0.5


class PromiseScraper:
    """Scrapes campaign promises from various online sources."""
    
    def __init__(self, delay_seconds: float = 1.0):
        self.delay_seconds = delay_seconds
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Keywords that commonly indicate promises
        self.promise_keywords = [
            'will', 'going to', 'plan to', 'promise', 'pledge', 'commit',
            'on day one', 'first day', 'immediately', 'executive order',
            'we\'re going to', 'i\'m going to', 'we will', 'i will'
        ]
        
        # Categories for automatic classification
        self.category_keywords = {
            'Economy': ['jobs', 'economy', 'unemployment', 'economic', 'business', 'trade deal', 'gdp'],
            'Immigration': ['border', 'wall', 'illegal', 'immigration', 'deportation', 'visa', 'asylum'],
            'Healthcare': ['healthcare', 'health care', 'insurance', 'medicare', 'medicaid', 'obamacare'],
            'Foreign Policy': ['foreign', 'nato', 'allies', 'diplomacy', 'embassy', 'ambassador'],
            'Defense': ['military', 'defense', 'armed forces', 'veterans', 'war', 'security'],
            'Energy': ['energy', 'oil', 'gas', 'renewable', 'pipeline', 'drilling', 'coal'],
            'Tax Policy': ['tax', 'taxes', 'irs', 'deduction', 'credit', 'revenue'],
            'Infrastructure': ['infrastructure', 'roads', 'bridges', 'transportation', 'airports']
        }
    
    def scrape_campaign_website(self, url: str) -> List[ScrapedPromise]:
        """Scrape promises from campaign website."""
        promises = []
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for promise-related content
            promise_sections = soup.find_all(['p', 'li', 'div'], 
                                           text=re.compile('|'.join(self.promise_keywords), re.IGNORECASE))
            
            for section in promise_sections:
                text = section.get_text().strip()
                if len(text) > 20 and self._is_likely_promise(text):
                    promises.append(ScrapedPromise(
                        text=text,
                        source_url=url,
                        source_title=soup.title.get_text() if soup.title else "Campaign Website",
                        date_found=datetime.now(),
                        confidence_score=self._calculate_promise_confidence(text)
                    ))
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        time.sleep(self.delay_seconds)
        return promises
    
    def scrape_news_articles(self, search_query: str = "Trump promises") -> List[ScrapedPromise]:
        """Scrape promises from news articles (placeholder - would need news API)."""
        # This would integrate with news APIs like NewsAPI, Google News, etc.
        # For now, returning empty list as placeholder
        print(f"Would search for news articles with query: {search_query}")
        return []
    
    def scrape_speech_transcripts(self, transcript_urls: List[str]) -> List[ScrapedPromise]:
        """Scrape promises from speech transcripts."""
        promises = []
        
        for url in transcript_urls:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract text content
                text_content = soup.get_text()
                
                # Split into sentences and analyze each
                sentences = re.split(r'[.!?]+', text_content)
                
                for sentence in sentences:
                    sentence = sentence.strip()
                    if len(sentence) > 20 and self._is_likely_promise(sentence):
                        promises.append(ScrapedPromise(
                            text=sentence,
                            source_url=url,
                            source_title="Speech Transcript",
                            date_found=datetime.now(),
                            confidence_score=self._calculate_promise_confidence(sentence)
                        ))
                
            except Exception as e:
                print(f"Error scraping transcript {url}: {e}")
            
            time.sleep(self.delay_seconds)
        
        return promises
    
    def scrape_rss_feeds(self, feed_urls: List[str]) -> List[ScrapedPromise]:
        """Scrape promises from RSS feeds."""
        promises = []
        
        for feed_url in feed_urls:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    # Analyze entry content for promises
                    content = entry.get('description', '') or entry.get('summary', '')
                    
                    if self._contains_promise_language(content):
                        promises.append(ScrapedPromise(
                            text=content[:500] + "..." if len(content) > 500 else content,
                            source_url=entry.get('link', feed_url),
                            source_title=entry.get('title', 'RSS Feed Entry'),
                            date_found=datetime.now(),
                            confidence_score=self._calculate_promise_confidence(content)
                        ))
                
            except Exception as e:
                print(f"Error scraping RSS feed {feed_url}: {e}")
            
            time.sleep(self.delay_seconds)
        
        return promises
    
    def _is_likely_promise(self, text: str) -> bool:
        """Determine if text is likely to contain a promise."""
        text_lower = text.lower()
        
        # Check for promise keywords
        has_promise_keywords = any(keyword in text_lower for keyword in self.promise_keywords)
        
        # Check for future tense indicators
        future_indicators = ['will', 'going to', 'plan to', 'intend to', 'shall']
        has_future_tense = any(indicator in text_lower for indicator in future_indicators)
        
        # Check minimum length
        is_substantial = len(text.split()) >= 5
        
        return has_promise_keywords and has_future_tense and is_substantial
    
    def _contains_promise_language(self, text: str) -> bool:
        """Check if text contains promise-related language."""
        return any(keyword in text.lower() for keyword in self.promise_keywords)
    
    def _calculate_promise_confidence(self, text: str) -> float:
        """Calculate confidence score for a potential promise."""
        score = 0.0
        text_lower = text.lower()
        
        # Base score for promise keywords
        keyword_matches = sum(1 for keyword in self.promise_keywords if keyword in text_lower)
        score += min(keyword_matches * 0.2, 0.6)
        
        # Bonus for specific commitment language
        strong_commitments = ['pledge', 'promise', 'guarantee', 'commit', 'swear']
        if any(commitment in text_lower for commitment in strong_commitments):
            score += 0.3
        
        # Bonus for actionable language
        action_words = ['build', 'create', 'eliminate', 'reduce', 'increase', 'implement']
        if any(action in text_lower for action in action_words):
            score += 0.2
        
        # Penalty for vague language
        vague_words = ['maybe', 'possibly', 'might', 'could', 'probably']
        if any(vague in text_lower for vague in vague_words):
            score -= 0.2
        
        return min(max(score, 0.0), 1.0)
    
    def categorize_promise(self, promise_text: str) -> str:
        """Automatically categorize a promise based on its content."""
        text_lower = promise_text.lower()
        
        # Count keyword matches for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or 'Other' if no matches
        if category_scores:
            return max(category_scores, key=category_scores.get)
        return 'Other'
    
    def convert_to_promise(self, scraped_promise: ScrapedPromise) -> Promise:
        """Convert a scraped promise to a Promise object."""
        # Create source
        source = Source(
            url=scraped_promise.source_url,
            title=scraped_promise.source_title,
            source_type=SourceType.OTHER,  # Could be improved with URL analysis
            date=scraped_promise.date_found,
            description=f"Scraped on {scraped_promise.date_found}",
            reliability_score=scraped_promise.confidence_score
        )
        
        # Create promise
        promise = Promise(
            text=scraped_promise.text,
            category=self.categorize_promise(scraped_promise.text),
            status=PromiseStatus.NOT_STARTED,
            date_made=scraped_promise.date_found,
            sources=[source],
            tags=self._extract_tags(scraped_promise.text)
        )
        
        return promise
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from promise text."""
        tags = []
        text_lower = text.lower()
        
        # Policy area tags
        if 'tax' in text_lower:
            tags.append('taxes')
        if 'job' in text_lower:
            tags.append('employment')
        if 'border' in text_lower or 'wall' in text_lower:
            tags.append('border-security')
        if 'health' in text_lower:
            tags.append('healthcare')
        if 'trade' in text_lower:
            tags.append('trade')
        if 'energy' in text_lower:
            tags.append('energy')
        
        # Timeline tags
        if any(phrase in text_lower for phrase in ['day one', 'first day', 'immediately']):
            tags.append('immediate')
        if any(phrase in text_lower for phrase in ['100 days', 'first 100']):
            tags.append('100-days')
        
        return tags


# Example usage and predefined source lists
class PromiseSourceManager:
    """Manages lists of sources for promise scraping."""
    
    # Common sources for Trump promises (examples)
    CAMPAIGN_WEBSITES = [
        "https://www.donaldjtrump.com/platform",
        # Add more official campaign URLs
    ]
    
    RSS_FEEDS = [
        # Add RSS feeds from news sources, campaign feeds, etc.
    ]
    
    SPEECH_TRANSCRIPT_URLS = [
        # Add URLs to speech transcripts
    ]
    
    @staticmethod
    def get_all_sources() -> Dict[str, List[str]]:
        """Get all configured sources."""
        return {
            'campaign_websites': PromiseSourceManager.CAMPAIGN_WEBSITES,
            'rss_feeds': PromiseSourceManager.RSS_FEEDS,
            'speech_transcripts': PromiseSourceManager.SPEECH_TRANSCRIPT_URLS
        }
