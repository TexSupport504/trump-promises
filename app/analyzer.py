"""
Analysis utilities for Trump campaign promises.
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
import math

from .models import Promise, PromiseStatus, AnalyticsData
from .database import DatabaseManager


class PromiseAnalyzer:
    """Analyzes campaign promises for insights and trends."""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    def generate_analytics_report(self) -> AnalyticsData:
        """Generate comprehensive analytics report."""
        promises = self.db_manager.get_all_promises()
        
        if not promises:
            return AnalyticsData()
        
        # Basic statistics
        total_promises = len(promises)
        promises_by_status = self._count_by_status(promises)
        promises_by_category = self._count_by_category(promises)
        
        # Calculate fulfillment metrics
        fulfilled_count = (promises_by_status.get('Fulfilled', 0) + 
                          promises_by_status.get('Partially Fulfilled', 0))
        fulfillment_rate = (fulfilled_count / total_promises * 100) if total_promises > 0 else 0.0
        
        # Average progress
        total_progress = sum(promise.progress_percentage for promise in promises)
        average_progress = total_progress / total_promises if total_promises > 0 else 0.0
        
        # Most active categories (by count)
        most_active_categories = [category for category, count in 
                                sorted(promises_by_category.items(), 
                                      key=lambda x: x[1], reverse=True)[:5]]
        
        # Recent updates
        recent_updates = self._get_recent_updates(promises, limit=10)
        
        return AnalyticsData(
            total_promises=total_promises,
            promises_by_status=promises_by_status,
            promises_by_category=promises_by_category,
            fulfillment_rate=fulfillment_rate,
            average_progress=average_progress,
            most_active_categories=most_active_categories,
            recent_updates=recent_updates
        )
    
    def _count_by_status(self, promises: List[Promise]) -> Dict[str, int]:
        """Count promises by status."""
        status_counts = defaultdict(int)
        for promise in promises:
            status_counts[promise.status.value] += 1
        return dict(status_counts)
    
    def _count_by_category(self, promises: List[Promise]) -> Dict[str, int]:
        """Count promises by category."""
        category_counts = defaultdict(int)
        for promise in promises:
            category_counts[promise.category] += 1
        return dict(category_counts)
    
    def _get_recent_updates(self, promises: List[Promise], limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent promise updates."""
        updates = []
        
        for promise in promises:
            updates.append({
                'promise_id': promise.id,
                'promise_text': promise.text[:100] + "..." if len(promise.text) > 100 else promise.text,
                'status': promise.status.value,
                'category': promise.category,
                'last_updated': promise.date_updated.isoformat(),
                'progress': promise.progress_percentage
            })
        
        # Sort by last updated and limit
        updates.sort(key=lambda x: x['last_updated'], reverse=True)
        return updates[:limit]
    
    def analyze_promise_trends(self, days_back: int = 30) -> Dict[str, Any]:
        """Analyze trends in promises over time."""
        promises = self.db_manager.get_all_promises()
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Filter recent promises
        recent_promises = [p for p in promises if p.date_updated >= cutoff_date]
        
        # Analyze trends
        trends = {
            'new_promises': len([p for p in recent_promises if p.created_at >= cutoff_date]),
            'status_changes': len([p for p in recent_promises if p.date_updated >= cutoff_date]),
            'category_activity': self._analyze_category_activity(recent_promises),
            'progress_trends': self._analyze_progress_trends(promises, days_back),
            'fulfillment_velocity': self._calculate_fulfillment_velocity(promises, days_back)
        }
        
        return trends
    
    def _analyze_category_activity(self, promises: List[Promise]) -> Dict[str, int]:
        """Analyze activity by category."""
        activity = defaultdict(int)
        for promise in promises:
            activity[promise.category] += 1
        return dict(activity)
    
    def _analyze_progress_trends(self, promises: List[Promise], days_back: int) -> Dict[str, float]:
        """Analyze progress trends."""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Calculate average progress for recent vs. older promises
        recent_promises = [p for p in promises if p.date_updated >= cutoff_date]
        older_promises = [p for p in promises if p.date_updated < cutoff_date]
        
        recent_avg = sum(p.progress_percentage for p in recent_promises) / len(recent_promises) if recent_promises else 0
        older_avg = sum(p.progress_percentage for p in older_promises) / len(older_promises) if older_promises else 0
        
        return {
            'recent_average_progress': recent_avg,
            'older_average_progress': older_avg,
            'progress_change': recent_avg - older_avg
        }
    
    def _calculate_fulfillment_velocity(self, promises: List[Promise], days_back: int) -> float:
        """Calculate rate of promise fulfillment."""
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        fulfilled_recently = len([
            p for p in promises 
            if p.status in [PromiseStatus.FULFILLED, PromiseStatus.PARTIALLY_FULFILLED] 
            and p.date_updated >= cutoff_date
        ])
        
        return fulfilled_recently / days_back if days_back > 0 else 0.0
    
    def find_similar_promises(self, promise: Promise, threshold: float = 0.3) -> List[Tuple[Promise, float]]:
        """Find promises similar to the given promise."""
        all_promises = self.db_manager.get_all_promises()
        similar_promises = []
        
        for other_promise in all_promises:
            if other_promise.id == promise.id:
                continue
            
            similarity = self._calculate_text_similarity(promise.text, other_promise.text)
            if similarity >= threshold:
                similar_promises.append((other_promise, similarity))
        
        # Sort by similarity score
        similar_promises.sort(key=lambda x: x[1], reverse=True)
        return similar_promises
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts using basic word overlap."""
        # Simple word-based similarity (could be improved with NLP libraries)
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def analyze_promise_complexity(self, promise: Promise) -> Dict[str, Any]:
        """Analyze the complexity and specificity of a promise."""
        text = promise.text
        
        # Basic metrics
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Specificity indicators
        specific_numbers = len(re.findall(r'\b\d+\b', text))
        specific_dates = len(re.findall(r'\b\d{4}\b|\bday one\b|\bfirst day\b', text))
        specific_amounts = len(re.findall(r'\$[\d,]+|\b\d+\s*(million|billion|trillion|percent|%)', text))
        
        # Action words
        action_words = ['build', 'create', 'eliminate', 'reduce', 'increase', 'implement', 
                       'establish', 'end', 'start', 'begin', 'stop', 'cancel']
        action_count = sum(1 for word in action_words if word in text.lower())
        
        # Qualifier words (indicating uncertainty)
        qualifier_words = ['maybe', 'possibly', 'might', 'could', 'probably', 'try', 'attempt']
        qualifier_count = sum(1 for word in qualifier_words if word in text.lower())
        
        # Calculate complexity score
        complexity_score = min((
            word_count * 0.01 +
            specific_numbers * 0.1 +
            specific_dates * 0.15 +
            specific_amounts * 0.2 +
            action_count * 0.1 -
            qualifier_count * 0.1
        ), 1.0)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_words_per_sentence': avg_words_per_sentence,
            'specific_numbers': specific_numbers,
            'specific_dates': specific_dates,
            'specific_amounts': specific_amounts,
            'action_words': action_count,
            'qualifier_words': qualifier_count,
            'complexity_score': max(complexity_score, 0.0),
            'specificity_level': self._classify_specificity(complexity_score)
        }
    
    def _classify_specificity(self, score: float) -> str:
        """Classify promise specificity based on score."""
        if score >= 0.7:
            return "Very Specific"
        elif score >= 0.5:
            return "Specific"
        elif score >= 0.3:
            return "Moderate"
        elif score >= 0.1:
            return "Vague"
        else:
            return "Very Vague"
    
    def generate_priority_recommendations(self, promises: List[Promise]) -> List[Dict[str, Any]]:
        """Generate recommendations for promise prioritization."""
        recommendations = []
        
        for promise in promises:
            complexity = self.analyze_promise_complexity(promise)
            
            # Calculate recommendation score
            score = 0.0
            factors = []
            
            # High specificity promises are easier to track
            if complexity['specificity_level'] in ['Very Specific', 'Specific']:
                score += 0.3
                factors.append("High specificity makes tracking easier")
            
            # Promises with recent activity
            days_since_update = (datetime.now() - promise.date_updated).days
            if days_since_update < 30:
                score += 0.2
                factors.append("Recent activity indicates priority")
            
            # Category importance (could be weighted based on current events)
            high_priority_categories = ['Economy', 'Healthcare', 'Immigration']
            if promise.category in high_priority_categories:
                score += 0.2
                factors.append(f"{promise.category} is a high-priority category")
            
            # Progress stagnation
            if promise.status == PromiseStatus.IN_PROGRESS and days_since_update > 60:
                score += 0.3
                factors.append("Progress appears stagnant, needs attention")
            
            recommendations.append({
                'promise_id': promise.id,
                'promise_text': promise.text[:100] + "..." if len(promise.text) > 100 else promise.text,
                'recommendation_score': score,
                'factors': factors,
                'suggested_action': self._suggest_action(promise, score)
            })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x['recommendation_score'], reverse=True)
        return recommendations
    
    def _suggest_action(self, promise: Promise, score: float) -> str:
        """Suggest action based on promise analysis."""
        if score >= 0.6:
            return "High priority - track closely and update frequently"
        elif score >= 0.4:
            return "Medium priority - monitor for changes"
        elif promise.status == PromiseStatus.NOT_STARTED:
            return "Low priority - check for any initial progress"
        else:
            return "Maintain current monitoring level"
    
    def export_analysis_report(self, format_type: str = "dict") -> Dict[str, Any]:
        """Export comprehensive analysis report."""
        analytics = self.generate_analytics_report()
        trends = self.analyze_promise_trends()
        promises = self.db_manager.get_all_promises()
        recommendations = self.generate_priority_recommendations(promises)
        
        report = {
            'report_date': datetime.now().isoformat(),
            'analytics': analytics.to_dict(),
            'trends': trends,
            'recommendations': recommendations[:10],  # Top 10 recommendations
            'summary': {
                'total_promises': analytics.total_promises,
                'fulfillment_rate': analytics.fulfillment_rate,
                'most_active_category': analytics.most_active_categories[0] if analytics.most_active_categories else "None",
                'recommendations_count': len(recommendations)
            }
        }
        
        return report
