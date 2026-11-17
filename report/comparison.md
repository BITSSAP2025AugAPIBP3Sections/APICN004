# Provider Comparison — APICN004

Same three questions through the shared RAG pipeline; token usage is the
provider's own reported count. Cost = prompt·$/1M-in + completion·$/1M-out.

| Provider | Model | Tier | Latency (ms) | Prompt tok | Completion tok | Total tok | Cost (USD) |
|----------|-------|------|-------------:|-----------:|---------------:|----------:|-----------:|
| Local SLM (Ollama) | qwen2.5:3b | Easy | 4,010 | 1708 | 118 | 1826 | $0.000000 |
| Local SLM (Ollama) | qwen2.5:3b | Medium | 7,712 | 1621 | 326 | 1947 | $0.000000 |
| Local SLM (Ollama) | qwen2.5:3b | Complex | 34,725 | 1611 | 1800 | 3411 | $0.000000 |

## Averages per request

| Provider | Avg latency (ms) | Avg total tokens | Avg cost (USD) |
|----------|-----------------:|-----------------:|---------------:|
| Local SLM (Ollama) | 15,482 | 2,395 | $0.000000 |
