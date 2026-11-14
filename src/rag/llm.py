"""LLM provider layer.

One `stream_chat()` generator and one `chat()` convenience wrapper drive every mode.
Providers `slm` (Ollama, the default), `groq`, `openai`, and `openrouter` all speak the
OpenAI chat-completions API; `anthropic` uses the Messages API.

The system prompt forces grounding: answer only from the supplied corpus context, say
so explicitly when the corpus lacks the answer, and cite the source document + page.
"""
from __future__ import annotations

import json
import os
from typing import Iterator

import requests

from src import config  # noqa: F401  (ensures .env is loaded)

BASE_URLS = {
    "slm": os.getenv("SLM_BASE_URL", "http://localhost:11434/v1"),
    "groq": "https://api.groq.com/openai/v1",
    "openai": "https://api.openai.com/v1",
    "openrouter": "https://openrouter.ai/api/v1",
    "anthropic": "https://api.anthropic.com/v1",
}

_DEFAULT_MODEL = {
    "slm": "qwen2.5:3b",
    "groq": "llama-3.3-70b-versatile",
    "openai": "gpt-4o-mini",
    "anthropic": "claude-3-5-haiku-20241022",
    "openrouter": "meta-llama/llama-3.1-8b-instruct",
}

_KEY_VAR = {
    "slm": "SLM_API_KEY",
    "groq": "GROQ_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}

SYSTEM_PROMPT = (
    "You are an assistant on Indian Income Tax, answering from an official corpus "
    "(the Income-tax Act, Union Budget speeches, and government FAQs).\n"
    "Rules:\n"
    "1. Answer ONLY using the provided context. Do not use outside knowledge.\n"
    "2. If the context does not contain the answer, say clearly: "
    "\"I could not find this in the provided corpus.\" Do not guess.\n"
    "3. Tax rules are year-specific. State the financial year / assessment year your "
    "answer applies to, and use provisions from that year's budget.\n"
    "4. For calculations, show the steps (slabs, surcharge, cess) explicitly.\n"
    "5. Cite the source document name and page for key figures, e.g. (bs2024_25.pdf p.12).\n"
    "6. Do NOT use LaTeX or math markup. Write all formulas and calculations in plain "
    "text using ordinary symbols (x or *, /, +, -, =, parentheses) and numbers — for "
    "example: Indexed Cost = Purchase Price x (CII sale / CII purchase). Never use "
    "\\frac, \\text, \\[ \\], \\( \\), or $ ... $."
)


def resolve() -> tuple[str, str, str]:
    """Return (provider, model, api_key)."""
    provider = os.getenv("LLM_PROVIDER", "slm").strip().lower()
    if provider not in BASE_URLS:
        raise SystemExit(f"LLM_PROVIDER={provider!r} not in {sorted(BASE_URLS)}")
    model = os.getenv("LLM_MODEL") or _DEFAULT_MODEL.get(provider, "")
    api_key = os.getenv(_KEY_VAR.get(provider, ""), "")
    return provider, model, api_key


def build_messages(question: str, context: str, history: list[dict] | None) -> list[dict]:
    user = f"Context from corpus:\n{context}\n\nQuestion: {question}"
    return (
        [{"role": "system", "content": SYSTEM_PROMPT}]
        + list(history or [])
        + [{"role": "user", "content": user}]
    )


def _max_tokens() -> int:
    return int(os.getenv("LLM_MAX_TOKENS", "900"))


def _temperature() -> float:
    return float(os.getenv("LLM_TEMPERATURE", "0.1"))


def _stream_openai(base: str, api_key: str, model: str, messages: list[dict]) -> Iterator[str]:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    with requests.post(
        f"{base}/chat/completions",
        headers=headers,
        json={
            "model": model,
            "messages": messages,
            "max_tokens": _max_tokens(),
            "temperature": _temperature(),
            "stream": True,
        },
        timeout=180,
        stream=True,
    ) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines(decode_unicode=True):
            if not raw or not raw.startswith("data:"):
                continue
            payload = raw[len("data:"):].strip()
            if payload == "[DONE]":
                break
            try:
                delta = json.loads(payload)["choices"][0]["delta"].get("content")
            except (json.JSONDecodeError, KeyError, IndexError):
                continue
            if delta:
                yield delta


def _stream_anthropic(api_key: str, model: str, messages: list[dict]) -> Iterator[str]:
    system_text = "\n".join(m["content"] for m in messages if m["role"] == "system")
    chat_msgs = [m for m in messages if m["role"] != "system"]
    with requests.post(
        f"{BASE_URLS['anthropic']}/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "system": system_text,
            "messages": chat_msgs,
            "max_tokens": _max_tokens(),
            "temperature": _temperature(),
            "stream": True,
        },
        timeout=180,
        stream=True,
    ) as resp:
        resp.raise_for_status()
        for raw in resp.iter_lines(decode_unicode=True):
            if not raw or not raw.startswith("data:"):
                continue
            try:
                evt = json.loads(raw[len("data:"):].strip())
            except json.JSONDecodeError:
                continue
            if evt.get("type") == "content_block_delta":
                piece = evt.get("delta", {}).get("text")
                if piece:
                    yield piece


def stream_chat(question: str, context: str, history: list[dict] | None = None) -> Iterator[str]:
    """Yield answer text deltas from the configured provider."""
    provider, model, api_key = resolve()
    messages = build_messages(question, context, history)
    if provider == "anthropic":
        yield from _stream_anthropic(api_key, model, messages)
    else:
        yield from _stream_openai(BASE_URLS[provider], api_key or "ollama", model, messages)


def chat(question: str, context: str, history: list[dict] | None = None) -> str:
    """Return the full answer as a single string (consumes the stream)."""
    return "".join(stream_chat(question, context, history))
