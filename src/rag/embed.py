"""Shared embedding model — a single cached SentenceTransformer used by both the
ingestion pipeline and the retriever, so the model is loaded at most once per process.

Embeddings are L2-normalised, which makes cosine similarity equivalent to a dot product
and keeps ingest/query vectors consistent with the ChromaDB `cosine` space.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Sequence

from src import config


@lru_cache(maxsize=4)
def _load(model_name: str):
    # Imported lazily so that importing this module (e.g. in unit tests that
    # monkeypatch embed_texts) does not require torch to be installed.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name)


def get_model(model_name: str | None = None):
    return _load(model_name or config.embed_model())


def embed_texts(texts: Sequence[str], batch_size: int | None = None) -> list[list[float]]:
    """Return L2-normalised embeddings for a batch of documents."""
    model = get_model()
    vecs = model.encode(
        list(texts),
        batch_size=batch_size or config.embed_batch(),
        normalize_embeddings=True,
        show_progress_bar=False,
        convert_to_numpy=True,
    )
    return vecs.tolist()


def embed_query(text: str) -> list[float]:
    """Return a single L2-normalised query embedding."""
    model = get_model()
    vec = model.encode(
        [text], normalize_embeddings=True, show_progress_bar=False, convert_to_numpy=True
    )[0]
    return vec.tolist()


def embed_dim() -> int:
    return int(get_model().get_sentence_embedding_dimension())
