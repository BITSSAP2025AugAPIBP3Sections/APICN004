# Limitations — APICN004

## Corpus & coverage
- Answers are only as complete as the PDFs in `data/`. If a budget speech, FAQ, or the full
  Income-tax Act is missing at ingestion time, questions depending on it may return
  "I could not find this in the provided corpus." Ingestion warns about missing expected files.
- Scanned/image-only pages yield no text under PyMuPDF (no OCR). The official corpus is
  text-based, so this mainly affects stray scanned inserts.

## Retrieval
- Chunking is character-based with overlap, not semantically aware; a provision split across a
  chunk boundary can be partially retrieved. Larger `TOP_K` mitigates this at a latency cost.
- Year biasing keys off an FY/AY *explicitly stated in the question*. A question that implies a
  year only through context (e.g. "this year") is not disambiguated.
- `all-MiniLM-L6-v2` is small and fast but less precise than larger embedding models; dense
  legal phrasing can retrieve near-miss sections.

## Generation
- The model can still misread retrieved context, especially multi-step tax computations
  (surcharge thresholds, marginal relief, cess). Numeric answers should be verified against the
  official answer key — the system grounds and cites but does not independently recompute.
- Grounding is enforced by prompt, not by hard constraint; a determined model can still phrase
  outside-corpus knowledge. Citations, however, are rendered from retrieval metadata and are
  trustworthy even if prose drifts.
- Default local SLM (`qwen2.5:3b`) is weaker at long multi-step arithmetic than the hosted
  models; for the complex questions (Q-C01…Q-C03) a larger model (Groq 70B) gives better working.

## Speech
- `faster-whisper` transcription quality drops on heavy accents, fast speech, or noisy mics, and
  may mis-hear figures (e.g. "lakh" vs "lack"); the transcript is shown so the user can retry.
- `edge-tts` requires network access to Microsoft voices; fully-offline speech needs `piper`
  with a local voice model.
- Long answers take longer to synthesise; sentence-group streaming reduces time-to-first-audio
  but total speech time still scales with answer length.

## Operational
- First run downloads the embedding model and (for local STT) the Whisper model.
- Python 3.11 is required; the ML/audio wheels are not yet available for 3.14.
- The ChromaDB index and `.env` are gitignored; a fresh clone must run ingestion and provide keys.
