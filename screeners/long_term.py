# screeners/long_term.py
"""Fundamental analysis screener for long-term investments."""

from typing import Dict, List, Tuple


def rank_long_term_investments(
    stocks_data: Dict[str, dict],
) -> List[Tuple[str, float, Dict]]:
    """
    Rank stocks by fundamental score for long-term investment.

    Score = (1/forward_PE) * 100 + revenue_growth * 100 + ROE

    Args:
        stocks_data: Dict mapping ticker -> {"info": ..., "history": ..., "news": ...}

    Returns:
        Sorted list of (ticker, score, info) tuples, highest score first
    """
    scores = []

    for ticker, data in stocks_data.items():
        info = data["info"]

        # Require forward PE for valuation
        fwd_pe = info.get("forwardPE")
        if fwd_pe is None or fwd_pe <= 0:
            continue

        # Growth and profitability metrics
        rev_growth = info.get("revenueGrowth", 0) or 0  # Fraction (0.15 = 15%)
        roe = info.get("returnOnEquity", 0) or 0  # Fraction (0.20 = 20%)

        # Composite score (higher is better)
        pe_score = (1.0 / fwd_pe) * 100  # Low PE = high score
        growth_score = rev_growth * 100  # High growth = high score
        roe_score = roe  # High ROE = high score

        total_score = pe_score + growth_score + roe_score
        scores.append((ticker, total_score, info))

    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
