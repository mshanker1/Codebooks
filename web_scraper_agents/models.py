"""
Data models for the web scraper agent system.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class WebPage:
    """Represents a fetched web page."""
    url: str
    title: Optional[str] = None
    content: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    status_code: int = 0
    fetch_time: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None


@dataclass
class ExtractedData:
    """Represents extracted and structured data from a web page."""
    url: str
    title: str
    headings: List[str] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    links: List[Dict[str, str]] = field(default_factory=list)
    images: List[Dict[str, str]] = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    main_content: str = ""


@dataclass
class AnalysisResult:
    """Represents the analysis results."""
    url: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    word_count: int = 0
    content_type: str = "general"
    importance_score: float = 0.0


@dataclass
class PresentationResult:
    """Represents the final formatted presentation."""
    url: str
    formatted_text: str
    timestamp: datetime = field(default_factory=datetime.now)
