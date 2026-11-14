# Submission — APICN004

- **Team ID:** APICN004
- **GitHub repository:** https://github.com/BITSSAP2025AugAPIBP3Sections/APICN004
- **App entry point:** `streamlit run src/app.py` (web UI) · `python src/app.py --mode tito --question "..."` (headless CLI)
- **One-shot TITO (CLI):** `python src/app.py --mode tito --question "<question>"` (or `python src/rag/core.py "<question>"`)
- **Default provider:** open-source SLM — Ollama + `qwen2.5:3b` (Apache-2.0); `.env` fallback to Groq / OpenAI / Anthropic / OpenRouter
- **STT engine:** faster-whisper (`base`, local default); Groq / OpenAI Whisper API options
- **TTS engine:** edge-tts (`en-IN-NeerjaNeural`, sentence-group streaming); piper option

## Team

| Member | ID | Email | Role |
|--------|----|-------|------|
| Nilay Shekhar | 2023SL70011 | 2023sl70011@wilp.bits-pilani.ac.in | RAG pipeline (ingestion, retrieval, year-aware biasing), LLM integration |
| Prerana Maktal | 2023SL70016 | 2023sl70016@wilp.bits-pilani.ac.in | Speech modules (STT/TTS), Streamlit UI & four interaction modes |
| Pravalika Bachu | 2023SL70017 | 2023sl70017@wilp.bits-pilani.ac.in | Evaluation harness, latency measurements, documentation |

## Stack

- **Default LLM:** open-source SLM via Ollama (`qwen2.5:3b`, Apache-2.0, OpenAI-compatible
  endpoint). Multi-provider switch also supports Groq / OpenAI / Anthropic / OpenRouter.
  Developed and evaluated on the local open-source SLM (13-question eval, latency measurements).
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` (local, offline, 384-dim).
- **Vector store:** ChromaDB persistent collection (cosine), with `{doc, page, fy_tag}` metadata.
- **STT:** faster-whisper (local default); Groq / OpenAI Whisper API options.
- **TTS:** edge-tts (default); piper option. Sentence-group streaming for early audio.
- **Frontend:** Streamlit — one screen drives all four modes over one RAG pipeline.

## Feature completion

- **TITO** — typed question → retrieval → grounded, cited answer.
- **TIVO** — TITO + edge-tts speech output.
- **VITO** — microphone → faster-whisper transcription → TITO.
- **VIVO** — VITO + TIVO, with multi-turn conversation history in session.
- **RAG** — ChromaDB cosine retrieval; year-aware biasing (FY/AY in the question steers
  retrieval toward that budget's provisions); per-chunk `doc`/`page` citations.
- **Reproducible ingestion** — deterministic chunking + `index/manifest.json` recording the
  embedding model, dimensions, chunk params, and per-document chunk counts.
- **Tests** — offline unit suite (chunking, FY detection, provider selection, SSE parsing,
  pipeline orchestration, source dedup, speech helpers, module imports).

## External data used

- None beyond the official corpus in `data/` (Income-tax Act, Union Budget speeches, and
  government FAQs). The Income-tax Act PDF is distributed via a GitHub Release due to size.

## AI coding assistant disclosure

- **Claude Code (Anthropic, `claude-opus-4-8`)** — used to scaffold the repository, author the
  RAG pipeline (ingestion, ChromaDB retrieval with year-aware biasing, multi-provider streaming
  LLM layer, shared `core` pipeline), the Streamlit four-mode UI, the speech modules, the unit
  test suite, the evaluation harness, and this documentation. All code was reviewed and tested
  by the team.

## Bonuses attempted

- **Streaming TTS** — answer synthesised sentence-group by sentence-group so audio starts early.
- **Multi-turn VIVO** — prior turns are carried into the prompt; follow-up questions supported.
- **Reproducible ingestion** — deterministic chunking + manifest.

## One-line claim to fame

A single Streamlit RAG app serving all four interaction modes over one ChromaDB pipeline, with
year-aware retrieval for year-sensitive tax questions, swappable LLM/STT/TTS providers, grounded
citations, and streaming answer + speech.
