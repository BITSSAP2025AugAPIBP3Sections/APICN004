import importlib

import pytest

from src.ui import components as ui


def test_mode_io_map():
    assert ui.mode_io("TITO") == ("text", "text")
    assert ui.mode_io("VIVO") == ("voice", "voice")
    assert ui.mode_io("TIVO") == ("text", "voice")
    assert ui.mode_io("VITO") == ("voice", "text")


def test_format_sources_dedupes():
    md = ui.format_sources([
        {"doc": "a.pdf", "page": 1}, {"doc": "a.pdf", "page": 1}, {"doc": "b.pdf", "page": 2},
    ])
    assert md.count("a.pdf") == 1
    assert "b.pdf" in md


def test_format_sources_empty():
    assert "No sources" in ui.format_sources([])


def test_to_llm_history_limits_turns():
    history = []
    for i in range(10):
        history.append({"role": "user", "content": f"q{i}"})
        history.append({"role": "assistant", "content": f"a{i}"})
    msgs = ui.to_llm_history(history, max_turns=2)
    assert len(msgs) == 4
    assert msgs[0]["content"] == "q8"


@pytest.mark.parametrize("mod", [
    "src.config", "src.rag.embed", "src.rag.ingest", "src.rag.retriever",
    "src.rag.llm", "src.rag.core", "src.speech.stt", "src.speech.tts",
    "src.ui.components",
])
def test_modules_import(mod):
    assert importlib.import_module(mod) is not None
