"""
Web Scraper Agents - An agent-based architecture for web scraping and analysis.
"""

from .base_agent import BaseAgent
from .scraper_agent import WebScraperAgent
from .analyzer_agent import AnalyzerAgent
from .presenter_agent import PresenterAgent
from .orchestrator import AgentOrchestrator
from .models import (
    WebPage,
    ExtractedData,
    AnalysisResult,
    PresentationResult
)

__version__ = '1.0.0'
__all__ = [
    'BaseAgent',
    'WebScraperAgent',
    'AnalyzerAgent',
    'PresenterAgent',
    'AgentOrchestrator',
    'WebPage',
    'ExtractedData',
    'AnalysisResult',
    'PresentationResult',
]
