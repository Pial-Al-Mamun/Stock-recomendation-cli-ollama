# ai/ollama_client.py
"""Ollama AI integration for stock analysis."""

import asyncio
import ollama
from typing import Dict
from config import OLLAMA_MODEL
from prompts.templates import build_analysis_prompt


async def get_ai_prediction(
    ticker: str, indicators: Dict, news_str: str, info: Dict
) -> str:
    """
    Send analysis prompt to Ollama and return the model's response.

    Args:
        ticker: Stock ticker symbol
        indicators: Technical indicators dictionary
        news_str: Formatted news headlines string
        info: Company info dictionary from yfinance

    Returns:
        AI model's analysis text
    """
    prompt = build_analysis_prompt(ticker, indicators, news_str, info)

    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        None,
        lambda: ollama.chat(
            model=OLLAMA_MODEL, messages=[{"role": "user", "content": prompt}]
        ),
    )

    return response["message"]["content"]
