"""
Flask web routes for the Trump Promises Tracker.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
from typing import Dict, Any, List

from ..database import DatabaseManager
from ..models import Promise, Source, PromiseStatus, SourceType
from ..analyzer import PromiseAnalyzer
from config import Config
from .link_validation_routes import add_link_validation_routes
from .analytics_routes import add_analytics_routes


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db_manager = DatabaseManager()
    analyzer = PromiseAnalyzer(db_manager)
    
    @app.route('/')
    def index():
        """Home page with dashboard."""
        # Get sorting parameters for recent promises section
        sort_by = request.args.get('sort_by', 'progress')  # Default sort by progress for dashboard
        sort_order = request.args.get('sort_order', 'desc')  # Default descending
        
        analytics = analyzer.generate_analytics_report()
        
        # Get all promises and apply sorting
        all_promises = db_manager.get_all_promises()
        
        # Apply sorting to all promises
        if sort_by == 'progress':
            all_promises.sort(key=lambda p: p.progress_percentage, reverse=(sort_order == 'desc'))
        elif sort_by == 'priority':
            all_promises.sort(key=lambda p: p.priority, reverse=(sort_order == 'desc'))
        elif sort_by == 'category':
            all_promises.sort(key=lambda p: p.category, reverse=(sort_order == 'desc'))
        elif sort_by == 'status':
            all_promises.sort(key=lambda p: p.status.value, reverse=(sort_order == 'desc'))
        elif sort_by == 'created_at':
            all_promises.sort(key=lambda p: p.created_at or '', reverse=(sort_order == 'desc'))
        else:
            # Default to progress if invalid sort_by
            all_promises.sort(key=lambda p: p.progress_percentage, reverse=(sort_order == 'desc'))
        
        # Get top 10 for dashboard display
        recent_promises = all_promises[:10]
        
        return render_template('index.html', 
                             analytics=analytics,
                             recent_promises=recent_promises,
                             current_sort_by=sort_by,
                             current_sort_order=sort_order)
    
    @app.route('/promises')
    def promises():
        """List all promises with filtering and sorting options."""
        category = request.args.get('category')
        status = request.args.get('status')
        sort_by = request.args.get('sort_by', 'created_at')  # Default sort by creation date
        sort_order = request.args.get('sort_order', 'desc')  # Default descending
        page = int(request.args.get('page', 1))
        per_page = 20
        
        # Convert status string to enum if provided
        status_filter = None
        if status:
            try:
                status_filter = PromiseStatus(status)
            except ValueError:
                status_filter = None
        
        # Get filtered promises
        all_promises = db_manager.get_all_promises(category=category, status=status_filter)
        
        # Apply sorting
        if sort_by == 'progress':
            all_promises.sort(key=lambda p: p.progress_percentage, reverse=(sort_order == 'desc'))
        elif sort_by == 'priority':
            all_promises.sort(key=lambda p: p.priority, reverse=(sort_order == 'desc'))
        elif sort_by == 'category':
            all_promises.sort(key=lambda p: p.category, reverse=(sort_order == 'desc'))
        elif sort_by == 'status':
            all_promises.sort(key=lambda p: p.status.value, reverse=(sort_order == 'desc'))
        elif sort_by == 'created_at':
            all_promises.sort(key=lambda p: p.created_at or '', reverse=(sort_order == 'desc'))
        else:
            # Default to creation date if invalid sort_by
            all_promises.sort(key=lambda p: p.created_at or '', reverse=(sort_order == 'desc'))
        
        # Simple pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        promises_page = all_promises[start_idx:end_idx]
        
        # Pagination info
        total_pages = (len(all_promises) + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        return render_template('promises.html',
                             promises=promises_page,
                             categories=Config.PROMISE_CATEGORIES,
                             statuses=[s.value for s in PromiseStatus],
                             current_category=category,
                             current_status=status,
                             current_sort_by=sort_by,
                             current_sort_order=sort_order,
                             page=page,
                             total_pages=total_pages,
                             has_prev=has_prev,
                             has_next=has_next)
    
    @app.route('/promise/<int:promise_id>')
    def promise_detail(promise_id: int):
        """Show detailed view of a specific promise."""
        promise = db_manager.get_promise(promise_id)
        if not promise:
            flash('Promise not found.', 'error')
            return redirect(url_for('promises'))
        
        # Get progress updates
        progress_updates = db_manager.get_progress_updates(promise_id)
        
        # Get similar promises
        similar_promises = analyzer.find_similar_promises(promise, threshold=0.2)[:5]
        
        # Analyze promise complexity
        complexity_analysis = analyzer.analyze_promise_complexity(promise)
        
        return render_template('promise_detail.html',
                             promise=promise,
                             progress_updates=progress_updates,
                             similar_promises=similar_promises,
                             complexity=complexity_analysis)
    
    @app.route('/analytics')
    def analytics():
        """Analytics dashboard."""
        # Get analytics data
        analytics_data = db_manager.get_analytics_data()
        trends = analyzer.analyze_promise_trends()
        
        # Get all promises for additional analysis
        all_promises = db_manager.get_all_promises()
        recommendations = analyzer.generate_priority_recommendations(all_promises)[:10]
        
        # Get recent promises (last 10)
        recent_promises = sorted(all_promises, key=lambda p: p.date_updated or p.date_made, reverse=True)[:10]
        
        # Calculate priority distribution
        priority_data = {}
        for i in range(1, 6):
            priority_data[f'Priority {i}'] = sum(1 for p in all_promises if p.priority == i)
        
        # Calculate progress distribution
        progress_data = {
            '0%': sum(1 for p in all_promises if p.progress_percentage == 0),
            '1-25%': sum(1 for p in all_promises if 0 < p.progress_percentage <= 25),
            '26-50%': sum(1 for p in all_promises if 25 < p.progress_percentage <= 50),
            '51-75%': sum(1 for p in all_promises if 50 < p.progress_percentage <= 75),
            '76-99%': sum(1 for p in all_promises if 75 < p.progress_percentage < 100),
            '100%': sum(1 for p in all_promises if p.progress_percentage == 100)
        }
        
        # Count high priority promises
        high_priority_count = sum(1 for p in all_promises if p.priority == 5)
        
        return render_template('analytics.html',
                             analytics_data=analytics_data,
                             trends=trends,
                             recommendations=recommendations,
                             recent_promises=recent_promises,
                             priority_data=priority_data,
                             progress_data=progress_data,
                             high_priority_count=high_priority_count)
    
    @app.route('/add_promise', methods=['GET', 'POST'])
    def add_promise():
        """Add a new promise."""
        if request.method == 'POST':
            text = request.form.get('text', '').strip()
            category = request.form.get('category', 'Other')
            priority = int(request.form.get('priority', 3))
            source_title = request.form.get('source_title', '').strip()
            source_url = request.form.get('source_url', '').strip()
            notes = request.form.get('notes', '').strip()
            
            if not text:
                flash('Promise text is required.', 'error')
                return render_template('add_promise.html', categories=Config.PROMISE_CATEGORIES)
            
            # Create source if provided
            sources = []
            if source_title or source_url:
                sources.append(Source(
                    title=source_title or "Manual Entry",
                    url=source_url if source_url else None,
                    source_type=SourceType.OTHER,
                    date=datetime.now(),
                    description="Added via web interface"
                ))
            
            # Create promise
            promise = Promise(
                text=text,
                category=category,
                priority=priority,
                date_made=datetime.now(),
                sources=sources,
                notes=notes
            )
            
            try:
                promise_id = db_manager.add_promise(promise)
                flash(f'Promise added successfully with ID: {promise_id}', 'success')
                return redirect(url_for('promise_detail', promise_id=promise_id))
            except Exception as e:
                flash(f'Error adding promise: {str(e)}', 'error')
        
        return render_template('add_promise.html', categories=Config.PROMISE_CATEGORIES)
    
    @app.route('/api/promises')
    def api_promises():
        """API endpoint to get promises as JSON."""
        category = request.args.get('category')
        status = request.args.get('status')
        
        status_filter = None
        if status:
            try:
                status_filter = PromiseStatus(status)
            except ValueError:
                pass
        
        promises = db_manager.get_all_promises(category=category, status=status_filter)
        return jsonify([promise.to_dict() for promise in promises])
    
    @app.route('/api/analytics')
    def api_analytics():
        """API endpoint to get analytics data as JSON."""
        analytics_data = analyzer.generate_analytics_report()
        return jsonify(analytics_data.to_dict())
    
    @app.route('/api/promise/<int:promise_id>/update_status', methods=['POST'])
    def api_update_status(promise_id: int):
        """API endpoint to update promise status."""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if not new_status:
            return jsonify({'error': 'Status is required'}), 400
        
        try:
            status_enum = PromiseStatus(new_status)
        except ValueError:
            return jsonify({'error': 'Invalid status'}), 400
        
        promise = db_manager.get_promise(promise_id)
        if not promise:
            return jsonify({'error': 'Promise not found'}), 404
        
        promise.update_status(status_enum, notes)
        
        if db_manager.update_promise(promise):
            return jsonify({'success': True, 'message': 'Status updated successfully'})
        else:
            return jsonify({'error': 'Failed to update status'}), 500
    
    @app.route('/api/promise/<int:promise_id>/update_progress', methods=['POST'])
    def api_update_progress(promise_id: int):
        """API endpoint to update promise progress."""
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        progress = data.get('progress')
        notes = data.get('notes', '')
        
        if progress is None:
            return jsonify({'error': 'Progress is required'}), 400
        
        try:
            progress = float(progress)
            if not 0 <= progress <= 100:
                return jsonify({'error': 'Progress must be between 0 and 100'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid progress value'}), 400
        
        promise = db_manager.get_promise(promise_id)
        if not promise:
            return jsonify({'error': 'Promise not found'}), 404
        
        old_progress = promise.progress_percentage
        promise.progress_percentage = progress
        promise.date_updated = datetime.now()
        
        if notes:
            promise.notes += f"\n[{datetime.now().strftime('%Y-%m-%d')}] Progress updated from {old_progress}% to {progress}%: {notes}"
        
        if db_manager.update_promise(promise):
            return jsonify({'success': True, 'message': 'Progress updated successfully'})
        else:
            return jsonify({'error': 'Failed to update progress'}), 500
    
    @app.route('/search')
    def search():
        """Search promises."""
        query = request.args.get('q', '').strip()
        if not query:
            return render_template('search.html', promises=[], query='')
        
        # Simple text search (could be improved with full-text search)
        all_promises = db_manager.get_all_promises()
        matching_promises = [
            promise for promise in all_promises
            if query.lower() in promise.text.lower() or 
               query.lower() in promise.category.lower() or
               any(query.lower() in tag.lower() for tag in promise.tags)
        ]
        
        return render_template('search.html', promises=matching_promises, query=query)
    
    @app.route('/categories')
    def categories():
        """Show promises grouped by category."""
        analytics_data = db_manager.get_analytics_data()
        category_data = []
        
        for category, count in analytics_data['promises_by_category'].items():
            category_promises = db_manager.get_all_promises(category=category)
            category_data.append({
                'name': category,
                'count': count,
                'promises': category_promises[:5]  # Show first 5 promises
            })
        
        # Sort by count
        category_data.sort(key=lambda x: x['count'], reverse=True)
        
        return render_template('categories.html', categories=category_data)
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        return render_template('500.html'), 500
    
    # Add link validation routes
    add_link_validation_routes(app, db_manager)
    
    # Add analytics routes
    add_analytics_routes(app, db_manager)
    
    return app
