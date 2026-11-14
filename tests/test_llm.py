import json

import pytest

from src.rag import llm


def test_resolve_defaults(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.setenv("GROQ_API_KEY", "k")
    provider, model, key = llm.resolve()
    assert provider == "groq"
    assert model == "llama-3.3-70b-versatile"
    assert key == "k"


def test_resolve_explicit_model(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "slm")
    monkeypatch.setenv("LLM_MODEL", "qwen2.5:7b")
    provider, model, _ = llm.resolve()
    assert (provider, model) == ("slm", "qwen2.5:7b")


def test_resolve_unknown_provider(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "nope")
    with pytest.raises(SystemExit):
        llm.resolve()


def test_build_messages_order_and_grounding():
    msgs = llm.build_messages("Q?", "CTX", [{"role": "user", "content": "prev"}])
    assert msgs[0]["role"] == "system"
    assert "ONLY" in msgs[0]["content"]
    assert msgs[1] == {"role": "user", "content": "prev"}
    assert msgs[-1]["content"].endswith("Question: Q?")
    assert "CTX" in msgs[-1]["content"]


class _FakeResp:
    def __init__(self, lines):
        self._lines = lines

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def raise_for_status(self):
        pass

    def iter_lines(self, decode_unicode=True):
        yield from self._lines


def _sse(content):
    return "data: " + json.dumps({"choices": [{"delta": {"content": content}}]})


def test_stream_openai_parses_deltas(monkeypatch):
    lines = [_sse("Hello "), "", _sse("world"), "data: [DONE]"]
    monkeypatch.setattr(llm.requests, "post", lambda *a, **k: _FakeResp(lines))
    out = list(llm._stream_openai("http://x/v1", "key", "m", []))
    assert "".join(out) == "Hello world"


def test_chat_concatenates(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("GROQ_API_KEY", "k")
    monkeypatch.setattr(llm, "stream_chat", lambda *a, **k: iter(["a", "b", "c"]))
    assert llm.chat("q", "ctx") == "abc"
