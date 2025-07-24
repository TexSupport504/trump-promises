"""
Automated Link Validation Scheduler
Runs the link validation protocol on a schedule and integrates with the web application.
"""

import schedule
import time
import threading
from datetime import datetime, timedelta
import json
import os

# Import our validation protocol
from link_validation_protocol import LinkValidator, run_validation_protocol

class LinkValidationScheduler:
    """Schedules and manages automated link validation."""
    
    def __init__(self):
        self.validator = LinkValidator()
        self.last_validation = None
        self.validation_results = None
        self.is_running = False
        
    def run_scheduled_validation(self):
        """Run validation and store results."""
        print(f"🕐 {datetime.now().strftime('%H:%M:%S')} - Running scheduled link validation...")
        
        try:
            self.validation_results = run_validation_protocol()
            self.last_validation = datetime.now()
            
            # Save results to JSON for web interface
            results_file = "latest_validation_results.json"
            with open(results_file, 'w') as f:
                # Convert datetime objects to strings for JSON serialization
                serializable_results = self._make_json_serializable(self.validation_results)
                json.dump(serializable_results, f, indent=2)
            
            print("✅ Validation completed and results saved")
            
        except Exception as e:
            print(f"❌ Validation failed: {e}")
    
    def _make_json_serializable(self, data):
        """Convert complex objects to JSON-serializable format."""
        if isinstance(data, dict):
            return {k: self._make_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_json_serializable(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        else:
            return data
    
    def start_scheduler(self):
        """Start the validation scheduler."""
        if self.is_running:
            print("⚠️ Scheduler is already running")
            return
        
        self.is_running = True
        
        # Schedule validations
        schedule.every(6).hours.do(self.run_scheduled_validation)  # Every 6 hours
        schedule.every().day.at("09:00").do(self.run_scheduled_validation)  # Daily at 9 AM
        schedule.every().monday.at("08:00").do(self.run_comprehensive_validation)  # Weekly comprehensive
        
        print("📅 Link validation scheduler started:")
        print("   • Every 6 hours: Quick validation")
        print("   • Daily at 9 AM: Standard validation") 
        print("   • Mondays at 8 AM: Comprehensive validation")
        
        # Run initial validation
        self.run_scheduled_validation()
        
        # Start the scheduler loop in a separate thread
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        
        return scheduler_thread
    
    def run_comprehensive_validation(self):
        """Run comprehensive validation with additional checks."""
        print("🔍 Running comprehensive validation...")
        
        # Run standard validation
        self.run_scheduled_validation()
        
        # Additional comprehensive checks
        self._check_reliability_scores()
        self._check_source_diversity()
        self._generate_weekly_report()
    
    def _check_reliability_scores(self):
        """Check if any sources have low reliability scores."""
        with self.validator.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM sources WHERE reliability_score < 0.7
            """)
            low_reliability_count = cursor.fetchone()[0]
            
            if low_reliability_count > 0:
                print(f"⚠️ Found {low_reliability_count} sources with reliability < 70%")
    
    def _check_source_diversity(self):
        """Check source type diversity."""
        with self.validator.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT source_type, COUNT(*) as count
                FROM sources
                GROUP BY source_type
                ORDER BY count DESC
            """)
            source_types = cursor.fetchall()
            
            print("📊 Source type distribution:")
            for source_type, count in source_types:
                print(f"   • {source_type}: {count}")
    
    def _generate_weekly_report(self):
        """Generate a comprehensive weekly report."""
        timestamp = datetime.now().strftime("%Y%m%d")
        report_filename = f"weekly_link_report_{timestamp}.txt"
        
        # This would generate a more detailed weekly report
        print(f"📄 Weekly report would be saved to: {report_filename}")
    
    def stop_scheduler(self):
        """Stop the validation scheduler."""
        self.is_running = False
        print("🛑 Link validation scheduler stopped")
    
    def get_validation_status(self):
        """Get current validation status for web interface."""
        if not self.last_validation:
            return {
                'status': 'never_run',
                'message': 'Validation has never been run',
                'last_run': None
            }
        
        time_since = datetime.now() - self.last_validation
        
        if time_since > timedelta(hours=12):
            status = 'stale'
            message = f'Last validation was {time_since.days} days ago'
        elif time_since > timedelta(hours=6):
            status = 'warning'
            message = f'Last validation was {int(time_since.total_seconds() // 3600)} hours ago'
        else:
            status = 'current'
            message = f'Last validation was {int(time_since.total_seconds() // 60)} minutes ago'
        
        return {
            'status': status,
            'message': message,
            'last_run': self.last_validation.isoformat(),
            'results_summary': self.validation_results['summary'] if self.validation_results else None
        }

# Global scheduler instance
link_scheduler = LinkValidationScheduler()

def start_link_validation_service():
    """Start the link validation service."""
    return link_scheduler.start_scheduler()

def get_link_validation_status():
    """Get validation status for web interface."""
    return link_scheduler.get_validation_status()

if __name__ == "__main__":
    # Run the scheduler
    scheduler = LinkValidationScheduler()
    thread = scheduler.start_scheduler()
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop_scheduler()
        print("✅ Scheduler stopped")
