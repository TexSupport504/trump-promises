"""
Advanced analytics module for Trump Promises Tracker.
Provides enhanced progress tracking, comparative analysis, and reporting capabilities.
"""

import json
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict, Counter
import sqlite3

from .database import DatabaseManager
from .models import Promise, ProgressUpdate, PromiseStatus


class AdvancedAnalytics:
    """Advanced analytics and reporting for promises."""
    
    def __init__(self, db_manager: DatabaseManager):
        """Initialize analytics with database manager."""
        self.db_manager = db_manager
        
    def generate_progress_timeline(self, promise_id: Optional[int] = None) -> Dict[str, Any]:
        """
        Generate comprehensive timeline data for promises.
        
        Args:
            promise_id: Optional specific promise ID to analyze
            
        Returns:
            Dict containing timeline data with dates, progress points, and trends
        """
        if promise_id:
            promises = [self.db_manager.get_promise(promise_id)]
            promises = [p for p in promises if p is not None]
        else:
            promises = self.db_manager.get_all_promises()
        
        timeline_data = {
            'promise_timelines': [],
            'aggregate_timeline': [],
            'trends': {
                'daily_avg_progress': 0,
                'weekly_momentum': 0,
                'completion_velocity': 0
            }
        }
        
        # Generate individual promise timelines
        for promise in promises:
            # Get progress updates for this promise
            updates = self.db_manager.get_progress_updates(promise.id)
            
            promise_timeline = {
                'promise_id': promise.id,
                'title': promise.text,
                'category': promise.category,
                'current_progress': promise.progress_percentage,
                'timeline_points': []
            }
            
            # Add creation date as first point
            promise_timeline['timeline_points'].append({
                'date': promise.created_at.isoformat() if promise.created_at else datetime.now().isoformat(),
                'progress': 0,
                'event': 'Promise Created',
                'description': f"Promise '{promise.text}' was created"
            })
            
            # Add progress updates
            for update in updates:
                # Estimate progress based on impact score and content
                estimated_progress = self._estimate_progress_from_update(update, promise.progress_percentage)
                
                promise_timeline['timeline_points'].append({
                    'date': update.date.isoformat() if update.date else datetime.now().isoformat(),
                    'progress': estimated_progress,
                    'event': 'Progress Update',
                    'description': update.update_text[:100] + '...' if len(update.update_text) > 100 else update.update_text,
                    'source_url': update.source_url,
                    'impact_score': update.impact_score
                })
            
            # Add current status
            promise_timeline['timeline_points'].append({
                'date': datetime.now().isoformat(),
                'progress': promise.progress_percentage,
                'event': f'Current Status: {promise.status.value}',
                'description': f"Current progress: {promise.progress_percentage}%"
            })
            
            timeline_data['promise_timelines'].append(promise_timeline)
        
        # Generate aggregate timeline
        timeline_data['aggregate_timeline'] = self._generate_aggregate_timeline(promises)
        
        # Calculate trends
        timeline_data['trends'] = self._calculate_timeline_trends(promises)
        
        return timeline_data
    
    def _estimate_progress_from_update(self, update: ProgressUpdate, current_progress: float) -> float:
        """Estimate progress percentage from an update based on impact score and timing."""
        # Base estimation on impact score
        if update.impact_score:
            # High impact updates suggest significant progress
            if update.impact_score >= 8:
                return min(current_progress + 20, 100)
            elif update.impact_score >= 6:
                return min(current_progress + 10, 100)
            elif update.impact_score >= 4:
                return min(current_progress + 5, 100)
            else:
                return min(current_progress + 2, 100)
        
        # Fallback: estimate based on keywords in update text
        progress_keywords = {
            'completed': 25, 'signed': 20, 'approved': 15, 'passed': 15,
            'implemented': 20, 'launched': 15, 'started': 10, 'began': 10,
            'progress': 5, 'working': 5, 'developing': 5
        }
        
        text_lower = update.update_text.lower()
        estimated_increase = 0
        
        for keyword, value in progress_keywords.items():
            if keyword in text_lower:
                estimated_increase = max(estimated_increase, value)
        
        return min(current_progress + estimated_increase, 100)
    
    def _generate_aggregate_timeline(self, promises: List[Promise]) -> List[Dict[str, Any]]:
        """Generate aggregate timeline showing overall progress trends."""
        if not promises:
            return []
        
        # Group promises by creation date
        creation_dates = defaultdict(list)
        for promise in promises:
            date_key = promise.created_at.date() if promise.created_at else datetime.now().date()
            creation_dates[date_key].append(promise)
        
        aggregate_points = []
        cumulative_promises = 0
        cumulative_progress = 0
        
        for date in sorted(creation_dates.keys()):
            daily_promises = creation_dates[date]
            cumulative_promises += len(daily_promises)
            
            # Calculate average progress for all promises up to this date
            all_promises_to_date = []
            for d in creation_dates.keys():
                if d <= date:
                    all_promises_to_date.extend(creation_dates[d])
            
            if all_promises_to_date:
                avg_progress = sum(p.progress_percentage for p in all_promises_to_date) / len(all_promises_to_date)
            else:
                avg_progress = 0
            
            aggregate_points.append({
                'date': date.isoformat(),
                'total_promises': cumulative_promises,
                'average_progress': round(avg_progress, 2),
                'new_promises_today': len(daily_promises),
                'completion_rate': len([p for p in all_promises_to_date if p.progress_percentage >= 100]) / len(all_promises_to_date) * 100
            })
        
        return aggregate_points
    
    def _calculate_timeline_trends(self, promises: List[Promise]) -> Dict[str, float]:
        """Calculate various trend metrics."""
        if not promises:
            return {'daily_avg_progress': 0, 'weekly_momentum': 0, 'completion_velocity': 0}
        
        # Simple trend calculations
        total_progress = sum(p.progress_percentage for p in promises)
        avg_progress = total_progress / len(promises)
        
        # Calculate completion velocity (promises completed per month)
        completed_promises = len([p for p in promises if p.progress_percentage >= 100])
        months_active = 12  # Assume 12 months for now
        completion_velocity = completed_promises / months_active
        
        return {
            'daily_avg_progress': round(avg_progress / 30, 2),  # Rough daily average
            'weekly_momentum': round(avg_progress / 4, 2),  # Rough weekly momentum
            'completion_velocity': round(completion_velocity, 2)
        }
    
    def generate_comparative_analysis(self) -> Dict[str, Any]:
        """
        Generate comparative analysis across different dimensions.
        
        Returns:
            Dict containing comparative metrics across categories, priorities, etc.
        """
        promises = self.db_manager.get_all_promises()
        
        if not promises:
            return {'error': 'No promises found for analysis'}
        
        analysis = {
            'category_comparison': self._analyze_by_category(promises),
            'priority_comparison': self._analyze_by_priority(promises),
            'status_distribution': self._analyze_by_status(promises),
            'progress_distribution': self._analyze_progress_distribution(promises),
            'summary_metrics': self._calculate_summary_metrics(promises)
        }
        
        return analysis
    
    def _analyze_by_category(self, promises: List[Promise]) -> Dict[str, Any]:
        """Analyze promises by category."""
        categories = defaultdict(list)
        
        for promise in promises:
            categories[promise.category].append(promise)
        
        category_analysis = {}
        
        for category, cat_promises in categories.items():
            if cat_promises:
                avg_progress = sum(p.progress_percentage for p in cat_promises) / len(cat_promises)
                completed_count = len([p for p in cat_promises if p.progress_percentage >= 100])
                
                category_analysis[category] = {
                    'total_promises': len(cat_promises),
                    'avg_progress': round(avg_progress, 2),
                    'completion_rate': round((completed_count / len(cat_promises)) * 100, 2),
                    'status_breakdown': self._get_status_breakdown(cat_promises),
                    'top_performing': sorted(cat_promises, key=lambda p: p.progress_percentage, reverse=True)[:3]
                }
        
        return category_analysis
    
    def _analyze_by_priority(self, promises: List[Promise]) -> Dict[str, Any]:
        """Analyze promises by priority level."""
        priorities = defaultdict(list)
        
        for promise in promises:
            priorities[promise.priority].append(promise)
        
        priority_analysis = {}
        
        for priority, pri_promises in priorities.items():
            if pri_promises:
                avg_progress = sum(p.progress_percentage for p in pri_promises) / len(pri_promises)
                completed_count = len([p for p in pri_promises if p.progress_percentage >= 100])
                
                priority_analysis[f'Priority_{priority}'] = {
                    'total_promises': len(pri_promises),
                    'avg_progress': round(avg_progress, 2),
                    'completion_rate': round((completed_count / len(pri_promises)) * 100, 2),
                    'status_breakdown': self._get_status_breakdown(pri_promises)
                }
        
        return priority_analysis
    
    def _analyze_by_status(self, promises: List[Promise]) -> Dict[str, Any]:
        """Analyze distribution by status."""
        status_counts = Counter(promise.status.value for promise in promises)
        total_promises = len(promises)
        
        status_analysis = {}
        for status, count in status_counts.items():
            percentage = (count / total_promises) * 100
            status_analysis[status] = {
                'count': count,
                'percentage': round(percentage, 2)
            }
        
        return status_analysis
    
    def _analyze_progress_distribution(self, promises: List[Promise]) -> Dict[str, Any]:
        """Analyze distribution by progress ranges."""
        ranges = {
            '0-25%': 0,
            '26-50%': 0,
            '51-75%': 0,
            '76-99%': 0,
            '100%': 0
        }
        
        for promise in promises:
            progress = promise.progress_percentage
            if progress == 100:
                ranges['100%'] += 1
            elif progress > 75:
                ranges['76-99%'] += 1
            elif progress > 50:
                ranges['51-75%'] += 1
            elif progress > 25:
                ranges['26-50%'] += 1
            else:
                ranges['0-25%'] += 1
        
        total = len(promises)
        return {
            range_name: {
                'count': count,
                'percentage': round((count / total) * 100, 2) if total > 0 else 0
            }
            for range_name, count in ranges.items()
        }
    
    def _calculate_summary_metrics(self, promises: List[Promise]) -> Dict[str, Any]:
        """Calculate overall summary metrics."""
        if not promises:
            return {}
        
        total_promises = len(promises)
        completed_promises = len([p for p in promises if p.progress_percentage >= 100])
        avg_progress = sum(p.progress_percentage for p in promises) / total_promises
        high_priority_promises = len([p for p in promises if p.priority >= 4])
        stalled_promises = len([p for p in promises if p.progress_percentage < 10 and p.status.value not in ['Fulfilled', 'Broken']])
        
        return {
            'total_promises': total_promises,
            'completion_rate': round((completed_promises / total_promises) * 100, 2),
            'average_progress': round(avg_progress, 2),
            'high_priority_count': high_priority_promises,
            'stalled_count': stalled_promises,
            'most_active_category': self._get_most_active_category(promises),
            'highest_performing_category': self._get_highest_performing_category(promises)
        }
    
    def _get_status_breakdown(self, promises: List[Promise]) -> Dict[str, int]:
        """Get status breakdown for a list of promises."""
        return dict(Counter(promise.status.value for promise in promises))
    
    def _get_most_active_category(self, promises: List[Promise]) -> str:
        """Get the category with the most promises."""
        categories = Counter(promise.category for promise in promises)
        return categories.most_common(1)[0][0] if categories else 'N/A'
    
    def _get_highest_performing_category(self, promises: List[Promise]) -> str:
        """Get the category with the highest average progress."""
        categories = defaultdict(list)
        
        for promise in promises:
            categories[promise.category].append(promise.progress_percentage)
        
        if not categories:
            return 'N/A'
        
        category_averages = {
            category: sum(progresses) / len(progresses)
            for category, progresses in categories.items()
        }
        
        return max(category_averages.items(), key=lambda x: x[1])[0]
    
    def generate_advanced_visualizations(self) -> Dict[str, Any]:
        """
        Generate data for advanced visualizations.
        
        Returns:
            Dict containing visualization-ready data for charts and graphs
        """
        promises = self.db_manager.get_all_promises()
        
        viz_data = {
            'progress_heatmap': self._generate_progress_heatmap(promises),
            'category_performance_radar': self._generate_category_radar_data(promises),
            'timeline_chart': self._generate_timeline_chart_data(promises),
            'priority_vs_progress_scatter': self._generate_priority_scatter_data(promises),
            'status_funnel': self._generate_status_funnel_data(promises)
        }
        
        return viz_data
    
    def _generate_progress_heatmap(self, promises: List[Promise]) -> Dict[str, Any]:
        """Generate data for a progress heatmap by category and time."""
        # Group by category and month
        heatmap_data = defaultdict(lambda: defaultdict(float))
        
        for promise in promises:
            category = promise.category
            # Use creation month as the time dimension
            month = promise.created_at.strftime('%Y-%m') if promise.created_at else datetime.now().strftime('%Y-%m')
            heatmap_data[category][month] = promise.progress_percentage
        
        return dict(heatmap_data)
    
    def _generate_category_radar_data(self, promises: List[Promise]) -> Dict[str, Any]:
        """Generate radar chart data for category performance."""
        categories = defaultdict(list)
        
        for promise in promises:
            categories[promise.category].append(promise)
        
        radar_data = {}
        
        for category, cat_promises in categories.items():
            if cat_promises:
                metrics = {
                    'avg_progress': sum(p.progress_percentage for p in cat_promises) / len(cat_promises),
                    'completion_rate': len([p for p in cat_promises if p.progress_percentage >= 100]) / len(cat_promises) * 100,
                    'avg_priority': sum(p.priority for p in cat_promises) / len(cat_promises),
                    'promise_count': len(cat_promises)
                }
                radar_data[category] = metrics
        
        return radar_data
    
    def _generate_timeline_chart_data(self, promises: List[Promise]) -> List[Dict[str, Any]]:
        """Generate timeline chart data."""
        timeline_points = []
        
        for promise in promises:
            timeline_points.append({
                'date': promise.created_at.isoformat() if promise.created_at else datetime.now().isoformat(),
                'progress': promise.progress_percentage,
                'category': promise.category,
                'priority': promise.priority,
                'title': promise.text
            })
        
        return sorted(timeline_points, key=lambda x: x['date'])
    
    def _generate_priority_scatter_data(self, promises: List[Promise]) -> List[Dict[str, Any]]:
        """Generate scatter plot data for priority vs progress."""
        return [
            {
                'priority': promise.priority,
                'progress': promise.progress_percentage,
                'category': promise.category,
                'title': promise.text,
                'status': promise.status.value
            }
            for promise in promises
        ]
    
    def _generate_status_funnel_data(self, promises: List[Promise]) -> Dict[str, int]:
        """Generate funnel data showing promise status progression."""
        status_counts = Counter(promise.status.value for promise in promises)
        
        # Define funnel order
        funnel_order = ['Proposed', 'In Progress', 'Stalled', 'Fulfilled', 'Broken']
        
        funnel_data = {}
        for status in funnel_order:
            funnel_data[status] = status_counts.get(status, 0)
        
        return funnel_data
    
    def export_comprehensive_report(self, format_type: str = 'json') -> str:
        """
        Export comprehensive analytics report in specified format.
        
        Args:
            format_type: 'json', 'csv', or 'html'
            
        Returns:
            Formatted report string
        """
        # Gather all analytics data
        timeline_data = self.generate_progress_timeline()
        comparative_data = self.generate_comparative_analysis()
        viz_data = self.generate_advanced_visualizations()
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'timeline_analysis': timeline_data,
            'comparative_analysis': comparative_data,
            'visualization_data': viz_data,
            'executive_summary': self.generate_executive_summary(),
            'recommendations': self.generate_recommendations()
        }
        
        if format_type.lower() == 'json':
            return json.dumps(report_data, indent=2, default=str)
        
        elif format_type.lower() == 'csv':
            return self._export_to_csv(report_data)
        
        elif format_type.lower() == 'html':
            return self._export_to_html(report_data)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_to_csv(self, report_data: Dict[str, Any]) -> str:
        """Export report data to CSV format."""
        output = StringIO()
        
        # Write summary metrics
        writer = csv.writer(output)
        writer.writerow(['Trump Promises Tracker - Analytics Report'])
        writer.writerow(['Generated:', report_data['generated_at']])
        writer.writerow([])
        
        # Executive summary
        writer.writerow(['Executive Summary'])
        if 'executive_summary' in report_data and report_data['executive_summary']:
            for key, value in report_data['executive_summary'].items():
                writer.writerow([key, value])
        writer.writerow([])
        
        # Category comparison
        if 'comparative_analysis' in report_data and 'category_comparison' in report_data['comparative_analysis']:
            writer.writerow(['Category Analysis'])
            writer.writerow(['Category', 'Total Promises', 'Avg Progress', 'Completion Rate'])
            
            for category, data in report_data['comparative_analysis']['category_comparison'].items():
                writer.writerow([
                    category,
                    data.get('total_promises', 0),
                    data.get('avg_progress', 0),
                    data.get('completion_rate', 0)
                ])
        
        return output.getvalue()
    
    def _export_to_html(self, report_data: Dict[str, Any]) -> str:
        """Export report data to HTML format."""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Trump Promises Tracker - Analytics Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 10px; }}
                .section {{ margin: 20px 0; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Trump Promises Tracker - Analytics Report</h1>
                <p>Generated: {report_data['generated_at']}</p>
            </div>
            
            <div class="section">
                <h2>Executive Summary</h2>
                {self._format_summary_html(report_data.get('executive_summary', {}))}
            </div>
            
            <div class="section">
                <h2>Category Performance</h2>
                {self._format_category_table_html(report_data.get('comparative_analysis', {}).get('category_comparison', {}))}
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _format_summary_html(self, summary: Dict[str, Any]) -> str:
        """Format executive summary as HTML."""
        if not summary:
            return "<p>No summary data available.</p>"
        
        html = "<ul>"
        for key, value in summary.items():
            html += f"<li><strong>{key}:</strong> {value}</li>"
        html += "</ul>"
        
        return html
    
    def _format_category_table_html(self, categories: Dict[str, Any]) -> str:
        """Format category data as HTML table."""
        if not categories:
            return "<p>No category data available.</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Total Promises</th>
                    <th>Avg Progress</th>
                    <th>Completion Rate</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for category, data in categories.items():
            html += f"""
                <tr>
                    <td>{category}</td>
                    <td>{data.get('total_promises', 0)}</td>
                    <td>{data.get('avg_progress', 0)}%</td>
                    <td>{data.get('completion_rate', 0)}%</td>
                </tr>
            """
        
        html += "</tbody></table>"
        return html
    
    def generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary of promise tracking."""
        promises = self.db_manager.get_all_promises()
        
        if not promises:
            return {'error': 'No promises available for analysis'}
        
        total_promises = len(promises)
        completed_promises = len([p for p in promises if p.progress_percentage >= 100])
        avg_progress = sum(p.progress_percentage for p in promises) / total_promises
        
        # Find most/least performing categories
        categories = defaultdict(list)
        for promise in promises:
            categories[promise.category].append(promise.progress_percentage)
        
        category_averages = {
            cat: sum(progresses) / len(progresses)
            for cat, progresses in categories.items()
        }
        
        best_category = max(category_averages.items(), key=lambda x: x[1]) if category_averages else ('N/A', 0)
        worst_category = min(category_averages.items(), key=lambda x: x[1]) if category_averages else ('N/A', 0)
        
        return {
            'total_promises': total_promises,
            'completion_rate': round((completed_promises / total_promises) * 100, 2),
            'average_progress': round(avg_progress, 2),
            'best_performing_category': f"{best_category[0]} ({best_category[1]:.1f}%)",
            'least_performing_category': f"{worst_category[0]} ({worst_category[1]:.1f}%)",
            'high_priority_incomplete': len([p for p in promises if p.priority >= 4 and p.progress_percentage < 100]),
            'stalled_promises': len([p for p in promises if p.progress_percentage < 10])
        }
    
    def generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on analytics."""
        promises = self.db_manager.get_all_promises()
        recommendations = []
        
        if not promises:
            return [{'priority': 'High', 'title': 'Data Collection', 'description': 'No promises found. Begin data collection.'}]
        
        # Analyze for recommendations
        avg_progress = sum(p.progress_percentage for p in promises) / len(promises)
        stalled_count = len([p for p in promises if p.progress_percentage < 10])
        high_priority_incomplete = len([p for p in promises if p.priority >= 4 and p.progress_percentage < 100])
        
        if avg_progress < 30:
            recommendations.append({
                'priority': 'High',
                'title': 'Accelerate Progress',
                'description': f'Overall progress is {avg_progress:.1f}%. Focus on quick wins and removing blockers.'
            })
        
        if stalled_count > 5:
            recommendations.append({
                'priority': 'Medium',
                'title': 'Address Stalled Promises',
                'description': f'{stalled_count} promises have minimal progress. Review and prioritize or archive.'
            })
        
        if high_priority_incomplete > 0:
            recommendations.append({
                'priority': 'High',
                'title': 'High Priority Focus',
                'description': f'{high_priority_incomplete} high-priority promises are incomplete. Allocate additional resources.'
            })
        
        # Category-specific recommendations
        categories = defaultdict(list)
        for promise in promises:
            categories[promise.category].append(promise.progress_percentage)
        
        for category, progresses in categories.items():
            avg_cat_progress = sum(progresses) / len(progresses)
            if avg_cat_progress < 20:
                recommendations.append({
                    'priority': 'Medium',
                    'title': f'Improve {category} Category',
                    'description': f'{category} category has low progress ({avg_cat_progress:.1f}%). Consider strategy review.'
                })
        
        return recommendations
    
    def generate_progress_timeline(self, promise_id: Optional[int] = None) -> Dict[str, Any]:
        """Generate timeline data for promise progress tracking."""
        
        if promise_id:
            # Single promise timeline
            promise = self.db_manager.get_promise(promise_id)
            if not promise:
                return {}
            
            progress_updates = self.db_manager.get_progress_updates(promise_id)
            
            timeline_data = {
                'promise_id': promise_id,
                'promise_text': promise.text,
                'category': promise.category,
                'current_progress': promise.progress_percentage,
                'timeline': []
            }
            
            for update in progress_updates:
                timeline_data['timeline'].append({
                    'date': update.date.isoformat(),
                    'progress': update.progress_percentage,
                    'status': update.status.value,
                    'notes': update.notes
                })
            
            return timeline_data
        
        else:
            # Overall progress timeline
            promises = self.db_manager.get_all_promises()
            
            # Group by month for overall trends
            monthly_progress = defaultdict(list)
            
            for promise in promises:
                updates = self.db_manager.get_progress_updates(promise.id)
                for update in updates:
                    month_key = update.date.strftime('%Y-%m')
                    monthly_progress[month_key].append(update.progress_percentage)
            
            # Calculate average progress per month
            timeline_data = {
                'overall_timeline': [],
                'total_promises': len(promises)
            }
            
            for month, progress_values in sorted(monthly_progress.items()):
                avg_progress = sum(progress_values) / len(progress_values)
                timeline_data['overall_timeline'].append({
                    'month': month,
                    'average_progress': round(avg_progress, 2),
                    'promise_count': len(progress_values)
                })
            
            return timeline_data
    

        
        promises = self.db_manager.get_all_promises()
        
        # Category comparison
        category_stats = defaultdict(lambda: {
            'count': 0,
            'avg_progress': 0,
            'fulfilled': 0,
            'in_progress': 0,
            'not_started': 0,
            'broken': 0
        })
        
        # Priority comparison
        priority_stats = defaultdict(lambda: {
            'count': 0,
            'avg_progress': 0,
            'avg_completion_time': 0
        })
        
        # Time-based analysis
        monthly_stats = defaultdict(lambda: {
            'promises_made': 0,
            'promises_completed': 0,
            'avg_progress': 0
        })
        
        for promise in promises:
            # Category analysis
            cat = promise.category
            category_stats[cat]['count'] += 1
            category_stats[cat]['avg_progress'] += promise.progress_percentage
            
            # Status counting
            if promise.status == PromiseStatus.FULFILLED:
                category_stats[cat]['fulfilled'] += 1
            elif promise.status == PromiseStatus.IN_PROGRESS:
                category_stats[cat]['in_progress'] += 1
            elif promise.status == PromiseStatus.NOT_STARTED:
                category_stats[cat]['not_started'] += 1
            elif promise.status == PromiseStatus.BROKEN:
                category_stats[cat]['broken'] += 1
            
            # Priority analysis
            priority_stats[promise.priority]['count'] += 1
            priority_stats[promise.priority]['avg_progress'] += promise.progress_percentage
            
            # Monthly analysis
            if promise.date_made:
                month_key = promise.date_made.strftime('%Y-%m')
                monthly_stats[month_key]['promises_made'] += 1
                if promise.status == PromiseStatus.FULFILLED:
                    monthly_stats[month_key]['promises_completed'] += 1
                monthly_stats[month_key]['avg_progress'] += promise.progress_percentage
        
        # Calculate averages
        for cat_data in category_stats.values():
            if cat_data['count'] > 0:
                cat_data['avg_progress'] = round(cat_data['avg_progress'] / cat_data['count'], 2)
        
        for priority_data in priority_stats.values():
            if priority_data['count'] > 0:
                priority_data['avg_progress'] = round(priority_data['avg_progress'] / priority_data['count'], 2)
        
        for month_data in monthly_stats.values():
            if month_data['promises_made'] > 0:
                month_data['avg_progress'] = round(month_data['avg_progress'] / month_data['promises_made'], 2)
        
        return {
            'category_comparison': dict(category_stats),
            'priority_comparison': dict(priority_stats),
            'monthly_trends': dict(monthly_stats),
            'summary': {
                'total_categories': len(category_stats),
                'most_active_category': max(category_stats.keys(), key=lambda k: category_stats[k]['count']),
                'highest_progress_category': max(category_stats.keys(), key=lambda k: category_stats[k]['avg_progress']),
                'total_months_tracked': len(monthly_stats)
            }
        }
    
    def generate_advanced_visualizations(self) -> Dict[str, Any]:
        """Generate data for advanced visualizations."""
        
        promises = self.db_manager.get_all_promises()
        
        # Progress distribution histogram
        progress_ranges = {
            '0-10%': 0, '11-25%': 0, '26-50%': 0, 
            '51-75%': 0, '76-90%': 0, '91-100%': 0
        }
        
        # Completion velocity (promises completed per month)
        completion_velocity = defaultdict(int)
        
        # Source reliability analysis
        source_reliability = defaultdict(list)
        
        for promise in promises:
            # Progress distribution
            progress = promise.progress_percentage
            if progress <= 10:
                progress_ranges['0-10%'] += 1
            elif progress <= 25:
                progress_ranges['11-25%'] += 1
            elif progress <= 50:
                progress_ranges['26-50%'] += 1
            elif progress <= 75:
                progress_ranges['51-75%'] += 1
            elif progress <= 90:
                progress_ranges['76-90%'] += 1
            else:
                progress_ranges['91-100%'] += 1
            
            # Completion velocity
            if promise.status == PromiseStatus.FULFILLED and promise.date_updated:
                month_key = promise.date_updated.strftime('%Y-%m')
                completion_velocity[month_key] += 1
            
            # Source reliability
            for source in promise.sources:
                source_reliability[source.source_type.value].append(source.reliability_score)
        
        # Calculate average source reliability
        avg_source_reliability = {}
        for source_type, scores in source_reliability.items():
            if scores:
                avg_source_reliability[source_type] = round(sum(scores) / len(scores), 3)
        
        return {
            'progress_distribution': progress_ranges,
            'completion_velocity': dict(completion_velocity),
            'source_reliability': avg_source_reliability,
            'visualization_data': {
                'total_promises': len(promises),
                'data_quality_score': self._calculate_data_quality_score(promises),
                'trend_direction': self._calculate_trend_direction(promises)
            }
        }
    
    def export_comprehensive_report(self, format_type: str = 'json') -> str:
        """Export comprehensive analytics report in specified format."""
        
        report_data = {
            'generated_at': datetime.now().isoformat(),
            'summary': self._generate_executive_summary(),
            'progress_timeline': self.generate_progress_timeline(),
            'comparative_analysis': self.generate_comparative_analysis(),
            'visualizations': self.generate_advanced_visualizations(),
            'recommendations': self._generate_recommendations()
        }
        
        if format_type.lower() == 'json':
            return json.dumps(report_data, indent=2)
        
        elif format_type.lower() == 'csv':
            return self._export_to_csv(report_data)
        
        elif format_type.lower() == 'html':
            return self._export_to_html(report_data)
        
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _generate_executive_summary(self) -> Dict[str, Any]:
        """Generate executive summary of promise tracking."""
        
        promises = self.db_manager.get_all_promises()
        
        total_promises = len(promises)
        fulfilled_count = sum(1 for p in promises if p.status == PromiseStatus.FULFILLED)
        in_progress_count = sum(1 for p in promises if p.status == PromiseStatus.IN_PROGRESS)
        broken_count = sum(1 for p in promises if p.status == PromiseStatus.BROKEN)
        
        avg_progress = sum(p.progress_percentage for p in promises) / total_promises if promises else 0
        
        # Most and least active categories
        category_counts = Counter(p.category for p in promises)
        most_active_category = category_counts.most_common(1)[0] if category_counts else ("None", 0)
        
        return {
            'total_promises': total_promises,
            'fulfillment_rate': round((fulfilled_count / total_promises) * 100, 2) if total_promises else 0,
            'avg_progress': round(avg_progress, 2),
            'promises_fulfilled': fulfilled_count,
            'promises_in_progress': in_progress_count,
            'promises_broken': broken_count,
            'most_active_category': most_active_category[0],
            'category_promise_count': most_active_category[1],
            'data_completeness': self._calculate_data_completeness(promises)
        }
    
    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate actionable recommendations based on data analysis."""
        
        promises = self.db_manager.get_all_promises()
        comparative_data = self.generate_comparative_analysis()
        
        recommendations = []
        
        # Low progress promises
        low_progress_promises = [p for p in promises if p.progress_percentage < 25 and p.status != PromiseStatus.BROKEN]
        if len(low_progress_promises) > 10:
            recommendations.append({
                'type': 'priority',
                'title': 'Focus on Stalled Promises',
                'description': f'{len(low_progress_promises)} promises have less than 25% progress. Consider prioritizing these.',
                'action': 'Review and update status of low-progress promises'
            })
        
        # Category imbalance
        category_stats = comparative_data['category_comparison']
        categories_with_low_progress = [cat for cat, stats in category_stats.items() if stats['avg_progress'] < 30]
        if categories_with_low_progress:
            recommendations.append({
                'type': 'category',
                'title': 'Category Performance Gap',
                'description': f'Categories {", ".join(categories_with_low_progress)} have below-average progress.',
                'action': 'Analyze barriers and allocate more resources to underperforming categories'
            })
        
        # Source reliability
        visualization_data = self.generate_advanced_visualizations()
        low_reliability_sources = [source for source, score in visualization_data['source_reliability'].items() if score < 0.7]
        if low_reliability_sources:
            recommendations.append({
                'type': 'data_quality',
                'title': 'Improve Source Quality',
                'description': f'Source types {", ".join(low_reliability_sources)} have reliability scores below 70%.',
                'action': 'Verify and update sources with low reliability scores'
            })
        
        return recommendations
    
    def _calculate_data_quality_score(self, promises: List[Promise]) -> float:
        """Calculate overall data quality score."""
        
        if not promises:
            return 0.0
        
        quality_factors = []
        
        for promise in promises:
            # Check for completeness
            completeness_score = 0
            if promise.text.strip():
                completeness_score += 0.3
            if promise.category and promise.category != "Other":
                completeness_score += 0.2
            if promise.sources:
                completeness_score += 0.3
            if promise.date_made:
                completeness_score += 0.1
            if promise.notes.strip():
                completeness_score += 0.1
            
            quality_factors.append(completeness_score)
        
        return round(sum(quality_factors) / len(quality_factors), 3)
    
    def _calculate_trend_direction(self, promises: List[Promise]) -> str:
        """Calculate overall trend direction."""
        
        if len(promises) < 2:
            return "insufficient_data"
        
        # Simple trend calculation based on recent vs older promises
        sorted_promises = sorted(promises, key=lambda p: p.date_updated or datetime.min)
        
        recent_half = sorted_promises[len(sorted_promises)//2:]
        older_half = sorted_promises[:len(sorted_promises)//2]
        
        recent_avg = sum(p.progress_percentage for p in recent_half) / len(recent_half)
        older_avg = sum(p.progress_percentage for p in older_half) / len(older_half)
        
        if recent_avg > older_avg + 5:
            return "improving"
        elif recent_avg < older_avg - 5:
            return "declining"
        else:
            return "stable"
    
    def _calculate_data_completeness(self, promises: List[Promise]) -> float:
        """Calculate data completeness percentage."""
        
        if not promises:
            return 0.0
        
        total_fields = len(promises) * 5  # text, category, sources, date_made, notes
        completed_fields = 0
        
        for promise in promises:
            if promise.text.strip():
                completed_fields += 1
            if promise.category and promise.category != "Other":
                completed_fields += 1
            if promise.sources:
                completed_fields += 1
            if promise.date_made:
                completed_fields += 1
            if promise.notes.strip():
                completed_fields += 1
        
        return round((completed_fields / total_fields) * 100, 2)
    
    def _export_to_csv(self, report_data: Dict[str, Any]) -> str:
        """Export report data to CSV format."""
        
        output = io.StringIO()
        
        # Summary data
        writer = csv.writer(output)
        writer.writerow(['Metric', 'Value'])
        
        summary = report_data['summary']
        for key, value in summary.items():
            writer.writerow([key.replace('_', ' ').title(), value])
        
        # Category comparison
        writer.writerow([])
        writer.writerow(['Category Analysis'])
        writer.writerow(['Category', 'Count', 'Avg Progress', 'Fulfilled', 'In Progress', 'Not Started', 'Broken'])
        
        category_data = report_data['comparative_analysis']['category_comparison']
        for category, stats in category_data.items():
            writer.writerow([
                category, stats['count'], stats['avg_progress'],
                stats['fulfilled'], stats['in_progress'], 
                stats['not_started'], stats['broken']
            ])
        
        return output.getvalue()
    
    def _export_to_html(self, report_data: Dict[str, Any]) -> str:
        """Export report data to HTML format."""
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Trump Promises Tracker - Analytics Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .summary {{ background: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background: white; border-radius: 3px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Trump Promises Tracker - Analytics Report</h1>
            <p>Generated: {report_data['generated_at']}</p>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="metric"><strong>Total Promises:</strong> {report_data['summary']['total_promises']}</div>
                <div class="metric"><strong>Fulfillment Rate:</strong> {report_data['summary']['fulfillment_rate']}%</div>
                <div class="metric"><strong>Average Progress:</strong> {report_data['summary']['avg_progress']}%</div>
                <div class="metric"><strong>Data Completeness:</strong> {report_data['summary']['data_completeness']}%</div>
            </div>
            
            <h2>Recommendations</h2>
            <ul>
        """
        
        for rec in report_data['recommendations']:
            html_template += f"<li><strong>{rec['title']}:</strong> {rec['description']} <em>Action: {rec['action']}</em></li>"
        
        html_template += """
            </ul>
        </body>
        </html>
        """
        
        return html_template
