# analysis/indicators.py
"""Technical indicator calculations using numpy."""

import numpy as np
from typing import Dict
from config import SMA_SHORT_PERIOD, SMA_LONG_PERIOD, RSI_PERIOD, VOLUME_MA_PERIOD


def compute_technical_indicators(hist) -> Dict:
    """
    Compute SMA, RSI, volume ratio, and price changes from OHLCV data.

    Args:
        hist: yfinance history DataFrame with columns Close, Volume

    Returns:
        Dictionary of computed indicators
    """
    closes = hist["Close"].values
    volumes = hist["Volume"].values

    # Simple Moving Averages
    sma_short = (
        np.mean(closes[-SMA_SHORT_PERIOD:])
        if len(closes) >= SMA_SHORT_PERIOD
        else np.mean(closes)
    )
    sma_long = (
        np.mean(closes[-SMA_LONG_PERIOD:])
        if len(closes) >= SMA_LONG_PERIOD
        else np.mean(closes)
    )

    # Relative Strength Index (RSI)
    delta = np.diff(closes)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain = np.mean(gain[-RSI_PERIOD:]) if len(gain) >= RSI_PERIOD else np.mean(gain)
    avg_loss = np.mean(loss[-RSI_PERIOD:]) if len(loss) >= RSI_PERIOD else np.mean(loss)

    if avg_loss == 0:
        rsi = 100.0
    else:
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))

    # Volume analysis
    avg_vol = (
        np.mean(volumes[-VOLUME_MA_PERIOD:])
        if len(volumes) >= VOLUME_MA_PERIOD
        else np.mean(volumes)
    )
    latest_vol = volumes[-1]
    vol_ratio = latest_vol / avg_vol if avg_vol > 0 else 1.0

    # Price changes
    price_1d = (closes[-1] - closes[-2]) / closes[-2] * 100 if len(closes) >= 2 else 0.0
    price_5d = (closes[-1] - closes[-5]) / closes[-5] * 100 if len(closes) >= 5 else 0.0

    return {
        f"sma_{SMA_SHORT_PERIOD}": sma_short,
        f"sma_{SMA_LONG_PERIOD}": sma_long,
        "rsi": rsi,
        "vol_ratio": vol_ratio,
        "price_change_1d_percent": price_1d,
        "price_change_5d_percent": price_5d,
        "latest_close": closes[-1],
        "latest_volume": latest_vol,
    }
