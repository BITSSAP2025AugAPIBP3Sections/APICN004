from src.speech import tts
from src.speech import stt


def test_sentence_groups_pairs():
    text = "One. Two. Three. Four."
    groups = tts.sentence_groups(text, per_group=2)
    assert groups == ["One. Two.", "Three. Four."]


def test_sentence_groups_with_tail():
    groups = tts.sentence_groups("First sentence. A trailing clause", per_group=1)
    assert groups[0] == "First sentence."
    assert "trailing clause" in groups[-1]


def test_sentence_groups_empty():
    assert tts.sentence_groups("") == []


def test_audio_mime_edge(monkeypatch):
    monkeypatch.setenv("TTS_PROVIDER", "edge")
    assert tts.audio_mime() == "audio/mp3"


def test_audio_mime_piper(monkeypatch):
    monkeypatch.setenv("TTS_PROVIDER", "piper")
    assert tts.audio_mime() == "audio/wav"


def test_synthesize_empty_returns_empty():
    assert tts.synthesize("   ") == b""


def test_transcribe_none_path():
    assert stt.transcribe(None) is None


def test_transcribe_bytes_none():
    assert stt.transcribe_bytes(None) is None
