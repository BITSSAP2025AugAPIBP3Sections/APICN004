"""Compare LLM providers on latency, token usage, and cost for the same questions.

Runs the three representative questions (Easy / Medium / Complex) through the shared
RAG pipeline once per provider, capturing real token usage and wall-clock latency, and
computes an average cost per request from a configurable price table. Writes a markdown
table to report/comparison.md.

Usage:
    # local SLM only (no key needed):
    python tests/compare_providers.py

    # add Groq (set your key first):
    GROQ_API_KEY=... python tests/compare_providers.py

Accuracy is judged separately via tests/run_eval.py (the 13-question bank) per provider.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import core  # noqa: E402

# Representative questions (one per difficulty tier).
QUESTIONS = [
    ("Easy", "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?"),
    ("Medium", "A salaried individual earns ₹18,00,000 in FY 2024-25 under the new regime. Calculate the total tax, showing all steps."),
    ("Complex", "Mr. A (resident, 45): salary ₹24,00,000, LTCG ₹6,00,000 on listed equity sold after 23 July 2024, STCG ₹2,00,000, interest ₹3,00,000, PPF ₹2,00,000, medical ₹75,000. Compute tax under both regimes with surcharge and cess."),
]

# Provider configs to compare: (label, LLM_PROVIDER, LLM_MODEL, needs_key_env).
PROVIDERS = [
    ("Local SLM (Ollama)", "slm", "qwen2.5:3b", None),
    ("Groq (cloud)", "groq", "llama-3.3-70b-versatile", "GROQ_API_KEY"),
]

# USD price per 1,000,000 tokens (input, output). Fill with the provider's CURRENT
# published rates before trusting the cost column. Local Ollama is $0 (self-hosted).
# Leave an entry as None to print "set price" instead of a number.
PRICING = {
    "qwen2.5:3b": (0.0, 0.0),                 # local, self-hosted — no per-token cost
    "llama-3.3-70b-versatile": (None, None),  # TODO: set Groq's current $/1M in,out
}


def _cost_usd(model: str, usage: dict) -> float | None:
    rates = PRICING.get(model)
    if not rates or rates[0] is None or rates[1] is None or not usage:
        return None
    pin, pout = rates
    p = usage.get("prompt_tokens", 0)
    c = usage.get("completion_tokens", 0)
    return (p / 1_000_000) * pin + (c / 1_000_000) * pout


def run_provider(label: str, provider: str, model: str) -> list[dict]:
    os.environ["LLM_PROVIDER"] = provider
    os.environ["LLM_MODEL"] = model
    core.answer_question("warm up")  # warm the embedding cache
    rows = []
    for tier, q in QUESTIONS:
        t0 = time.time()
        res = core.answer_question(q)
        rows.append(
            {
                "tier": tier,
                "latency_ms": round((time.time() - t0) * 1000),
                "usage": res.get("usage", {}),
                "cost_usd": _cost_usd(model, res.get("usage", {})),
            }
        )
    return rows


def main() -> None:
    results = {}
    for label, provider, model, key_env in PROVIDERS:
        if key_env and not os.getenv(key_env):
            print(f"skip {label}: {key_env} not set")
            continue
        print(f"running {label} ({model}) …", flush=True)
        results[label] = (model, run_provider(label, provider, model))

    lines = ["# Provider Comparison — APICN004", ""]
    lines.append("Same three questions through the shared RAG pipeline; token usage is the")
    lines.append("provider's own reported count. Cost = prompt·$/1M-in + completion·$/1M-out.")
    lines.append("")
    lines.append("| Provider | Model | Tier | Latency (ms) | Prompt tok | Completion tok | Total tok | Cost (USD) |")
    lines.append("|----------|-------|------|-------------:|-----------:|---------------:|----------:|-----------:|")
    for label, (model, rows) in results.items():
        for r in rows:
            u = r["usage"] or {}
            cost = r["cost_usd"]
            cost_s = f"${cost:.6f}" if cost is not None else "set price"
            lines.append(
                f"| {label} | {model} | {r['tier']} | {r['latency_ms']:,} | "
                f"{u.get('prompt_tokens', '—')} | {u.get('completion_tokens', '—')} | "
                f"{u.get('total_tokens', '—')} | {cost_s} |"
            )
    # Averages
    lines.append("")
    lines.append("## Averages per request")
    lines.append("")
    lines.append("| Provider | Avg latency (ms) | Avg total tokens | Avg cost (USD) |")
    lines.append("|----------|-----------------:|-----------------:|---------------:|")
    for label, (model, rows) in results.items():
        n = len(rows) or 1
        avg_lat = round(sum(r["latency_ms"] for r in rows) / n)
        avg_tok = round(sum((r["usage"] or {}).get("total_tokens", 0) for r in rows) / n)
        costs = [r["cost_usd"] for r in rows if r["cost_usd"] is not None]
        avg_cost = f"${sum(costs) / len(costs):.6f}" if costs else "set price"
        lines.append(f"| {label} | {avg_lat:,} | {avg_tok:,} | {avg_cost} |")

    out = Path(__file__).resolve().parents[1] / "report" / "comparison.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
