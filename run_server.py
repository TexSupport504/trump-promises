"""
Simple launcher for the Trump Promises Tracker web application.
"""

import sys
import os

# Change to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add current directory to Python path
sys.path.insert(0, script_dir)

from app.web.routes import create_app

def main():
    """Launch the web application."""
    print("Starting Trump Promises Tracker...")
    print("=" * 40)
    
    app = create_app()
    
    print("Server starting on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
