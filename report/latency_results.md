# Latency Results — APICN004

Configuration tested: `LLM_PROVIDER=slm`, `LLM_MODEL=qwen2.5:3b` (Ollama, open-source),
embeddings `all-MiniLM-L6-v2`, STT `faster-whisper(base)`, TTS `edge-tts (en-IN-NeerjaNeural)`.  
Hardware: Apple M3 Pro MacBook Pro, 36 GB RAM.

> Measurements taken with a warm model cache (embedding model and retriever loaded once
> per process). Each LLM / TITO figure is the mean of 3 runs. STT figures are estimated
> from faster-whisper base-model benchmarks on M3 (≈5-second spoken question).
> TTS figures are measured from live edge-tts calls. The local SLM runs entirely on-device,
> so the full-answer time scales with answer length and the machine's CPU/GPU.

## Timings (mean of 3 runs)

| Metric | Easy (Q-E02) | Medium (Q-M01) | Complex (Q-C01) |
|--------|--------------|----------------|-----------------|
| Query embedding (ms) | 34 | 39 | 51 |
| Retrieval (ms) | 1 | 6 | 1 |
| LLM full answer (ms) | 2 155 | 7 656 | 27 527 |
| TITO total (ms) | 2 190 | 7 701 | 27 579 |
| STT transcription (ms) | ~300 | ~300 | ~300 |
| TTS first-audio (ms) | 1 195 | ~2 000 | ~2 000 |
| VIVO end-to-end: question spoken → answer audible (ms) | ~3 700 | ~4 500 | ~4 600 |

> VIVO end-to-end = STT + embed + retrieval + first streamed tokens + TTS first-chunk.
> The full spoken answer continues after that; first-audio is what sets perceived latency.

## Optimisations attempted

| # | Optimisation | Baseline | After | Effect |
|---|--------------|----------|-------|--------|
| 1 | **Streaming LLM output** — tokens rendered as they arrive rather than waiting for the full completion. | full-completion wait (~27 s for complex) | first tokens in ~1–2 s | User sees text far sooner; perceived latency drops sharply for long answers |
| 2 | **Sentence-group streaming TTS** — answer synthesised in ~2-sentence groups so audio begins before the whole answer is synthesised. | whole-answer synthesis | first group in ~1.2 s | Time-to-first-audio ↓ ~6× |
| 3 | **Warm model caches** — embedding model and faster-whisper model loaded once per process and reused across turns. | cold load each turn (~8 s first call) | ~40 ms after first turn | Eliminates repeated model-load cost; warm embed is 34–51 ms vs ~8 000 ms cold |
| 4 | **`max_tokens` tuning** — raised from 900 to 1 800 tokens so complex multi-step calculations complete without truncation; no latency impact on short questions. | truncated answers for Q-C01 | full answers for all 13 questions | Correctness ↑ with no regression on short questions |
