"""Ingestion package initialization."""

from .scraper_factory import (
    BaseLegalScraper,
    GermanScraper,
    SpanishScraper,
    USScraper,
    ScraperFactory,
)

__all__ = [
    "BaseLegalScraper",
    "GermanScraper",
    "SpanishScraper",
    "USScraper",
    "ScraperFactory",
]
