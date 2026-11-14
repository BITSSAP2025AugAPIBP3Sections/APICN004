"""Speech-to-text. Turns recorded audio (a file path or raw bytes from Streamlit's
`st.audio_input`) into text, then feeds it to the same RAG pipeline the typed modes use.

Providers (STT_PROVIDER): `local` (faster-whisper, default, offline) | `groq` | `openai`.
"""
from __future__ import annotations

import os
import tempfile
import time

import requests

from src import config  # noqa: F401  (ensures .env is loaded)

_model = None  # cached faster-whisper model (loaded once)


def _faster_whisper(wav_path: str) -> str:
    from faster_whisper import WhisperModel

    global _model
    if _model is None:
        _model = WhisperModel(os.getenv("STT_MODEL", "base"), device="auto", compute_type="auto")
    segments, _info = _model.transcribe(wav_path)
    return " ".join(s.text for s in segments).strip()


def _api_whisper(provider: str, wav_path: str) -> str:
    key_var = "GROQ_API_KEY" if provider == "groq" else "OPENAI_API_KEY"
    api_key = os.getenv(key_var, "")
    if not api_key:
        raise RuntimeError(f"STT_PROVIDER={provider} requires {key_var}")
    url = (
        "https://api.groq.com/openai/v1/audio/transcriptions"
        if provider == "groq"
        else "https://api.openai.com/v1/audio/transcriptions"
    )
    model = "whisper-large-v3-turbo" if provider == "groq" else "whisper-1"
    for attempt in range(2):
        try:
            with open(wav_path, "rb") as fh:
                resp = requests.post(
                    url,
                    headers={"Authorization": f"Bearer {api_key}"},
                    files={"file": fh},
                    data={"model": model},
                    timeout=120,
                )
            if resp.status_code == 429 or resp.status_code >= 500:
                if attempt == 0:
                    time.sleep(2)
                    continue
            resp.raise_for_status()
            text = resp.json().get("text")
            if text is None:
                raise ValueError(f"STT API ({provider}) unexpected response: {resp.json()}")
            return text.strip()
        except (requests.ConnectionError, requests.Timeout):
            if attempt == 0:
                time.sleep(2)
                continue
            raise
    return ""


def transcribe(wav_path: str | None) -> str | None:
    """Transcribe a WAV file path. Returns None for a missing path."""
    if not wav_path:
        return None
    provider = os.getenv("STT_PROVIDER", "local").strip().lower()
    try:
        if provider in ("groq", "openai"):
            return _api_whisper(provider, wav_path)
        return _faster_whisper(wav_path)
    finally:
        # Only clean up temp files we created (see transcribe_bytes).
        pass


def transcribe_bytes(audio_bytes: bytes | None, suffix: str = ".wav") -> str | None:
    """Transcribe raw audio bytes (e.g. from Streamlit's st.audio_input)."""
    if not audio_bytes:
        return None
    tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    try:
        tmp.write(audio_bytes)
        tmp.close()
        return transcribe(tmp.name)
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass
