"""
Data models for the Trump Promises Tracker application.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class PromiseStatus(Enum):
    """Enumeration of possible promise statuses."""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    FULFILLED = "Fulfilled"
    PARTIALLY_FULFILLED = "Partially Fulfilled"
    BROKEN = "Broken"
    STALLED = "Stalled"
    COMPROMISED = "Compromised"


class SourceType(Enum):
    """Enumeration of source types."""
    RALLY_SPEECH = "Rally Speech"
    CAMPAIGN_WEBSITE = "Campaign Website"
    INTERVIEW = "Interview"
    SOCIAL_MEDIA = "Social Media"
    POLICY_DOCUMENT = "Policy Document"
    DEBATE = "Debate"
    PRESS_CONFERENCE = "Press Conference"
    OFFICIAL_STATEMENT = "Official Statement"
    OTHER = "Other"


@dataclass
class Source:
    """Represents a source for a promise."""
    id: Optional[int] = None
    url: Optional[str] = None
    title: str = ""
    source_type: SourceType = SourceType.OTHER
    date: Optional[datetime] = None
    description: str = ""
    reliability_score: float = 1.0  # 0-1 scale
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert source to dictionary."""
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'source_type': self.source_type.value,
            'date': self.date.isoformat() if self.date else None,
            'description': self.description,
            'reliability_score': self.reliability_score,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class Promise:
    """Represents a campaign promise."""
    id: Optional[int] = None
    text: str = ""
    category: str = "Other"
    status: PromiseStatus = PromiseStatus.NOT_STARTED
    priority: int = 3  # 1-5 scale, 5 being highest priority
    date_made: Optional[datetime] = None
    date_updated: datetime = field(default_factory=datetime.now)
    sources: List[Source] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    progress_percentage: float = 0.0  # 0-100
    related_promises: List[int] = field(default_factory=list)  # IDs of related promises
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert promise to dictionary."""
        return {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'status': self.status.value,
            'priority': self.priority,
            'date_made': self.date_made.isoformat() if self.date_made else None,
            'date_updated': self.date_updated.isoformat(),
            'sources': [source.to_dict() for source in self.sources],
            'tags': self.tags,
            'notes': self.notes,
            'progress_percentage': self.progress_percentage,
            'related_promises': self.related_promises,
            'created_at': self.created_at.isoformat()
        }
    
    def add_source(self, source: Source) -> None:
        """Add a source to this promise."""
        if source not in self.sources:
            self.sources.append(source)
            self.date_updated = datetime.now()
    
    def update_status(self, new_status: PromiseStatus, notes: str = "") -> None:
        """Update the promise status."""
        self.status = new_status
        self.date_updated = datetime.now()
        if notes:
            self.notes += f"\n[{datetime.now().strftime('%Y-%m-%d')}] Status changed to {new_status.value}: {notes}"
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to this promise."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.date_updated = datetime.now()


@dataclass
class ProgressUpdate:
    """Represents a progress update for a promise."""
    id: Optional[int] = None
    promise_id: int = 0
    update_text: str = ""
    date: datetime = field(default_factory=datetime.now)
    source_url: Optional[str] = None
    impact_score: float = 0.0  # -1 to 1, negative for setbacks
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert progress update to dictionary."""
        return {
            'id': self.id,
            'promise_id': self.promise_id,
            'update_text': self.update_text,
            'date': self.date.isoformat(),
            'source_url': self.source_url,
            'impact_score': self.impact_score,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class AnalyticsData:
    """Represents analytics data for promises."""
    total_promises: int = 0
    promises_by_status: Dict[str, int] = field(default_factory=dict)
    promises_by_category: Dict[str, int] = field(default_factory=dict)
    fulfillment_rate: float = 0.0
    average_progress: float = 0.0
    most_active_categories: List[str] = field(default_factory=list)
    recent_updates: List[Dict[str, Any]] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert analytics data to dictionary."""
        return {
            'total_promises': self.total_promises,
            'promises_by_status': self.promises_by_status,
            'promises_by_category': self.promises_by_category,
            'fulfillment_rate': self.fulfillment_rate,
            'average_progress': self.average_progress,
            'most_active_categories': self.most_active_categories,
            'recent_updates': self.recent_updates,
            'generated_at': self.generated_at.isoformat()
        }
