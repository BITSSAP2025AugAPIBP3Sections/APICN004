# Provider Comparison — APICN004

Cost, latency, and accuracy for the same three questions (one per difficulty tier) run
through the shared RAG pipeline. **Only the local SLM rows are measured on this machine.**
The Groq rows are **projections** (see the methodology note) — we did not have a Groq API
key, so those numbers are estimated from Groq's published throughput and pricing, not from a
live run. They are included to illustrate the hosted-vs-local trade-off.

- Hardware (local): Apple M3 Pro, 36 GB RAM.
- Token counts are the provider's own reported usage (local) or the measured prompt sizes
  reused for the projection (Groq).

## Measured — Local SLM (Ollama, `qwen2.5:3b`, self-hosted)

| Tier | Latency (ms) | Prompt tok | Completion tok | Total tok | Cost (USD) |
|------|-------------:|-----------:|---------------:|----------:|-----------:|
| Easy | 4,010 | 1,708 | 118 | 1,826 | $0.000000 |
| Medium | 7,712 | 1,621 | 326 | 1,947 | $0.000000 |
| Complex | 34,725 | 1,611 | 1,800 | 3,411 | $0.000000 |

## Projected — Groq (`llama-3.3-70b-versatile`) · *estimated, not run*

> **Projection, not a measurement.** Latency estimated from Groq's published throughput for
> this model (~275 output tokens/s) plus ~0.3 s time-to-first-token / network overhead, applied
> to the measured token counts. Cost uses Groq's published rate of **≈ $0.59 / 1M input tokens**
> and **≈ $0.79 / 1M output tokens** (verify the current figure at groq.com/pricing). Actual
> results will vary with load and tokenizer differences.

| Tier | Latency (ms) | Prompt tok | Completion tok | Total tok | Cost (USD) |
|------|-------------:|-----------:|---------------:|----------:|-----------:|
| Easy | ~730 | 1,708 | 118 | 1,826 | ~$0.001101 |
| Medium | ~1,490 | 1,621 | 326 | 1,947 | ~$0.001214 |
| Complex | ~6,850 | 1,611 | 1,800 | 3,411 | ~$0.002372 |

## Averages per request

| Provider | Avg latency | Avg total tokens | Avg cost (USD) | Source |
|----------|------------:|-----------------:|---------------:|--------|
| Local SLM (`qwen2.5:3b`) | ~15,500 ms | 2,395 | **$0.000000** | measured |
| Groq (`llama-3.3-70b-versatile`) | ~3,000 ms | 2,395 | **~$0.001562** | projected |

## Accuracy

Accuracy is judged on the 13-question official bank via `python tests/run_eval.py`; the
"Correct?" column is completed by human review against the answer key.

- **Local SLM (`qwen2.5:3b`)** — measured. Reliable on fact-lookup questions (80C limit,
  standard deduction, slab rates, VDA provisions) with correct `doc p.page` citations. Weaker on
  the longest multi-step arithmetic (Q-C01/Q-C03), where slab-by-slab surcharge/cess chains can
  slip.
- **Groq `llama-3.3-70b-versatile`** — *not run.* A 70B model is expected to handle the complex
  multi-step calculations more reliably than a 3B local model; this is a projection based on
  model size, not a measured result on this corpus.

## How to replace the projection with a real measurement

```bash
GROQ_API_KEY=... python tests/compare_providers.py   # regenerates the measured Groq rows
GROQ_API_KEY=... LLM_PROVIDER=groq LLM_MODEL=llama-3.3-70b-versatile python tests/run_eval.py
```

Set Groq's current input/output prices in the `PRICING` table in
`tests/compare_providers.py` so the cost column is exact.
