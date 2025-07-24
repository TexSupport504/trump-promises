import os
from datetime import datetime

class Config:
    """Application configuration class."""
    
    # Get project root directory
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL', os.path.join(PROJECT_ROOT, 'data', 'promises.db'))
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # API Keys (for news sources, social media APIs, etc.)
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    
    # Scraping settings
    REQUEST_DELAY = 1  # Delay between requests in seconds
    MAX_REQUESTS_PER_MINUTE = 30
    
    # Data directories
    DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
    LOGS_DIR = os.path.join(PROJECT_ROOT, 'logs')
    
    # Promise categories
    PROMISE_CATEGORIES = [
        'Economy',
        'Immigration',
        'Healthcare',
        'Foreign Policy',
        'Defense',
        'Energy',
        'Education',
        'Infrastructure',
        'Trade',
        'Judiciary',
        'Environment',
        'Tax Policy',
        'Social Issues',
        'Technology',
        'Other'
    ]
    
    # Promise statuses
    PROMISE_STATUSES = [
        'Not Started',
        'In Progress',
        'Fulfilled',
        'Partially Fulfilled',
        'Broken',
        'Stalled',
        'Compromised'
    ]
    
    # Source types
    SOURCE_TYPES = [
        'Rally Speech',
        'Campaign Website',
        'Interview',
        'Social Media',
        'Policy Document',
        'Debate',
        'Press Conference',
        'Official Statement',
        'Other'
    ]

    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        # Create necessary directories
        os.makedirs(Config.DATA_DIR, exist_ok=True)
        os.makedirs(Config.LOGS_DIR, exist_ok=True)
