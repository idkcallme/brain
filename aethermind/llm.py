"""Simple interface to an LM Studio server."""

from __future__ import annotations
import requests
from typing import List, Dict

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"


def chat(messages: List[Dict[str, str]], model: str | None = None) -> str:
    """Send a chat completion request to LM Studio.

    Parameters
    ----------
    messages: list of {"role": str, "content": str}
        Conversation history following the OpenAI API format.
    model: optional model name registered with LM Studio.
    """
    payload = {"messages": messages}
    if model:
        payload["model"] = model
    resp = requests.post(LM_STUDIO_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]
