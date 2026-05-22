# utils/formatters.py
"""Utility functions for formatting data."""

from typing import List


def format_news_headlines(news_list: List[dict], max_items: int = 5) -> str:
    """
    Extract and format news headlines from yfinance news data.

    Args:
        news_list: List of news item dictionaries
        max_items: Maximum number of headlines to include

    Returns:
        Formatted string of news headlines
    """
    headlines = []
    for item in news_list[:max_items]:
        title = item.get("title", "No title available")
        publisher = item.get("publisher", "Unknown source")
        headlines.append(f"- [{publisher}] {title}")

    return "\n".join(headlines) if headlines else "No recent news available."
