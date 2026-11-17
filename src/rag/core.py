"""The single RAG pipeline shared by every interaction mode (TITO/TIVO/VITO/VIVO)
and by the evaluation harness. The UI only chooses how the question arrives (typed or
transcribed) and how the answer leaves (text or speech) — the retrieval + grounded
generation below is identical for all four modes.
"""
from __future__ import annotations

import time
from typing import Iterator

from src import config
from src.rag import llm
from src.rag.retriever import Retriever

_retriever: Retriever | None = None


def get_retriever() -> Retriever:
    """Load and cache the retriever (and its embedding model) once per process."""
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


def dedupe_sources(hits: list[dict]) -> list[dict]:
    """Collapse hits to unique (doc, page) citations, preserving rank order."""
    seen: set[tuple] = set()
    out: list[dict] = []
    for h in hits:
        key = (h["doc"], h["page"])
        if key not in seen:
            seen.add(key)
            out.append({"doc": h["doc"], "page": h["page"], "fy_tag": h.get("fy_tag", "general")})
    return out


def build_context(hits: list[dict]) -> str:
    return "\n\n".join(f"{h['text']}\n[source: {h['doc']} p.{h['page']}]" for h in hits)


def search_query(question: str, history: list[dict] | None = None) -> str:
    """Compose the retrieval query for (possibly) multi-step questions.

    A follow-up like "what about the old regime?" has no searchable terms on its own,
    so we prepend the most recent user turn(s). This keeps retrieval (and the FY/AY
    year-biasing) anchored to the ongoing topic. Generation still uses the original
    question plus the full chat history — only the search query is expanded.
    """
    if not history:
        return question
    prior_users = [m["content"] for m in history if m.get("role") == "user"][-2:]
    combined = "  ".join([*prior_users, question]).strip()
    return combined[:800]


def retrieve(
    question: str, top_k: int | None = None, history: list[dict] | None = None
) -> tuple[list[dict], str, list[dict]]:
    """Return (hits, context_string, deduped_sources)."""
    ret = get_retriever()
    hits = ret.search(search_query(question, history), top_k=top_k)
    return hits, build_context(hits), dedupe_sources(hits)


def stream_answer(
    question: str, history: list[dict] | None = None, top_k: int | None = None
) -> tuple[list[dict], Iterator[str], dict]:
    """Return (sources, token_generator, usage).

    Sources are known before generation starts, so the UI can show citations
    immediately and stream the answer underneath. `usage` is an initially-empty dict
    that the provider fills with token counts (prompt/completion/total) once the
    generator is fully consumed — read it after the stream ends.
    """
    _hits, context, sources = retrieve(question, top_k, history)
    usage: dict = {}
    return sources, llm.stream_chat(question, context, history, usage_out=usage), usage


def answer_question(
    question: str, history: list[dict] | None = None, top_k: int | None = None
) -> dict:
    """Non-streaming convenience wrapper used by the eval harness and the CLI.

    Returns {answer, sources, hits, timings, usage}.
    """
    ret = get_retriever()
    t0 = time.perf_counter()
    hits = ret.search(search_query(question, history), top_k=top_k)
    t1 = time.perf_counter()
    context = build_context(hits)
    usage: dict = {}
    answer = llm.chat(question, context, history, usage_out=usage)
    t2 = time.perf_counter()
    timings = {
        "embed_ms": round(ret._t_embed_ms, 1),
        "search_ms": round(ret._t_search_ms, 1),
        "retrieve_ms": round((t1 - t0) * 1000, 1),
        "llm_ms": round((t2 - t1) * 1000, 1),
        "total_ms": round((t2 - t0) * 1000, 1),
    }
    return {
        "answer": answer,
        "sources": dedupe_sources(hits),
        "hits": hits,
        "timings": timings,
        "usage": usage,
    }


def format_sources(sources: list[dict]) -> str:
    return "; ".join(f"{s['doc']} p.{s['page']}" for s in sources)


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) or "What is the Section 80C deduction limit?"
    res = answer_question(q)
    print(res["answer"])
    print("\nSources:", format_sources(res["sources"]))
    print("Tokens:", res["usage"] or "(usage not reported)")
    print("Timings:", res["timings"])
