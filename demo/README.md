# VIVO demo recordings

Seven end-to-end **VIVO** (voice-in, voice-out) audio demonstrations, `vivo_1.mp3`
through `vivo_7.mp3`, mapped to the official VIVO recording map.

> **Note:** The audio is synthesized using `edge-tts` (en-IN-NeerjaNeural voice) for both
> the question and the answer — the same TTS engine the live app uses for voice output.
> The question text is the official question and the answer comes directly from the live
> RAG pipeline (ChromaDB retrieval → open-source SLM via Ollama). `vivo_7.mp3` includes
> a multi-turn follow-up demonstrating conversation history.

| File | Question | Multi-turn? |
|------|----------|-------------|
| `vivo_1.mp3` | Q-E01 — new-regime slab rates FY 2024-25 | No |
| `vivo_2.mp3` | Q-E02 — Section 80C limit + investments | No |
| `vivo_3.mp3` | Q-E05 — LTCG on listed equity | No |
| `vivo_4.mp3` | Q-M01 — tax on ₹18 lakh (new regime) | No |
| `vivo_5.mp3` | Q-M04 — crypto / VDA under 115BBH + 194S | No |
| `vivo_6.mp3` | Q-C01 — both regimes with surcharge & cess | No |
| `vivo_7.mp3` | Q-C03 — residential status + RNOR, then follow-up on ROR tax | **Yes** |
