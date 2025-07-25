#!/usr/bin/env python3
"""
Development helper script for Trump Promises Tracker
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_server():
    """Run the Flask development server."""
    try:
        print("🚀 Starting Trump Promises Tracker...")
        print("📍 Project root:", project_root)
        print("🌑 Black & White Dark Mode Active")
        print("=" * 50)
        
        # Set environment variables
        os.environ['FLASK_APP'] = 'app.py'
        os.environ['FLASK_ENV'] = 'development'
        os.environ['FLASK_DEBUG'] = '1'
        
        # Import and run the app
        from app.web.routes import create_app
        from config import Config
        
        app = create_app()
        Config.init_app(app)
        
        print("🌐 Server starting at http://localhost:5000")
        print("📱 Dark theme preview at http://localhost:5000")
        print("🎨 Static preview: file:///preview-dark-theme.html")
        print("=" * 50)
        
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def install_deps():
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def create_figma_assets():
    """Create assets for Figma design workflow."""
    assets_dir = project_root / 'design-assets'
    assets_dir.mkdir(exist_ok=True)
    
    # Create color palette file
    colors_file = assets_dir / 'color-palette.json'
    colors = {
        "primary": {
            "bg-primary": "#000000",
            "bg-secondary": "#1a1a1a", 
            "bg-tertiary": "#2d2d2d",
            "text-primary": "#ffffff",
            "text-secondary": "#e0e0e0",
            "text-muted": "#b0b0b0"
        },
        "accents": {
            "accent-primary": "#ffffff",
            "accent-secondary": "#808080", 
            "border-color": "#404040"
        },
        "shadows": {
            "shadow-light": "rgba(255, 255, 255, 0.1)",
            "shadow-dark": "rgba(0, 0, 0, 0.5)"
        }
    }
    
    import json
    with open(colors_file, 'w') as f:
        json.dump(colors, f, indent=2)
    
    print(f"🎨 Color palette saved to: {colors_file}")

def preview_theme():
    """Open the theme preview in browser."""
    preview_file = project_root / 'preview-dark-theme.html'
    if preview_file.exists():
        import webbrowser
        webbrowser.open(f'file://{preview_file.absolute()}')
        print(f"🌐 Opening theme preview: {preview_file}")
    else:
        print("❌ Preview file not found")

def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("🌑 Trump Promises Tracker - Black & White Dark Mode")
        print("=" * 50)
        print("Usage: python dev.py <command>")
        print("")
        print("Commands:")
        print("  run       - Start the development server")
        print("  install   - Install dependencies")
        print("  figma     - Create Figma design assets")
        print("  preview   - Open theme preview in browser")
        print("")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'run':
        run_server()
    elif command == 'install':
        install_deps()
    elif command == 'figma':
        create_figma_assets()
    elif command == 'preview':
        preview_theme()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main()
