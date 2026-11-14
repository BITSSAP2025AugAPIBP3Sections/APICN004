from src.rag import core


class _FakeRetriever:
    def __init__(self, hits):
        self._hits = hits
        self._t_embed_ms = 1.0
        self._t_search_ms = 2.0

    def search(self, query, top_k=None):
        return self._hits


HITS = [
    {"text": "Section 80C allows up to 1,50,000.", "doc": "act.pdf", "page": 10, "fy_tag": "general", "score": 0.9},
    {"text": "Eligible: PPF, ELSS, LIC.", "doc": "act.pdf", "page": 10, "fy_tag": "general", "score": 0.8},
    {"text": "Slabs for new regime.", "doc": "bs2024_25.pdf", "page": 3, "fy_tag": "FY2024-25", "score": 0.7},
]


def test_dedupe_sources_collapses_doc_page():
    src = core.dedupe_sources(HITS)
    assert len(src) == 2
    assert src[0] == {"doc": "act.pdf", "page": 10, "fy_tag": "general"}


def test_build_context_includes_source_markers():
    ctx = core.build_context(HITS)
    assert "[source: act.pdf p.10]" in ctx
    assert "[source: bs2024_25.pdf p.3]" in ctx


def test_format_sources():
    assert core.format_sources(core.dedupe_sources(HITS)) == "act.pdf p.10; bs2024_25.pdf p.3"


def test_answer_question_uses_pipeline(monkeypatch):
    monkeypatch.setattr(core, "get_retriever", lambda: _FakeRetriever(HITS))
    monkeypatch.setattr(core.llm, "chat", lambda q, ctx, hist=None: f"answer::{len(ctx)}")
    res = core.answer_question("What is 80C?")
    assert res["answer"].startswith("answer::")
    assert res["sources"] == core.dedupe_sources(HITS)
    assert set(res["timings"]) == {"embed_ms", "search_ms", "retrieve_ms", "llm_ms", "total_ms"}


def test_stream_answer_returns_sources_and_gen(monkeypatch):
    monkeypatch.setattr(core, "get_retriever", lambda: _FakeRetriever(HITS))
    monkeypatch.setattr(core.llm, "stream_chat", lambda q, ctx, hist=None: iter(["x", "y"]))
    sources, gen = core.stream_answer("q")
    assert sources == core.dedupe_sources(HITS)
    assert "".join(gen) == "xy"
