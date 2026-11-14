"""Text-to-speech. Converts a generated answer into audio.

Providers (TTS_PROVIDER): `edge` (edge-tts, default — pure-python, no binary) | `piper`.

`synthesize()` returns audio bytes for Streamlit's `st.audio`. `synthesize_stream()`
yields audio sentence-group by sentence-group so playback can begin before the whole
answer is synthesised (latency optimisation / bonus). `speak()` plays audio for the CLI.
"""
from __future__ import annotations

import asyncio
import os
import platform
import re
import subprocess
import tempfile
from typing import Iterator

from src import config  # noqa: F401  (ensures .env is loaded)

_SENTENCE = re.compile(r"[^.!?]+[.!?]")

# Markdown / formatting cleanup so TTS never vocalises symbols like "asterisk".
_CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_LATEX = re.compile(r"\\[\[\]()]|\\[a-zA-Z]+|[\\${}]")        # \[ \] \( \) \frac ${} etc.
_HEADER = re.compile(r"^\s{0,3}#{1,6}\s*", re.MULTILINE)       # ### Heading
_BULLET = re.compile(r"^\s*[-*+]\s+", re.MULTILINE)            # - item / * item
_EMPHASIS = re.compile(r"(\*{1,3}|_{1,3}|`+|~{2})")            # **bold** _it_ `code` ~~s~~
_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")                    # [text](url) -> text
_MULTISPACE = re.compile(r"[ \t]{2,}")


def clean_for_speech(text: str) -> str:
    """Strip markdown and math markup so the voice reads words, not symbols."""
    t = _CODE_FENCE.sub(" ", text)
    t = _LINK.sub(r"\1", t)
    t = _HEADER.sub("", t)
    t = _BULLET.sub("", t)
    t = _EMPHASIS.sub("", t)
    t = _LATEX.sub(" ", t)
    t = t.replace("->", " to ").replace("→", " to ").replace("•", " ")
    t = t.replace("|", " ").replace("#", " ")
    t = re.sub(r"\bp\.\s*(\d+)", r"page \1", t)   # "p.32" -> "page 32"
    # Speak arithmetic minus between real amounts (₹ or comma-grouped), so
    # "₹18,00,000 - ₹75,000" is heard as "… minus …", not run together.
    def _say_minus(m: "re.Match") -> str:
        span = m.group(0)
        if "," in span or "₹" in span:
            return re.sub(r"\s*[-−]\s*", " minus ", span)
        return span
    t = re.sub(r"[₹\d][\d,]*\s*[-−]\s*₹?\s*[\d,]*\d", _say_minus, t)
    # Give every non-empty line a sentence end so the voice PAUSES between lines
    # (e.g. slab rows) instead of running numbers together ("12,500 5,00,001").
    lines = []
    for raw in t.split("\n"):
        ln = raw.strip()
        if not ln:
            continue
        if ln[-1] not in ".!?:;,":
            ln += "."
        lines.append(ln)
    t = " ".join(lines)
    t = _MULTISPACE.sub(" ", t)
    t = re.sub(r"\s+([.,;:!?])", r"\1", t)        # no space before punctuation
    t = re.sub(r"([.,;:]){2,}", r"\1", t)         # collapse repeats like ".."
    return t.strip()


def sentence_groups(text: str, per_group: int = 2) -> list[str]:
    """Split text into groups of ~`per_group` sentences for incremental synthesis."""
    parts = [p.strip() for p in _SENTENCE.findall(text) if p.strip()]
    tail = text[len("".join(_SENTENCE.findall(text))):].strip()
    if tail:
        parts.append(tail)
    if not parts:
        return [text] if text.strip() else []
    return [" ".join(parts[i:i + per_group]) for i in range(0, len(parts), per_group)]


def _edge_bytes(text: str) -> bytes:
    import edge_tts

    voice = os.getenv("TTS_VOICE") or "en-IN-NeerjaNeural"
    rate = os.getenv("TTS_RATE", "+0%")

    async def run() -> bytes:
        chunks: list[bytes] = []
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                chunks.append(chunk["data"])
        return b"".join(chunks)

    return asyncio.run(run())


def _piper_bytes(text: str) -> bytes:
    model = os.getenv("TTS_VOICE", "")
    if not model:
        raise RuntimeError("TTS_PROVIDER=piper requires TTS_VOICE to point at a .onnx model")
    fd, out = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        proc = subprocess.run(
            ["piper", "--model", model, "--output_file", out],
            input=text.encode("utf-8"),
            check=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"piper exited with {proc.returncode}")
        with open(out, "rb") as fh:
            return fh.read()
    finally:
        try:
            os.unlink(out)
        except OSError:
            pass


def synthesize(text: str) -> bytes:
    """Synthesise the whole answer and return audio bytes (mp3 for edge, wav for piper)."""
    provider = os.getenv("TTS_PROVIDER", "edge").strip().lower()
    spoken = clean_for_speech(text)
    if not spoken.strip():
        return b""
    return {"edge": _edge_bytes, "piper": _piper_bytes}[provider](spoken)


def synthesize_stream(text: str, per_group: int = 2) -> Iterator[bytes]:
    """Yield audio bytes per sentence-group so playback can start early."""
    for group in sentence_groups(clean_for_speech(text), per_group):
        audio = synthesize(group)
        if audio:
            yield audio


def audio_mime() -> str:
    return "audio/wav" if os.getenv("TTS_PROVIDER", "edge").lower() == "piper" else "audio/mp3"


def _play(audio_bytes: bytes, mime: str) -> None:
    suffix = ".wav" if "wav" in mime else ".mp3"
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    try:
        with open(path, "wb") as fh:
            fh.write(audio_bytes)
        system = platform.system().lower()
        if system == "darwin":
            subprocess.run(["afplay", path], check=False)
        elif system == "windows":
            subprocess.run(["cmd", "/c", "start", "", path], check=False)
        else:
            subprocess.run(["aplay", path], check=False)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


def speak(text: str) -> None:
    """CLI helper: synthesise sentence-group by sentence-group and play immediately."""
    mime = audio_mime()
    for audio in synthesize_stream(text):
        _play(audio, mime)
