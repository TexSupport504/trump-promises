"""
Command-line interface for the Trump Promises Tracker.
"""

import click
from datetime import datetime
from typing import Optional

from .database import DatabaseManager
from .models import Promise, Source, PromiseStatus, SourceType
from .scraper import PromiseScraper, PromiseSourceManager
from .analyzer import PromiseAnalyzer
from config import Config


@click.group()
def cli():
    """Trump Promises Tracker CLI"""
    pass


@cli.command()
def init_db():
    """Initialize the database."""
    click.echo("Initializing database...")
    db_manager = DatabaseManager()
    click.echo("Database initialized successfully!")


@cli.command()
@click.argument('text')
@click.option('--category', default='Other', help='Promise category')
@click.option('--source', help='Source description')
@click.option('--url', help='Source URL')
@click.option('--priority', type=int, default=3, help='Priority level (1-5)')
def add_promise(text: str, category: str, source: Optional[str], url: Optional[str], priority: int):
    """Add a new promise to the database."""
    db_manager = DatabaseManager()
    
    # Create source if provided
    sources = []
    if source or url:
        sources.append(Source(
            title=source or "Manual Entry",
            url=url,
            source_type=SourceType.OTHER,
            date=datetime.now(),
            description=f"Added via CLI on {datetime.now().strftime('%Y-%m-%d')}"
        ))
    
    # Create promise
    promise = Promise(
        text=text,
        category=category,
        priority=priority,
        date_made=datetime.now(),
        sources=sources
    )
    
    promise_id = db_manager.add_promise(promise)
    click.echo(f"Promise added with ID: {promise_id}")


@cli.command()
@click.argument('promise_id', type=int)
@click.argument('status')
@click.option('--notes', help='Optional notes about the status change')
def update_status(promise_id: int, status: str, notes: Optional[str]):
    """Update the status of a promise."""
    db_manager = DatabaseManager()
    
    try:
        promise_status = PromiseStatus(status)
    except ValueError:
        click.echo(f"Invalid status. Valid options: {[s.value for s in PromiseStatus]}")
        return
    
    promise = db_manager.get_promise(promise_id)
    if not promise:
        click.echo(f"Promise with ID {promise_id} not found.")
        return
    
    promise.update_status(promise_status, notes or "")
    
    if db_manager.update_promise(promise):
        click.echo(f"Promise {promise_id} status updated to: {status}")
    else:
        click.echo("Failed to update promise status.")


@cli.command()
@click.option('--category', help='Filter by category')
@click.option('--status', help='Filter by status')
@click.option('--limit', type=int, default=10, help='Maximum number of results')
def list_promises(category: Optional[str], status: Optional[str], limit: int):
    """List promises with optional filtering."""
    db_manager = DatabaseManager()
    
    status_filter = None
    if status:
        try:
            status_filter = PromiseStatus(status)
        except ValueError:
            click.echo(f"Invalid status. Valid options: {[s.value for s in PromiseStatus]}")
            return
    
    promises = db_manager.get_all_promises(category=category, status=status_filter)
    
    if not promises:
        click.echo("No promises found matching the criteria.")
        return
    
    click.echo(f"\nFound {len(promises)} promises:")
    click.echo("=" * 80)
    
    for i, promise in enumerate(promises[:limit]):
        click.echo(f"\nID: {promise.id}")
        click.echo(f"Text: {promise.text[:100]}{'...' if len(promise.text) > 100 else ''}")
        click.echo(f"Category: {promise.category}")
        click.echo(f"Status: {promise.status.value}")
        click.echo(f"Priority: {promise.priority}")
        click.echo(f"Progress: {promise.progress_percentage:.1f}%")
        click.echo(f"Last Updated: {promise.date_updated.strftime('%Y-%m-%d %H:%M')}")
        if promise.sources:
            click.echo(f"Sources: {len(promise.sources)}")
        click.echo("-" * 40)


@cli.command()
@click.argument('promise_id', type=int)
def show_promise(promise_id: int):
    """Show detailed information about a specific promise."""
    db_manager = DatabaseManager()
    promise = db_manager.get_promise(promise_id)
    
    if not promise:
        click.echo(f"Promise with ID {promise_id} not found.")
        return
    
    click.echo("\nPromise Details:")
    click.echo("=" * 60)
    click.echo(f"ID: {promise.id}")
    click.echo(f"Text: {promise.text}")
    click.echo(f"Category: {promise.category}")
    click.echo(f"Status: {promise.status.value}")
    click.echo(f"Priority: {promise.priority}")
    click.echo(f"Progress: {promise.progress_percentage:.1f}%")
    click.echo(f"Date Made: {promise.date_made.strftime('%Y-%m-%d') if promise.date_made else 'Unknown'}")
    click.echo(f"Last Updated: {promise.date_updated.strftime('%Y-%m-%d %H:%M')}")
    click.echo(f"Created: {promise.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    if promise.tags:
        click.echo(f"Tags: {', '.join(promise.tags)}")
    
    if promise.notes:
        click.echo(f"Notes: {promise.notes}")
    
    if promise.sources:
        click.echo(f"\nSources ({len(promise.sources)}):")
        for i, source in enumerate(promise.sources, 1):
            click.echo(f"  {i}. {source.title}")
            if source.url:
                click.echo(f"     URL: {source.url}")
            click.echo(f"     Type: {source.source_type.value}")
            click.echo(f"     Reliability: {source.reliability_score:.2f}")
    
    # Show progress updates
    progress_updates = db_manager.get_progress_updates(promise_id)
    if progress_updates:
        click.echo(f"\nProgress Updates ({len(progress_updates)}):")
        for update in progress_updates[:5]:  # Show last 5 updates
            click.echo(f"  • {update.date.strftime('%Y-%m-%d')}: {update.update_text}")


@cli.command()
def generate_report():
    """Generate analytics report."""
    db_manager = DatabaseManager()
    analyzer = PromiseAnalyzer(db_manager)
    
    click.echo("Generating analytics report...")
    
    # Get analytics data
    analytics = analyzer.generate_analytics_report()
    
    click.echo("\nTrump Promises Tracker - Analytics Report")
    click.echo("=" * 50)
    click.echo(f"Generated: {analytics.generated_at}")
    click.echo(f"Total Promises: {analytics.total_promises}")
    click.echo(f"Fulfillment Rate: {analytics.fulfillment_rate:.1f}%")
    click.echo(f"Average Progress: {analytics.average_progress:.1f}%")
    
    click.echo("\nPromises by Status:")
    for status, count in analytics.promises_by_status.items():
        percentage = (count / analytics.total_promises * 100) if analytics.total_promises > 0 else 0
        click.echo(f"  {status}: {count} ({percentage:.1f}%)")
    
    click.echo("\nPromises by Category:")
    for category, count in analytics.promises_by_category.items():
        percentage = (count / analytics.total_promises * 100) if analytics.total_promises > 0 else 0
        click.echo(f"  {category}: {count} ({percentage:.1f}%)")
    
    click.echo(f"\nMost Active Categories: {', '.join(analytics.most_active_categories)}")
    
    # Trends analysis
    trends = analyzer.analyze_promise_trends()
    click.echo(f"\nRecent Activity (Last 30 days):")
    click.echo(f"  New Promises: {trends['new_promises']}")
    click.echo(f"  Status Changes: {trends['status_changes']}")
    click.echo(f"  Fulfillment Velocity: {trends['fulfillment_velocity']:.2f} promises/day")


@cli.command()
@click.option('--source-type', type=click.Choice(['campaign', 'news', 'rss', 'transcripts']), 
              default='campaign', help='Type of source to scrape')
@click.option('--limit', type=int, default=10, help='Maximum promises to scrape')
def scrape_promises(source_type: str, limit: int):
    """Scrape promises from online sources."""
    click.echo(f"Scraping promises from {source_type} sources...")
    
    scraper = PromiseScraper()
    db_manager = DatabaseManager()
    
    scraped_promises = []
    
    if source_type == 'campaign':
        for url in PromiseSourceManager.CAMPAIGN_WEBSITES[:2]:  # Limit to first 2 for demo
            scraped_promises.extend(scraper.scrape_campaign_website(url))
    elif source_type == 'rss':
        scraped_promises.extend(scraper.scrape_rss_feeds(PromiseSourceManager.RSS_FEEDS))
    elif source_type == 'transcripts':
        scraped_promises.extend(scraper.scrape_speech_transcripts(PromiseSourceManager.SPEECH_TRANSCRIPT_URLS))
    else:
        click.echo("News scraping requires API integration (placeholder)")
        return
    
    if not scraped_promises:
        click.echo("No promises found from the specified sources.")
        return
    
    click.echo(f"Found {len(scraped_promises)} potential promises.")
    
    # Convert and save promises
    added_count = 0
    for scraped_promise in scraped_promises[:limit]:
        if scraped_promise.confidence_score >= 0.5:  # Only high-confidence promises
            promise = scraper.convert_to_promise(scraped_promise)
            promise_id = db_manager.add_promise(promise)
            added_count += 1
            click.echo(f"Added promise {promise_id}: {promise.text[:50]}...")
    
    click.echo(f"\nAdded {added_count} new promises to the database.")


@cli.command()
def show_stats():
    """Show quick statistics."""
    db_manager = DatabaseManager()
    analytics_data = db_manager.get_analytics_data()
    
    click.echo("\nQuick Statistics:")
    click.echo("=" * 30)
    click.echo(f"Total Promises: {analytics_data['total_promises']}")
    click.echo(f"Fulfillment Rate: {analytics_data['fulfillment_rate']:.1f}%")
    click.echo(f"Average Progress: {analytics_data['average_progress']:.1f}%")
    
    if analytics_data['most_active_categories']:
        click.echo(f"Top Category: {analytics_data['most_active_categories'][0]}")


@cli.command()
@click.argument('promise_id', type=int)
@click.argument('progress', type=float)
@click.option('--notes', help='Notes about the progress update')
def update_progress(promise_id: int, progress: float, notes: Optional[str]):
    """Update the progress percentage of a promise."""
    if not 0 <= progress <= 100:
        click.echo("Progress must be between 0 and 100.")
        return
    
    db_manager = DatabaseManager()
    promise = db_manager.get_promise(promise_id)
    
    if not promise:
        click.echo(f"Promise with ID {promise_id} not found.")
        return
    
    old_progress = promise.progress_percentage
    promise.progress_percentage = progress
    promise.date_updated = datetime.now()
    
    if notes:
        promise.notes += f"\n[{datetime.now().strftime('%Y-%m-%d')}] Progress updated from {old_progress}% to {progress}%: {notes}"
    
    if db_manager.update_promise(promise):
        click.echo(f"Promise {promise_id} progress updated to {progress}%")
    else:
        click.echo("Failed to update promise progress.")


if __name__ == '__main__':
    cli()
