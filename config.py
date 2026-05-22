# config.py
"""Central configuration for the stock analyzer."""

# Ollama model to use
OLLAMA_MODEL = "llama3"  # change to "mistral", "phi3", etc.

# Default watchlist for screening
WATCHLIST = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA",
    "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS",
    "NFLX", "ADBE", "CRM", "PYPL"
]

# Technical indicator parameters
SMA_SHORT_PERIOD = 20
SMA_LONG_PERIOD = 50
RSI_PERIOD = 14
VOLUME_MA_PERIOD = 20

# Screening thresholds
RSI_OVERBOUGHT = 70
MOMENTUM_DAYS = 5