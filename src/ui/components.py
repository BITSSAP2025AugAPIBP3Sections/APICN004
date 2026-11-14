"""Small Streamlit presentation helpers for the APICN004 app.

Kept separate from app.py so the interaction logic stays readable and the helpers
can be unit-tested without spinning up Streamlit.
"""
from __future__ import annotations

import re

MODES = {
    "TITO": ("text", "text"),
    "TIVO": ("text", "voice"),
    "VITO": ("voice", "text"),
    "VIVO": ("voice", "voice"),
}

MODE_HELP = {
    "TITO": "Type a question → read the answer.",
    "TIVO": "Type a question → hear the answer.",
    "VITO": "Speak a question → read the answer.",
    "VIVO": "Speak a question → hear the answer.",
}

_FRAC = re.compile(r"\\[dt]?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}")
_TEXT = re.compile(r"\\text(?:bf|it|rm)?\s*\{([^{}]*)\}")
_MATHOP = {
    r"\times": "×", r"\cdot": "·", r"\div": "÷", r"\pm": "±",
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠", r"\approx": "≈",
    r"\%": "%", r"\,": " ", r"\;": " ", r"\!": "", r"\quad": "  ",
    r"\left": "", r"\right": "", r"\\": " ",
}


def latex_to_text(text: str) -> str:
    """Convert LaTeX math markup to clean readable text, keeping normal markdown.

    The model is told not to emit LaTeX, but when it does (\\[ \\], \\frac, \\text …)
    Streamlit renders it literally. This turns it into plain arithmetic so formulas
    read naturally on screen without KaTeX parse risks.
    """
    t = text
    # Unwrap block / inline math delimiters: \[ \]  \( \)  $$ $$  $ $
    t = re.sub(r"\\\[|\\\]|\\\(|\\\)", " ", t)
    t = re.sub(r"\${1,2}", " ", t)
    # \text{...} first so nested braces inside \frac are already gone.
    for _ in range(3):
        t = _TEXT.sub(r"\1", t)
    # \frac{a}{b} -> (a / b); run twice for simple nesting.
    for _ in range(2):
        t = _FRAC.sub(r"(\1 / \2)", t)
    # Common operators / spacing commands.
    for k, v in _MATHOP.items():
        t = t.replace(k, v)
    # Any remaining \command -> drop the backslash; strip leftover math braces.
    t = re.sub(r"\\([a-zA-Z]+)", r"\1", t)
    t = re.sub(r"(?<!\|)[{}]", "", t)
    # Collapse doubled parens from \left( \frac … \right) and squeeze spaces.
    t = re.sub(r"\(\s*\(", "(", t)
    t = re.sub(r"\)\s*\)", ")", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"[ \t]+([.,;:)])", r"\1", t)
    return t


def mode_io(mode: str) -> tuple[str, str]:
    """Return (input_kind, output_kind) for a mode name, e.g. ('voice', 'text')."""
    return MODES[mode]


def format_sources(sources: list[dict]) -> str:
    """Render deduped citations as a compact markdown string."""
    if not sources:
        return "_No sources retrieved._"
    seen: list[tuple] = []
    for s in sources:
        key = (s["doc"], s["page"])
        if key not in seen:
            seen.append(key)
    return "\n".join(f"- `{doc}` — p.{page}" for doc, page in seen)


def to_llm_history(history: list[dict], max_turns: int = 4) -> list[dict]:
    """Convert UI chat history to the role/content list the LLM expects (last N turns)."""
    msgs: list[dict] = []
    for turn in history[-max_turns * 2:]:
        if turn["role"] in ("user", "assistant"):
            msgs.append({"role": turn["role"], "content": turn["content"][:1800]})
    return msgs
