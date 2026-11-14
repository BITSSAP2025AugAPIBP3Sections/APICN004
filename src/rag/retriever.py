"""Retrieval over the persistent ChromaDB index.

Returns top-k chunks with their source document + page, so every answer can be cited.
When a question names a financial/assessment year, retrieval is biased toward chunks
tagged with that year (budget-speech provisions) so year-sensitive answers don't mix
provisions from different budgets.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

from src import config
from src.rag import embed

# AY 2025-26 corresponds to FY 2024-25, etc. We map an AY in the question back to its FY.
_FY = re.compile(r"\bFY\s*(20\d{2})\s*[-/]\s*(\d{2})\b", re.IGNORECASE)
_AY = re.compile(r"\bAY\s*(20\d{2})\s*[-/]\s*(\d{2})\b", re.IGNORECASE)
_FINYEAR = re.compile(r"\b(20\d{2})\s*[-/]\s*(\d{2})\b")

# Supplementary FAQ / guidance documents in the corpus.
_FAQ_DOCS = [
    "FAQs-on-BIS-Exemption.pdf",
    "FAQs-on-FIIs-Exemption.pdf",
    "FAQs-on-Transition-Provisions.pdf",
    "Updated-FQAs-on-Interplay&Transitions.pdf",
    "E-Book-Guidance-Note-Crypto-Asset-Reporting-Obligations.pdf",
]
# Trigger words that suggest the question is asking about a FAQ / guidance document.
_FAQ_HINT = re.compile(
    r"\b(FAQ|faqs?|FII|foreign\s+institutional|BIS|transition\s+provision|interplay"
    r"|crypto\s+guidance|VDA\s+guidance|guidance\s+note|reporting\s+obligation)\b",
    re.IGNORECASE,
)


def detect_fy(question: str) -> str | None:
    """Return a canonical 'FY2024-25' tag implied by the question, or None."""
    m = _FY.search(question)
    if m:
        return f"FY{m.group(1)}-{m.group(2)}"
    m = _AY.search(question)
    if m:  # AY 2025-26 -> FY 2024-25
        start = int(m.group(1)) - 1
        return f"FY{start}-{str(start + 1)[-2:]}"
    m = _FINYEAR.search(question)
    if m:
        return f"FY{m.group(1)}-{m.group(2)}"
    return None


class Retriever:
    def __init__(self, index_dir: str | Path | None = None, collection: str | None = None):
        import chromadb

        path = Path(index_dir) if index_dir else config.index_dir()
        if not path.exists():
            raise RuntimeError(
                f"Index not found at {path}. Run `python src/rag/ingest.py` first."
            )
        self._client = chromadb.PersistentClient(path=str(path))
        self._coll = self._client.get_collection(collection or config.collection_name())
        self.count = self._coll.count()
        self._t_embed_ms = 0.0
        self._t_search_ms = 0.0

    def _query(self, vec: list[float], k: int, where: dict | None = None) -> list[dict]:
        res = self._coll.query(
            query_embeddings=[vec],
            n_results=k,
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        hits: list[dict] = []
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        dists = res["distances"][0]
        for text, meta, dist in zip(docs, metas, dists):
            hits.append(
                {
                    "text": text,
                    "doc": meta.get("doc", "?"),
                    "page": meta.get("page", "?"),
                    "fy_tag": meta.get("fy_tag", "general"),
                    "score": round(1.0 - float(dist), 4),  # cosine distance -> similarity
                }
            )
        return hits

    def search(self, query: str, top_k: int | None = None) -> list[dict]:
        k = top_k or config.top_k()
        if k <= 0:
            raise ValueError(f"top_k must be positive, got {k}")

        t0 = time.perf_counter()
        vec = embed.embed_query(query)
        self._t_embed_ms = (time.perf_counter() - t0) * 1000

        t1 = time.perf_counter()
        base = self._query(vec, k)

        fy = detect_fy(query)
        if fy:
            # Prepend year-matched provisions, then fill with the general ranking.
            fy_hits = self._query(vec, k, where={"fy_tag": fy})
            merged: list[dict] = []
            seen: set[tuple] = set()
            for h in fy_hits + base:
                key = (h["doc"], h["page"], h["text"][:40])
                if key not in seen:
                    seen.add(key)
                    merged.append(h)
            base = merged[:k]

        if _FAQ_HINT.search(query):
            # Prepend FAQ/guidance-doc chunks so they aren't buried by Act chunks.
            faq_hits = self._query(vec, k, where={"doc": {"$in": _FAQ_DOCS}})
            merged2: list[dict] = []
            seen2: set[tuple] = set()
            for h in faq_hits + base:
                key = (h["doc"], h["page"], h["text"][:40])
                if key not in seen2:
                    seen2.add(key)
                    merged2.append(h)
            base = merged2[:k]

        self._t_search_ms = (time.perf_counter() - t1) * 1000
        return base


if __name__ == "__main__":
    r = Retriever()
    print(f"[retriever] {r.count:,} chunks")
    for hit in r.search("How is long-term capital gain on listed shares taxed?", top_k=3):
        print(f"\n[{hit['doc']} p.{hit['page']} {hit['fy_tag']} score={hit['score']}]")
        print(hit["text"][:220])
