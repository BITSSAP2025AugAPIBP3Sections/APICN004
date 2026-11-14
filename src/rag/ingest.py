"""Ingestion: read every PDF in DATA_DIR, split into page-anchored chunks, embed them
with a local sentence-transformers model, and store them in a persistent ChromaDB
collection together with a reproducibility manifest.

Run:  python src/rag/ingest.py

Design notes
------------
* Deterministic, word-boundary chunking (no randomness) → reproducible index (bonus).
* Every chunk carries metadata {doc, page, fy_tag} so the retriever can cite the exact
  source page and bias retrieval toward the financial year named in a question.
* The collection is rebuilt from scratch each run (idempotent) and a manifest.json is
  written describing exactly what produced the index.
"""
from __future__ import annotations

import json
import re
import sys
import time
from pathlib import Path

# Make `src.*` importable when run directly as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src import config  # noqa: E402
from src.rag import embed  # noqa: E402

# Corpus whose presence we expect for the full official test bank. Ingestion still
# runs with a subset (useful while PDFs are being assembled), but warns about gaps.
EXPECTED_CORPUS: tuple[str, ...] = (
    "Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf",
    "E-Book-Guidance-Note-Crypto-Asset-Reporting-Obligations.pdf",
    "FAQs-on-BIS-Exemption.pdf",
    "FAQs-on-FIIs-Exemption.pdf",
    "FAQs-on-Transition-Provisions.pdf",
    "Updated-FQAs-on-Interplay&Transitions.pdf",
    "bs202223.pdf",
    "bs2023_24.pdf",
    "bs2024_25(I).pdf",
    "bs2024_25.pdf",
    "bs2025_26.pdf",
)

_YEAR_PAIR = re.compile(r"(20\d{2})[^\d]?(\d{2})")


def fy_tag_for(filename: str) -> str:
    """Derive a financial-year tag from a budget-speech filename.

    bs202223.pdf -> 'FY2022-23', bs2024_25(I).pdf -> 'FY2024-25'.
    Non-budget documents (the Act, FAQs, crypto guidance) are tagged 'general'.
    """
    stem = filename.lower()
    if stem.startswith("bs"):
        m = _YEAR_PAIR.search(filename)
        if m:
            return f"FY{m.group(1)}-{m.group(2)}"
    return "general"


def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """Split normalised text into ~`size`-char chunks on word boundaries with overlap."""
    text = " ".join(text.split())
    if not text:
        return []
    chunks: list[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + size, n)
        if end < n:
            boundary = text.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        next_start = max(start + 1, end - overlap)
        space = text.find(" ", next_start, end)
        start = space + 1 if space != -1 else next_start
    return chunks


def iter_pages(path: Path):
    """Yield (page_no, text) for each page of a PDF using PyMuPDF (1-indexed)."""
    import pymupdf

    doc = pymupdf.open(str(path))
    try:
        for page_no, page in enumerate(doc, start=1):
            try:
                yield page_no, page.get_text() or ""
            except Exception as exc:  # noqa: BLE001
                print(f"  WARNING: {path.name} p{page_no}: {exc}", file=sys.stderr)
                yield page_no, ""
    finally:
        doc.close()


def build_records(pdf_paths: list[Path], size: int, overlap: int):
    """Return (records, per_doc_counts). Each record is a dict with text + metadata."""
    records: list[dict] = []
    per_doc: dict[str, dict] = {}
    for pdf in pdf_paths:
        tag = fy_tag_for(pdf.name)
        pages = 0
        before = len(records)
        for page_no, text in iter_pages(pdf):
            pages += 1
            for chunk in chunk_text(text, size, overlap):
                records.append(
                    {"text": chunk, "doc": pdf.name, "page": page_no, "fy_tag": tag}
                )
        per_doc[pdf.name] = {"pages": pages, "chunks": len(records) - before, "fy_tag": tag}
        print(f"  {pdf.name}: {pages} pages, {len(records) - before} chunks  [{tag}]")
    return records, per_doc


def ingest() -> dict:
    data = config.data_dir()
    index = config.index_dir()
    size, overlap = config.chunk_size(), config.chunk_overlap()

    if overlap >= size:
        raise ValueError(f"CHUNK_OVERLAP ({overlap}) must be < CHUNK_SIZE ({size})")
    if not data.exists():
        raise RuntimeError(f"DATA_DIR does not exist: {data}")

    pdf_paths = sorted(data.glob("*.pdf"))
    if not pdf_paths:
        raise RuntimeError(f"No PDFs found in {data}")

    present = {p.name for p in pdf_paths}
    missing = [n for n in EXPECTED_CORPUS if n not in present]
    if missing:
        print(
            "  NOTE: building index WITHOUT these expected corpus files "
            "(some official questions may be unanswerable until they are added):",
            file=sys.stderr,
        )
        for n in missing:
            print(f"    - {n}", file=sys.stderr)

    t0 = time.time()
    print(f"Reading {len(pdf_paths)} PDF(s) from {data} ...")
    records, per_doc = build_records(pdf_paths, size, overlap)
    if not records:
        raise RuntimeError("No chunks produced from the corpus.")

    model_name = config.embed_model()
    print(f"\nEmbedding {len(records)} chunks with {model_name} ...")
    vectors = embed.embed_texts([r["text"] for r in records])
    dim = len(vectors[0])

    # Build the collection fresh (atomic from the reader's perspective: we drop and
    # recreate, then add everything in one pass before writing the manifest).
    index.mkdir(parents=True, exist_ok=True)
    import chromadb

    client = chromadb.PersistentClient(path=str(index))
    name = config.collection_name()
    try:
        client.delete_collection(name)
    except Exception:  # noqa: BLE001  (collection may not exist yet)
        pass
    coll = client.create_collection(name, metadata={"hnsw:space": "cosine"})

    batch = 5000  # ChromaDB add batch cap
    for i in range(0, len(records), batch):
        sl = slice(i, i + batch)
        coll.add(
            ids=[f"{r['doc']}::p{r['page']}::c{j}" for j, r in enumerate(records[sl], start=i)],
            documents=[r["text"] for r in records[sl]],
            metadatas=[{"doc": r["doc"], "page": r["page"], "fy_tag": r["fy_tag"]} for r in records[sl]],
            embeddings=vectors[sl],
        )

    elapsed = time.time() - t0
    manifest = {
        "collection": name,
        "embed_model": model_name,
        "embed_dim": dim,
        "chunk_size": size,
        "chunk_overlap": overlap,
        "num_chunks": len(records),
        "num_docs": len(pdf_paths),
        "documents": per_doc,
        "expected_missing": missing,
        "build_seconds": round(elapsed, 1),
    }
    (index / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("\n=== Ingestion complete ===")
    print(f"  Documents:   {len(pdf_paths)}")
    print(f"  Chunks:      {len(records)}")
    print(f"  Dimensions:  {dim}")
    print(f"  Index dir:   {index}")
    print(f"  Time:        {elapsed:.1f}s")
    if missing:
        print(f"  Missing expected PDFs: {len(missing)} (see warning above)")
    return manifest


if __name__ == "__main__":
    try:
        ingest()
    except (ValueError, RuntimeError) as exc:
        print(f"FATAL: {exc}", file=sys.stderr)
        sys.exit(1)
