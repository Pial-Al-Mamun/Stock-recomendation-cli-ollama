# screeners/fast_trades.py
"""Momentum-based screener for short-term trades."""

from typing import Dict, List, Tuple
from analysis.indicators import compute_technical_indicators
from config import RSI_OVERBOUGHT


def rank_fast_trades(stocks_data: Dict[str, dict]) -> List[Tuple[str, float, Dict]]:
    """
    Rank stocks by momentum score for fast trades.

    Score = positive_5d_return * volume_factor * overbought_penalty

    Args:
        stocks_data: Dict mapping ticker -> {"info": ..., "history": ..., "news": ...}

    Returns:
        Sorted list of (ticker, score, indicators) tuples, highest score first
    """
    scores = []

    for ticker, data in stocks_data.items():
        if data["history"].empty:
            continue

        ind = compute_technical_indicators(data["history"])
        momentum = ind["price_change_5d_percent"]

        # Skip negative momentum
        if momentum <= 0:
            continue

        # Volume factor (cap at 3x average)
        vol_score = min(ind["vol_ratio"], 3.0) / 3.0

        # Penalize overbought conditions
        rsi_penalty = 1.0 if ind["rsi"] < RSI_OVERBOUGHT else 0.5

        score = momentum * vol_score * rsi_penalty
        scores.append((ticker, score, ind))

    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores
