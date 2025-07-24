"""
Web interface routes for link validation monitoring
"""

from flask import render_template, jsonify, request
from datetime import datetime
import json
import os

def add_link_validation_routes(app, db):
    """Add link validation routes to the Flask app."""
    
    @app.route('/admin/link-validation')
    def link_validation_dashboard():
        """Display link validation dashboard."""
        # Load latest validation results
        results = load_latest_validation_results()
        
        return render_template('admin/link_validation.html', 
                             validation_results=results,
                             page_title="Link Validation Dashboard")
    
    @app.route('/api/link-validation/status')
    def link_validation_status():
        """API endpoint for link validation status."""
        try:
            from link_validation_integration import get_link_validation_status
            status = get_link_validation_status()
            return jsonify(status)
        except ImportError:
            return jsonify({
                'status': 'unavailable',
                'message': 'Link validation service not running'
            })
    
    @app.route('/api/link-validation/run', methods=['POST'])
    def run_link_validation():
        """Manually trigger link validation."""
        try:
            from link_validation_integration import run_validation_protocol
            results = run_validation_protocol()
            return jsonify({
                'status': 'success',
                'message': 'Validation completed',
                'results': results['summary']
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Validation failed: {str(e)}'
            })
    
    @app.route('/api/sources/validate/<int:source_id>')
    def validate_single_source(source_id):
        """Validate a single source."""
        try:
            from link_validation_protocol import LinkValidator
            
            # Get source from database
            source = db.get_source(source_id)
            if not source:
                return jsonify({'error': 'Source not found'}), 404
            
            # Validate the source
            validator = LinkValidator()
            is_valid, status_code, error_msg = validator.validate_url(source.url)
            
            return jsonify({
                'source_id': source_id,
                'url': source.url,
                'is_valid': is_valid,
                'status_code': status_code,
                'error_message': error_msg if not is_valid else None,
                'validated_at': datetime.now().isoformat()
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def load_latest_validation_results():
    """Load the latest validation results from file."""
    results_file = "latest_validation_results.json"
    
    if not os.path.exists(results_file):
        return {
            'status': 'no_data',
            'message': 'No validation results available',
            'summary': {
                'valid_count': 0,
                'invalid_count': 0,
                'placeholder_count': 0,
                'validation_date': None
            }
        }
    
    try:
        with open(results_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error loading results: {str(e)}',
            'summary': {
                'valid_count': 0,
                'invalid_count': 0,
                'placeholder_count': 0,
                'validation_date': None
            }
        }
