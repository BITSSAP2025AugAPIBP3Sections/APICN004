"""Central configuration for APICN004.

All tunables are read from the environment (loaded from `.env`). Values are read
at call time via small accessor functions so tests can monkeypatch the environment
without re-importing modules.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the repo root (two levels up from this file: src/ -> repo root).
_REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_REPO_ROOT / ".env")

REPO_ROOT = _REPO_ROOT


def _get(name: str, default: str) -> str:
    val = os.getenv(name)
    return val if val not in (None, "") else default


def data_dir() -> Path:
    return (REPO_ROOT / _get("DATA_DIR", "data")).resolve()


def index_dir() -> Path:
    return (REPO_ROOT / _get("INDEX_DIR", "index")).resolve()


def collection_name() -> str:
    return _get("COLLECTION", "income_tax")


def embed_model() -> str:
    return _get("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


def embed_batch() -> int:
    return int(_get("EMBED_BATCH", "64"))


def chunk_size() -> int:
    return int(_get("CHUNK_SIZE", "900"))


def chunk_overlap() -> int:
    return int(_get("CHUNK_OVERLAP", "150"))


def top_k() -> int:
    return int(_get("TOP_K", "6"))


def show_timing() -> bool:
    return _get("SHOW_TIMING", "0") not in ("0", "false", "False", "")
