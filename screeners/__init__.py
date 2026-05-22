# screeners/__init__.py
from .fast_trades import rank_fast_trades
from .long_term import rank_long_term_investments

__all__ = ["rank_fast_trades", "rank_long_term_investments"]
