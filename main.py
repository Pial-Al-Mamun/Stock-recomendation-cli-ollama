# main.py
"""CLI entry point for the stock analyzer."""

import asyncio
import sys

from ai.ollama_client import get_ai_prediction
from analysis.indicators import compute_technical_indicators
from config import WATCHLIST
from data.fetcher import fetch_stock_data
from screeners.fast_trades import rank_fast_trades
from screeners.long_term import rank_long_term_investments
from utils.formatters import format_news_headlines


async def analyze_single_stock():
    """Fetch data for a single ticker and get AI prediction."""
    ticker = input("Enter ticker symbol (e.g., AAPL): ").strip().upper()

    if not ticker:
        print("No ticker entered.")
        return

    print(f"\n📊 Fetching data for {ticker}...")
    data = await fetch_stock_data(ticker)

    if data["history"].empty:
        print(f"❌ No historical data found for {ticker}")
        return

    # Compute technical indicators
    indicators = compute_technical_indicators(data["history"])

    # Format news
    news_formatted = format_news_headlines(data["news"])

    # Display collected data summary
    print(f"\n✅ Data collected for {ticker}:")
    print(f"   Latest Price: ${indicators['latest_close']:.2f}")
    print(f"   5-Day Change: {indicators['price_change_5d_percent']:+.2f}%")
    print(f"   RSI: {indicators['rsi']:.1f}")
    print(f"   Market Cap: ${data['info'].get('marketCap', 'N/A'):,}")
    print(f"\n🤖 Asking {sys.modules['config'].OLLAMA_MODEL} for analysis...\n")

    # Get AI prediction
    prediction = await get_ai_prediction(
        ticker, indicators, news_formatted, data["info"]
    )

    print("=" * 60)
    print(prediction)
    print("=" * 60)


async def screen_stocks():
    """Scan watchlist and rank by momentum or fundamentals."""
    print("\nScreening Mode:")
    print("  1 - ⚡ Fast trades (momentum-based, short-term)")
    print("  2 - 📈 Long-term investment (fundamentals-based)")
    mode = input("Choose mode (1 or 2): ").strip()

    if mode not in ("1", "2"):
        print("❌ Invalid choice. Returning to menu.")
        return

    print(f"\n🔍 Scanning {len(WATCHLIST)} stocks...")

    # Fetch all stocks concurrently
    tasks = [fetch_stock_data(ticker) for ticker in WATCHLIST]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Build data dictionary, skipping errors
    stocks_data = {}
    errors = []
    for ticker, result in zip(WATCHLIST, results):
        if isinstance(result, Exception):
            errors.append((ticker, str(result)))
        else:
            stocks_data[ticker] = result

    if errors:
        print(f"\n⚠️  Failed to fetch {len(errors)} stock(s):")
        for ticker, err in errors[:3]:
            print(f"   - {ticker}: {err}")

    if not stocks_data:
        print("❌ No data available to screen.")
        return

    # Apply selected screener
    if mode == "1":
        print("\n" + "=" * 60)
        print("⚡ TOP MOMENTUM PICKS (Fast Trades)")
        print("=" * 60)

        rankings = rank_fast_trades(stocks_data)
        if not rankings:
            print("No stocks with positive momentum found.")
            return

        for rank, (ticker, score, indicators) in enumerate(rankings[:5], 1):
            print(f"\n{rank}. {ticker} — Momentum Score: {score:.2f}")
            print(f"   5-Day Change: {indicators['price_change_5d_percent']:+.2f}%")
            print(f"   RSI: {indicators['rsi']:.1f}")
            print(f"   Volume Ratio: {indicators['vol_ratio']:.2f}x avg")

    else:
        print("\n" + "=" * 60)
        print("📈 TOP LONG-TERM INVESTMENT PICKS")
        print("=" * 60)

        rankings = rank_long_term_investments(stocks_data)
        if not rankings:
            print("No stocks with sufficient fundamental data found.")
            return

        for rank, (ticker, score, info) in enumerate(rankings[:5], 1):
            print(f"\n{rank}. {ticker} — Value Score: {score:.2f}")
            print(f"   Forward P/E: {info.get('forwardPE', 'N/A')}")
            print(f"   Revenue Growth: {info.get('revenueGrowth', 'N/A')}")
            print(f"   ROE: {info.get('returnOnEquity', 'N/A')}")
            print(f"   Sector: {info.get('sector', 'N/A')}")

    print("\n" + "-" * 60)


async def main():
    """Display and handle the main CLI menu."""
    while True:
        print("\n" + "🏦" * 20)
        print("       STOCK ANALYZER CLI")
        print("🏦" * 20)
        print("\n1. 📋 Analyze a specific stock")
        print("2. 🔍 Find best stocks (screening)")
        print("3. 🚪 Exit")

        choice = input("\n➡️  Select option (1-3): ").strip()

        if choice == "1":
            await analyze_single_stock()
        elif choice == "2":
            await screen_stocks()
        elif choice == "3":
            print("\n👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
