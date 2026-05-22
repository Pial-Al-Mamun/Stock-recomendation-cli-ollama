# prompts/templates.py
"""Prompt templates for the Ollama AI model."""

from typing import Dict


def build_analysis_prompt(
    ticker: str, indicators: Dict, news_str: str, info: Dict
) -> str:
    """
    Build the analysis prompt with all available data.

    Args:
        ticker: Stock ticker
        indicators: Technical indicators dict
        news_str: Formatted recent news
        info: Company info dict

    Returns:
        Complete prompt string for the AI model
    """
    return f"""
You are an experienced financial analyst. Analyze the following data for {ticker} and provide:

1. **Short-term prediction (1-5 days):** RISE or FALL, with confidence 1-10
2. **Medium-term prediction (1-4 weeks):** RISE or FALL, with confidence 1-10
3. **Brief reasoning:** 2-3 sentences combining technical and fundamental factors

**Technical Indicators:**
- Latest Price: ${indicators["latest_close"]:.2f}
- SMA 20: ${indicators["sma_20"]:.2f}
- SMA 50: ${indicators["sma_50"]:.2f}
- RSI (14): {indicators["rsi"]:.1f}
- 1-Day Change: {indicators["price_change_1d_percent"]:+.2f}%
- 5-Day Change: {indicators["price_change_5d_percent"]:+.2f}%
- Volume Ratio (vs 20-day avg): {indicators["vol_ratio"]:.2f}

**Recent News Headlines:**
{news_str}

**Company Fundamentals:**
- Sector: {info.get("sector", "N/A")}
- Industry: {info.get("industry", "N/A")}
- Market Cap: ${info.get("marketCap", "N/A"):,} 
- P/E (TTM): {info.get("trailingPE", "N/A")}
- Forward P/E: {info.get("forwardPE", "N/A")}
- EPS (TTM): {info.get("trailingEps", "N/A")}
- Dividend Yield: {info.get("dividendYield", "N/A")}
- 52-Week High: ${info.get("fiftyTwoWeekHigh", "N/A")}
- 52-Week Low: ${info.get("fiftyTwoWeekLow", "N/A")}
- Beta: {info.get("beta", "N/A")}

Provide your analysis below:
"""
