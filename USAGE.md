# Trump Promises Tracker - Usage Guide

## Quick Start

1. **Setup**: Run `python setup.py` to initialize the database and add sample data
2. **Web Interface**: Run `python run_server.py` and visit http://localhost:5000
3. **CLI Tools**: Use `python -m app.cli --help` for command-line operations

## Web Interface Features

### Dashboard (/)
- Overview of all promises with key statistics
- Charts showing promise distribution by status and category
- Recent promises with progress indicators

### All Promises (/promises)
- Complete list of all promises with filtering options
- Filter by category and status
- Pagination for large datasets
- Progress bars and status indicators

### Promise Details (/promise/<id>)
- Detailed view of individual promises
- Source information and links
- Progress updates timeline
- Similar promises suggestions
- Complexity analysis

### Analytics (/analytics)
- Comprehensive analytics dashboard
- Trend analysis over time
- Priority recommendations
- Category performance metrics

### Add Promise (/add_promise)
- Form to add new promises manually
- Source attribution
- Category and priority assignment

## CLI Commands

### Database Management
```bash
# Initialize database
python -m app.cli init-db

# Show quick statistics
python -m app.cli show-stats
```

### Promise Management
```bash
# Add a new promise
python -m app.cli add-promise "Promise text" --category "Economy" --priority 4

# List promises
python -m app.cli list-promises --limit 10

# Filter promises
python -m app.cli list-promises --category "Immigration" --status "Fulfilled"

# Show detailed promise information
python -m app.cli show-promise 1
```

### Status Updates
```bash
# Update promise status
python -m app.cli update-status 1 "Fulfilled" --notes "Completed in 2024"

# Update progress percentage
python -m app.cli update-progress 1 75 --notes "Significant progress made"
```

### Analytics
```bash
# Generate comprehensive report
python -m app.cli generate-report
```

### Data Collection
```bash
# Scrape promises from online sources
python -m app.cli scrape-promises --source-type campaign --limit 10
```

## API Endpoints

### GET /api/promises
- Returns all promises as JSON
- Supports category and status filtering
- Example: `/api/promises?category=Economy&status=Fulfilled`

### GET /api/analytics
- Returns analytics data as JSON
- Includes all dashboard statistics

### POST /api/promise/<id>/update_status
- Updates promise status
- Requires JSON body: `{"status": "Fulfilled", "notes": "Optional notes"}`

### POST /api/promise/<id>/update_progress
- Updates promise progress percentage
- Requires JSON body: `{"progress": 75, "notes": "Optional notes"}`

## Data Categories

The system organizes promises into these categories:
- **Economy**: Jobs, GDP, economic growth, business policies
- **Immigration**: Border security, visa policies, deportation
- **Healthcare**: Insurance, Medicare, Medicaid, health reform
- **Foreign Policy**: International relations, treaties, diplomacy
- **Defense**: Military spending, veterans affairs, security
- **Energy**: Oil, gas, renewable energy, independence
- **Education**: School policies, funding, reforms
- **Infrastructure**: Roads, bridges, transportation, airports
- **Trade**: International trade deals, tariffs, agreements
- **Judiciary**: Court appointments, legal reforms
- **Environment**: Climate policies, regulations
- **Tax Policy**: Tax cuts, reforms, IRS policies
- **Social Issues**: Cultural and social policies
- **Technology**: Tech regulations, innovation policies
- **Other**: Miscellaneous promises

## Promise Statuses

- **Not Started**: No action has been taken
- **In Progress**: Work is actively underway
- **Fulfilled**: Promise has been completely kept
- **Partially Fulfilled**: Promise has been partially kept
- **Broken**: Promise was not kept
- **Stalled**: Progress has stopped
- **Compromised**: Modified version was implemented

## Data Sources

The system can track promises from various sources:
- Campaign rally speeches
- Official campaign websites
- News interviews
- Social media posts
- Policy documents
- Debate transcripts
- Press conferences
- Official statements

## Web Scraping

The system includes tools to automatically collect promises from:
- Campaign websites
- RSS feeds
- Speech transcripts
- News articles (with API integration)

Use responsibly and respect robots.txt files and rate limits.

## Database Schema

### Promises Table
- ID, text, category, status, priority
- Date made, date updated, progress percentage
- Notes, tags, related promises

### Sources Table
- ID, URL, title, source type, date
- Description, reliability score

### Promise-Sources Junction Table
- Links promises to their sources
- Many-to-many relationship

### Progress Updates Table
- ID, promise ID, update text, date
- Source URL, impact score

## Advanced Features

### Promise Analysis
- Complexity scoring based on specificity
- Similar promise detection
- Priority recommendations
- Trend analysis

### Export/Import
- JSON export of all data
- Analytics report generation
- Progress tracking

### Security
- Input validation
- SQL injection prevention
- XSS protection

## Development

### Adding New Features
1. Update models in `app/models.py`
2. Add database migrations in `app/database.py`
3. Create CLI commands in `app/cli.py`
4. Add web routes in `app/web/routes.py`
5. Create templates in `app/web/templates/`

### Testing
```bash
# Test CLI functionality
python -m app.cli show-stats

# Test web server
python run_server.py

# Test database operations
python -c "from app.database import DatabaseManager; db = DatabaseManager(); print(db.get_analytics_data())"
```

## Deployment

### Production Setup
1. Set environment variables:
   - `SECRET_KEY`: Random secret key for Flask
   - `DATABASE_URL`: Production database URL
   - `FLASK_DEBUG`: Set to 'false'

2. Use production WSGI server:
   ```bash
   gunicorn app:app
   ```

3. Set up reverse proxy (nginx/Apache)
4. Configure SSL certificate
5. Set up monitoring and backups

## Troubleshooting

### Common Issues
1. **Database locked**: Restart the application
2. **Import errors**: Check Python path and virtual environment
3. **Port in use**: Change port in configuration
4. **Permission errors**: Check file permissions in data directory

### Logs
- Application logs are stored in the `logs/` directory
- Database file is in `data/promises.db`
- Check terminal output for error messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request
5. Follow coding standards and documentation

## License

This project is for educational and informational purposes. Use responsibly and in accordance with applicable laws and terms of service.
