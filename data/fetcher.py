# data/fetcher.py
"""Async data fetching using yfinance."""

import asyncio
import yfinance as yf
from typing import Dict


async def fetch_stock_data(ticker: str) -> Dict:
    """
    Fetch info, historical prices (3mo), and news for a single ticker.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        Dictionary with keys: ticker, info, history, news
    """
    loop = asyncio.get_running_loop()

    # Run blocking yfinance calls in executor
    def _fetch():
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="3mo")

        # Handle news - it's a property, not a method
        try:
            news = stock.news  # Property access, not function call
        except Exception:
            news = []  # Fallback if news isn't available

        return {"ticker": ticker, "info": info, "history": hist, "news": news}

    result = await loop.run_in_executor(None, _fetch)
    return result
