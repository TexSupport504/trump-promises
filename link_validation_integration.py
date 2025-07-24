"""
Integration module for the link validation protocol with the main application.
"""

import threading
import os
import sys

# Add the project root to sys.path so we can import modules
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def start_link_validation_service():
    """Start the background link validation service."""
    try:
        from link_scheduler import LinkValidationScheduler
        
        # Create and start the scheduler
        scheduler = LinkValidationScheduler()
        
        # Start the scheduler in a background thread
        scheduler_thread = scheduler.start_scheduler()
        
        print("✓ Link validation service started successfully")
        return True
        
    except ImportError as e:
        print(f"⚠ Warning: Could not start link validation service: {e}")
        return False
    except Exception as e:
        print(f"⚠ Error starting link validation service: {e}")
        return False

def run_validation_protocol():
    """Run the validation protocol manually."""
    try:
        from link_validation_protocol import LinkValidator
        from app.database import DatabaseManager
        
        # Initialize components
        db = DatabaseManager()
        validator = LinkValidator()
        
        # Get all sources from database
        promises = db.get_all_promises()
        all_sources = []
        
        for promise in promises:
            for source in promise.sources:
                all_sources.append({
                    'id': source.id,
                    'promise_id': promise.id,
                    'title': source.title,
                    'url': source.url,
                    'source_type': source.source_type.value if source.source_type else 'unknown'
                })
        
        # Run validation
        print(f"Validating {len(all_sources)} sources...")
        
        valid_count = 0
        invalid_count = 0
        placeholder_count = 0
        details = []
        
        for source in all_sources:
            is_valid, status_code, error_msg = validator.validate_url(source['url'])
            is_placeholder = validator.is_placeholder_url(source['url'])
            
            if is_placeholder:
                placeholder_count += 1
            elif is_valid:
                valid_count += 1
            else:
                invalid_count += 1
            
            details.append({
                'source_id': source['id'],
                'promise_id': source['promise_id'],
                'source_title': source['title'],
                'url': source['url'],
                'is_valid': is_valid,
                'is_placeholder': is_placeholder,
                'status_code': status_code,
                'error_message': error_msg
            })
        
        # Generate results
        from datetime import datetime
        
        results = {
            'status': 'success',
            'summary': {
                'valid_count': valid_count,
                'invalid_count': invalid_count,
                'placeholder_count': placeholder_count,
                'total_count': len(all_sources),
                'validation_date': datetime.now().isoformat()
            },
            'details': details
        }
        
        # Save results to file for web interface
        import json
        with open('latest_validation_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"✓ Validation completed: {valid_count} valid, {invalid_count} invalid, {placeholder_count} placeholders")
        return results
        
    except Exception as e:
        error_result = {
            'status': 'error',
            'message': str(e),
            'summary': {
                'valid_count': 0,
                'invalid_count': 0,
                'placeholder_count': 0,
                'total_count': 0,
                'validation_date': None
            },
            'details': []
        }
        
        print(f"✗ Validation failed: {e}")
        return error_result

def get_link_validation_status():
    """Get the current status of the link validation system."""
    try:
        import json
        
        # Check if results file exists
        if os.path.exists('latest_validation_results.json'):
            with open('latest_validation_results.json', 'r') as f:
                results = json.load(f)
            
            return {
                'status': 'available',
                'last_run': results['summary']['validation_date'],
                'summary': results['summary']
            }
        else:
            return {
                'status': 'no_data',
                'message': 'No validation results available'
            }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error reading validation status: {str(e)}'
        }

if __name__ == '__main__':
    # Test the validation protocol
    print("Testing link validation protocol...")
    results = run_validation_protocol()
    print(f"Results: {results['summary']}")
