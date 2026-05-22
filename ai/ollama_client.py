# ai/ollama_client.py
"""Ollama AI integration for stock analysis."""

import asyncio
import os
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

    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    client = ollama.Client(host=host)

    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
            ),
        )
    except ollama.ResponseError as e:
        if e.status_code == 404 and "model" in str(e).lower():
            print(
                f"\n⏬ Ollama model '{OLLAMA_MODEL}' not found. Pulling it now (this may take a few minutes)...\n"
            )
            await loop.run_in_executor(None, lambda: client.pull(OLLAMA_MODEL))
            print("\n✅ Model pulled successfully. Now analyzing...\n")
            response = await loop.run_in_executor(
                None,
                lambda: client.chat(
                    model=OLLAMA_MODEL,
                    messages=[{"role": "user", "content": prompt}],
                ),
            )
        else:
            raise

    return response["message"]["content"]
