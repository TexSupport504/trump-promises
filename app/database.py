"""
Database utilities for the Trump Promises Tracker application.
"""

import os
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

from .models import Promise, Source, ProgressUpdate, PromiseStatus, SourceType


class DatabaseManager:
    """Manages database operations for the promises tracker."""
    
    def __init__(self, db_path: str = "data/promises.db"):
        # Convert to absolute path based on the project root
        if not os.path.isabs(db_path):
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.db_path = os.path.join(project_root, db_path)
        else:
            self.db_path = db_path
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database with required tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create sources table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    title TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    date TEXT,
                    description TEXT,
                    reliability_score REAL DEFAULT 1.0,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create promises table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS promises (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    category TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER DEFAULT 3,
                    date_made TEXT,
                    date_updated TEXT NOT NULL,
                    tags TEXT,  -- JSON array
                    notes TEXT,
                    progress_percentage REAL DEFAULT 0.0,
                    related_promises TEXT,  -- JSON array of IDs
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create promise_sources junction table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS promise_sources (
                    promise_id INTEGER,
                    source_id INTEGER,
                    PRIMARY KEY (promise_id, source_id),
                    FOREIGN KEY (promise_id) REFERENCES promises (id) ON DELETE CASCADE,
                    FOREIGN KEY (source_id) REFERENCES sources (id) ON DELETE CASCADE
                )
            """)
            
            # Create progress_updates table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS progress_updates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    promise_id INTEGER NOT NULL,
                    update_text TEXT NOT NULL,
                    date TEXT NOT NULL,
                    source_url TEXT,
                    impact_score REAL DEFAULT 0.0,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (promise_id) REFERENCES promises (id) ON DELETE CASCADE
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_promises_category ON promises (category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_promises_status ON promises (status)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_promises_date_made ON promises (date_made)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_progress_updates_promise_id ON progress_updates (promise_id)")
            
            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode for better concurrency
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def add_source(self, source: Source) -> int:
        """Add a new source to the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sources (url, title, source_type, date, description, reliability_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                source.url,
                source.title,
                source.source_type.value,
                source.date.isoformat() if source.date else None,
                source.description,
                source.reliability_score,
                source.created_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_source(self, source_id: int) -> Optional[Source]:
        """Get a source by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sources WHERE id = ?", (source_id,))
            row = cursor.fetchone()
            
            if row:
                return Source(
                    id=row['id'],
                    url=row['url'],
                    title=row['title'],
                    source_type=SourceType(row['source_type']),
                    date=datetime.fromisoformat(row['date']) if row['date'] else None,
                    description=row['description'],
                    reliability_score=row['reliability_score'],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
            return None
    
    def add_promise(self, promise: Promise) -> int:
        """Add a new promise to the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Add sources first
            source_ids = []
            for source in promise.sources:
                if source.id is None:
                    cursor.execute("""
                        INSERT INTO sources (url, title, source_type, date, description, reliability_score, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        source.url,
                        source.title,
                        source.source_type.value,
                        source.date.isoformat() if source.date else None,
                        source.description,
                        source.reliability_score,
                        source.created_at.isoformat()
                    ))
                    source.id = cursor.lastrowid
                source_ids.append(source.id)
            
            # Insert the promise
            cursor.execute("""
                INSERT INTO promises (text, category, status, priority, date_made, date_updated, 
                                    tags, notes, progress_percentage, related_promises, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                promise.text,
                promise.category,
                promise.status.value,
                promise.priority,
                promise.date_made.isoformat() if promise.date_made else None,
                promise.date_updated.isoformat(),
                json.dumps(promise.tags),
                promise.notes,
                promise.progress_percentage,
                json.dumps(promise.related_promises),
                promise.created_at.isoformat()
            ))
            
            promise_id = cursor.lastrowid
            
            # Link sources to promise
            for source_id in source_ids:
                cursor.execute("""
                    INSERT OR IGNORE INTO promise_sources (promise_id, source_id)
                    VALUES (?, ?)
                """, (promise_id, source_id))
            
            conn.commit()
            return promise_id or 0
    
    def get_promise(self, promise_id: int) -> Optional[Promise]:
        """Get a promise by ID with all associated sources."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get the promise
            cursor.execute("SELECT * FROM promises WHERE id = ?", (promise_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Get associated sources
            cursor.execute("""
                SELECT s.* FROM sources s
                INNER JOIN promise_sources ps ON s.id = ps.source_id
                WHERE ps.promise_id = ?
            """, (promise_id,))
            source_rows = cursor.fetchall()
            
            sources = []
            for source_row in source_rows:
                sources.append(Source(
                    id=source_row['id'],
                    url=source_row['url'],
                    title=source_row['title'],
                    source_type=SourceType(source_row['source_type']),
                    date=datetime.fromisoformat(source_row['date']) if source_row['date'] else None,
                    description=source_row['description'],
                    reliability_score=source_row['reliability_score'],
                    created_at=datetime.fromisoformat(source_row['created_at'])
                ))
            
            return Promise(
                id=row['id'],
                text=row['text'],
                category=row['category'],
                status=PromiseStatus(row['status']),
                priority=row['priority'],
                date_made=datetime.fromisoformat(row['date_made']) if row['date_made'] else None,
                date_updated=datetime.fromisoformat(row['date_updated']),
                sources=sources,
                tags=json.loads(row['tags']) if row['tags'] else [],
                notes=row['notes'] or "",
                progress_percentage=row['progress_percentage'],
                related_promises=json.loads(row['related_promises']) if row['related_promises'] else [],
                created_at=datetime.fromisoformat(row['created_at'])
            )
    
    def update_promise(self, promise: Promise) -> bool:
        """Update an existing promise."""
        if promise.id is None:
            return False
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE promises 
                SET text = ?, category = ?, status = ?, priority = ?, date_made = ?, 
                    date_updated = ?, tags = ?, notes = ?, progress_percentage = ?, 
                    related_promises = ?
                WHERE id = ?
            """, (
                promise.text,
                promise.category,
                promise.status.value,
                promise.priority,
                promise.date_made.isoformat() if promise.date_made else None,
                promise.date_updated.isoformat(),
                json.dumps(promise.tags),
                promise.notes,
                promise.progress_percentage,
                json.dumps(promise.related_promises),
                promise.id
            ))
            
            conn.commit()
            return cursor.rowcount > 0
    
    def get_all_promises(self, category: Optional[str] = None, status: Optional[PromiseStatus] = None) -> List[Promise]:
        """Get all promises, optionally filtered by category or status."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM promises"
            params = []
            
            if category or status:
                query += " WHERE "
                conditions = []
                
                if category:
                    conditions.append("category = ?")
                    params.append(category)
                
                if status:
                    conditions.append("status = ?")
                    params.append(status.value)
                
                query += " AND ".join(conditions)
            
            query += " ORDER BY date_updated DESC"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            promises = []
            for row in rows:
                promise = Promise(
                    id=row['id'],
                    text=row['text'],
                    category=row['category'],
                    status=PromiseStatus(row['status']),
                    priority=row['priority'],
                    date_made=datetime.fromisoformat(row['date_made']) if row['date_made'] else None,
                    date_updated=datetime.fromisoformat(row['date_updated']),
                    tags=json.loads(row['tags']) if row['tags'] else [],
                    notes=row['notes'] or "",
                    progress_percentage=row['progress_percentage'],
                    related_promises=json.loads(row['related_promises']) if row['related_promises'] else [],
                    created_at=datetime.fromisoformat(row['created_at'])
                )
                
                # Load sources for each promise
                cursor.execute("""
                    SELECT s.* FROM sources s
                    INNER JOIN promise_sources ps ON s.id = ps.source_id
                    WHERE ps.promise_id = ?
                """, (promise.id,))
                source_rows = cursor.fetchall()
                
                for source_row in source_rows:
                    promise.sources.append(Source(
                        id=source_row['id'],
                        url=source_row['url'],
                        title=source_row['title'],
                        source_type=SourceType(source_row['source_type']),
                        date=datetime.fromisoformat(source_row['date']) if source_row['date'] else None,
                        description=source_row['description'],
                        reliability_score=source_row['reliability_score'],
                        created_at=datetime.fromisoformat(source_row['created_at'])
                    ))
                
                promises.append(promise)
            
            return promises
    
    def add_progress_update(self, update: ProgressUpdate) -> int:
        """Add a progress update for a promise."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO progress_updates (promise_id, update_text, date, source_url, impact_score, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                update.promise_id,
                update.update_text,
                update.date.isoformat(),
                update.source_url,
                update.impact_score,
                update.created_at.isoformat()
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_progress_updates(self, promise_id: int) -> List[ProgressUpdate]:
        """Get all progress updates for a promise."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM progress_updates 
                WHERE promise_id = ? 
                ORDER BY date DESC
            """, (promise_id,))
            rows = cursor.fetchall()
            
            updates = []
            for row in rows:
                updates.append(ProgressUpdate(
                    id=row['id'],
                    promise_id=row['promise_id'],
                    update_text=row['update_text'],
                    date=datetime.fromisoformat(row['date']),
                    source_url=row['source_url'],
                    impact_score=row['impact_score'],
                    created_at=datetime.fromisoformat(row['created_at'])
                ))
            
            return updates
    
    def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data for all promises."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total promises
            cursor.execute("SELECT COUNT(*) as total FROM promises")
            total_promises = cursor.fetchone()['total']
            
            # Promises by status
            cursor.execute("SELECT status, COUNT(*) as count FROM promises GROUP BY status")
            promises_by_status = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Promises by category
            cursor.execute("SELECT category, COUNT(*) as count FROM promises GROUP BY category ORDER BY count DESC")
            promises_by_category = {row['category']: row['count'] for row in cursor.fetchall()}
            
            # Average progress
            cursor.execute("SELECT AVG(progress_percentage) as avg_progress FROM promises")
            avg_progress = cursor.fetchone()['avg_progress'] or 0.0
            
            # Fulfillment rate
            fulfilled_count = promises_by_status.get('Fulfilled', 0) + promises_by_status.get('Partially Fulfilled', 0)
            fulfillment_rate = (fulfilled_count / total_promises * 100) if total_promises > 0 else 0.0
            
            return {
                'total_promises': total_promises,
                'promises_by_status': promises_by_status,
                'promises_by_category': promises_by_category,
                'fulfillment_rate': fulfillment_rate,
                'average_progress': avg_progress,
                'most_active_categories': list(promises_by_category.keys())[:5],
                'generated_at': datetime.now().isoformat()
            }
