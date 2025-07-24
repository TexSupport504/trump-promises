# Trump Promises Tracker

A comprehensive Python application to track President Trump's campaign promises from his first term through his current term, including analysis and monitoring capabilities.

## Features

- **Promise Tracking**: Comprehensive database of campaign promises
- **Source Management**: Track multiple sources for each promise
- **Status Monitoring**: Track fulfillment status of promises
- **Web Interface**: User-friendly web interface for browsing and managing promises
- **CLI Tools**: Command-line interface for data management
- **Analytics**: Analysis and visualization of promise data
- **Auto-Collection**: Automated scraping of new promises from various sources

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd trump-promises
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python -m app.cli init-db
```

## Usage

### Web Interface
```bash
python app.py
```
Visit `http://localhost:5000` to access the web interface.

### CLI Commands
```bash
# Initialize database
python -m app.cli init-db

# Add a new promise
python -m app.cli add-promise "Promise text" --category "Economy" --source "Rally in Iowa"

# Update promise status
python -m app.cli update-status <promise_id> "In Progress"

# Generate analytics report
python -m app.cli generate-report
```

## Project Structure

```
trump-promises/
├── app/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── database.py        # Database utilities
│   ├── scraper.py         # Web scraping utilities
│   ├── analyzer.py        # Promise analysis tools
│   ├── cli.py            # Command-line interface
│   └── web/
│       ├── __init__.py
│       ├── routes.py      # Flask routes
│       └── templates/     # HTML templates
├── data/
│   └── promises.db       # SQLite database
├── config.py             # Application configuration
├── app.py               # Main application entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Data Sources

The application can collect promises from:
- Campaign rallies and speeches
- Official campaign websites
- News interviews
- Social media posts
- Policy documents
- Debate transcripts

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational and informational purposes.
