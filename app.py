"""
Main application entry point for the Trump Promises Tracker.
"""

import os
from app.web.routes import create_app
from config import Config

# Create the Flask application
app = create_app()

# Start the link validation service
try:
    from link_validation_integration import start_link_validation_service
    start_link_validation_service()
except Exception as e:
    print(f"Warning: Could not start link validation service: {e}")

if __name__ == '__main__':
    # Create necessary directories
    Config.init_app(app)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=Config.DEBUG
    )
