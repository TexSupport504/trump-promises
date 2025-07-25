"""
Enhanced analytics routes for the Trump Promises Tracker.
"""

from flask import render_template, jsonify, request, make_response, send_file
from datetime import datetime
import json
import io

from ..advanced_analytics import AdvancedAnalytics


def add_analytics_routes(app, db_manager):
    """Add enhanced analytics routes to the Flask app."""
    
    analytics = AdvancedAnalytics(db_manager)
    
    @app.route('/analytics/advanced')
    def advanced_analytics():
        """Enhanced analytics dashboard."""
        
        # Get comparative analysis data
        comparative_data = analytics.generate_comparative_analysis()
        
        # Get visualization data  
        viz_data = analytics.generate_advanced_visualizations()
        
        # Get timeline data for overall progress
        timeline_data = analytics.generate_progress_timeline()
        
        return render_template('analytics/advanced.html',
                             comparative_data=comparative_data,
                             visualization_data=viz_data,
                             timeline_data=timeline_data,
                             page_title="Advanced Analytics")
    
    @app.route('/api/analytics/progress-timeline')
    def api_progress_timeline():
        """API endpoint for progress timeline data."""
        promise_id = request.args.get('promise_id', type=int)
        
        timeline_data = analytics.generate_progress_timeline(promise_id)
        return jsonify(timeline_data)
    
    @app.route('/api/analytics/comparative')
    def api_comparative_analysis():
        """API endpoint for comparative analysis data."""
        
        comparative_data = analytics.generate_comparative_analysis()
        return jsonify(comparative_data)
    
    @app.route('/api/analytics/visualizations')
    def api_visualizations():
        """API endpoint for visualization data."""
        
        viz_data = analytics.generate_advanced_visualizations()
        return jsonify(viz_data)
    
    @app.route('/analytics/export')
    def export_analytics():
        """Export comprehensive analytics report."""
        
        format_type = request.args.get('format', 'json').lower()
        
        try:
            report_data = analytics.export_comprehensive_report(format_type)
            
            if format_type == 'json':
                response = make_response(report_data)
                response.headers['Content-Type'] = 'application/json'
                response.headers['Content-Disposition'] = f'attachment; filename=promises_report_{datetime.now().strftime("%Y%m%d")}.json'
                
            elif format_type == 'csv':
                response = make_response(report_data)
                response.headers['Content-Type'] = 'text/csv'
                response.headers['Content-Disposition'] = f'attachment; filename=promises_report_{datetime.now().strftime("%Y%m%d")}.csv'
                
            elif format_type == 'html':
                response = make_response(report_data)
                response.headers['Content-Type'] = 'text/html'
                response.headers['Content-Disposition'] = f'attachment; filename=promises_report_{datetime.now().strftime("%Y%m%d")}.html'
                
            else:
                return jsonify({'error': 'Unsupported format'}), 400
            
            return response
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/analytics/recommendations')
    def analytics_recommendations():
        """Show analytics-based recommendations."""
        
        # Get executive summary
        summary = analytics.generate_executive_summary()
        
        # Get recommendations
        recommendations = analytics.generate_recommendations()
        
        # Get comparative data for context
        comparative_data = analytics.generate_comparative_analysis()
        
        return render_template('analytics/recommendations.html',
                             summary=summary,
                             recommendations=recommendations,
                             comparative_data=comparative_data,
                             page_title="Analytics Recommendations")
    
    @app.route('/analytics/category/<category_name>')
    def category_deep_dive(category_name):
        """Deep dive analytics for a specific category."""
        
        # Get all promises for this category
        all_promises = db_manager.get_all_promises()
        category_promises = [p for p in all_promises if p.category == category_name]
        
        if not category_promises:
            return render_template('404.html'), 404
        
        # Calculate category-specific metrics
        total_promises = len(category_promises)
        avg_progress = sum(p.progress_percentage for p in category_promises) / total_promises
        fulfilled_count = sum(1 for p in category_promises if p.status.value == 'Fulfilled')
        
        # Status distribution
        status_distribution = {}
        for promise in category_promises:
            status = promise.status.value
            status_distribution[status] = status_distribution.get(status, 0) + 1
        
        # Progress distribution
        progress_ranges = {
            '0-25%': sum(1 for p in category_promises if p.progress_percentage <= 25),
            '26-50%': sum(1 for p in category_promises if 25 < p.progress_percentage <= 50),
            '51-75%': sum(1 for p in category_promises if 50 < p.progress_percentage <= 75),
            '76-100%': sum(1 for p in category_promises if p.progress_percentage > 75)
        }
        
        # Top performing promises in category
        top_promises = sorted(category_promises, key=lambda p: p.progress_percentage, reverse=True)[:5]
        
        category_data = {
            'name': category_name,
            'total_promises': total_promises,
            'avg_progress': round(avg_progress, 2),
            'fulfillment_rate': round((fulfilled_count / total_promises) * 100, 2),
            'status_distribution': status_distribution,
            'progress_distribution': progress_ranges,
            'top_promises': top_promises
        }
        
        return render_template('analytics/category_deep_dive.html',
                             category_data=category_data,
                             page_title=f"{category_name} Analytics")
    
    @app.route('/api/analytics/progress-tracking')
    def api_progress_tracking():
        """API for real-time progress tracking data."""
        
        promises = db_manager.get_all_promises()
        
        # Calculate progress velocity (change over time)
        progress_tracking = {
            'total_promises': len(promises),
            'current_avg_progress': sum(p.progress_percentage for p in promises) / len(promises) if promises else 0,
            'completion_rate': {
                'daily': 0,  # Would need more sophisticated tracking
                'weekly': 0,
                'monthly': 0
            },
            'stalled_promises': len([p for p in promises if p.progress_percentage < 10 and p.status.value != 'Broken']),
            'high_priority_incomplete': len([p for p in promises if p.priority >= 4 and p.progress_percentage < 100])
        }
        
        return jsonify(progress_tracking)
