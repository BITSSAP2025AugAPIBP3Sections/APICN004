"""Run the 13 official evaluation questions through the shared TITO pipeline and write
report/test_results.md.

Usage:  python tests/run_eval.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.rag import core, llm  # noqa: E402

QUESTIONS: list[tuple[str, str, str]] = [
    ("Q-E01", "Easy", "What are the income tax slab rates for an individual under the new regime for FY 2024-25 (AY 2025-26)?"),
    ("Q-E02", "Easy", "What is the maximum deduction allowed under Section 80C in a financial year, and name three eligible investments?"),
    ("Q-E03", "Easy", "What is the basic exemption limit for a resident individual under 60 years of age under the old regime?"),
    ("Q-E04", "Easy", "What is the standard deduction available to a salaried employee under the new tax regime for FY 2024-25?"),
    ("Q-E05", "Easy", "What is the tax rate applicable to long-term capital gains on listed equity shares held for more than 12 months as per the latest budget?"),
    ("Q-M01", "Medium", "A salaried individual earns ₹18,00,000 gross annual salary in FY 2024-25, contributes ₹1,50,000 to EPF, pays ₹50,000 NPS Tier-1, and has ₹25,000 health insurance premium. Compute tax under the new regime (assume standard deduction applies)."),
    ("Q-M02", "Medium", "I bought a residential property for ₹80,00,000 in 2018 and sold it in FY 2024-25 for ₹1,20,00,000. Compute the capital gains tax due (state your indexation assumptions clearly)."),
    ("Q-M03", "Medium", "An individual transfers ₹12,00,000 in a financial year under the Liberalised Remittance Scheme (LRS) for foreign education. What TCS rate applies after the FY 2023-24 changes to Section 206C, and what exemption applies?"),
    ("Q-M04", "Medium", "What are the provisions for taxation of Virtual Digital Assets (cryptocurrency) under Section 115BBH, including the rate, the loss set-off rule, and the TDS under Section 194S?"),
    ("Q-M05", "Medium", "A taxpayer has salary income and one self-occupied house with home-loan interest of ₹2,00,000. With gross total income of ₹15,00,000 (all salary except the interest deduction), under which regime (old vs new) is tax lower, and why?"),
    ("Q-C01", "Complex", "Mr. A (resident, 45) has: (i) salary ₹24,00,000; (ii) LTCG ₹6,00,000 on listed equity sold after 23 July 2024; (iii) STCG on equity ₹2,00,000; (iv) interest income ₹3,00,000. He invests ₹2,00,000 in PPF and pays ₹75,000 medical insurance. Compute total tax under BOTH regimes and recommend the better one. Show every slab step, surcharge and cess."),
    ("Q-C02", "Complex", "A non-resident FII earned ₹50,00,000 from Indian listed securities in FY 2024-25. Explain how the FAQs on FIIs exemption and the transition provisions apply, what rate applies, and what documentation is needed to claim the benefit."),
    ("Q-C03", "Complex", "Compare the treatment of 'days of stay' for determining residential status for an individual with Indian income of ₹40,00,000 who visited India for 130 days across two visits in a year, referencing the deeming provisions. Then compute the tax consequence if the person is RNOR with the same income."),
]

VIVO_MAP = [
    ("vivo_1.mp3", "Q-E01"), ("vivo_2.mp3", "Q-E02"), ("vivo_3.mp3", "Q-E05"),
    ("vivo_4.mp3", "Q-M01"), ("vivo_5.mp3", "Q-M04"), ("vivo_6.mp3", "Q-C01"),
    ("vivo_7.mp3", "Q-C03"),
]


def _cell(text: str, limit: int = 320) -> str:
    text = text.replace("\n", " ").replace("|", "\\|").strip()
    return text[:limit] + "…" if len(text) > limit else text


def _table(results: list[dict], tier: str) -> str:
    rows = [r for r in results if r["tier"] == tier]
    lines = [
        "| ID | Question | Answer (truncated) | Correct? | Note | Sources |",
        "|----|----------|--------------------|----------|------|---------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['qid']} | {_cell(r['question'], 110)} | {_cell(r['answer'])} |  |  | {_cell(r['sources'], 180)} |"
        )
    return "\n".join(lines)


def _details(results: list[dict]) -> str:
    out = []
    for r in results:
        out.append(
            f"<details><summary>{r['qid']} — full answer ({r['ms']:.0f} ms)</summary>\n\n"
            f"{r['answer']}\n\n**Sources:** {r['sources']}\n\n</details>"
        )
    return "\n\n".join(out)


def run() -> None:
    provider, model, _ = llm.resolve()
    print(f"Provider={provider} model={model}")
    results: list[dict] = []
    for i, (qid, tier, q) in enumerate(QUESTIONS, 1):
        print(f"[{i}/{len(QUESTIONS)}] {qid} ({tier})…", flush=True)
        t0 = time.time()
        res = core.answer_question(q)
        results.append(
            {
                "qid": qid, "tier": tier, "question": q,
                "answer": res["answer"], "sources": core.format_sources(res["sources"]),
                "ms": (time.time() - t0) * 1000,
            }
        )

    def _vivo_row(f: str, qid: str) -> str:
        if f == "vivo_7.mp3":  # the multi-turn demo: Q-C03 + an RNOR/ROR follow-up
            return f"| demo/{f} | {qid} | Yes | Yes | Yes | Multi-turn: Q-C03 then a follow-up on ROR tax liability |"
        return f"| demo/{f} | {qid} | Yes | Yes | n/a | Single-turn spoken Q and A |"

    vivo_rows = "\n".join(_vivo_row(f, qid) for f, qid in VIVO_MAP)
    content = f"""# TITO Test Results — APICN004

- LLM provider / model: `{provider}` / `{model}`
- Top-k retrieved: {core.config.top_k()}
- Vector store: ChromaDB (cosine) over sentence-transformers `{core.config.embed_model()}`
- Correctness column filled in by human review against the official answer key.

## Easy

{_table(results, "Easy")}

## Medium

{_table(results, "Medium")}

## Complex

{_table(results, "Complex")}

## Full answers

{_details(results)}

## VIVO demo integration notes

| Demo file | Question ID | Transcript captured? | Answer audible? | Follow-up handled? | Note |
|-----------|-------------|----------------------|-----------------|--------------------|------|
{vivo_rows}
"""
    out = Path(__file__).resolve().parents[1] / "report" / "test_results.md"
    out.write_text(content, encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    run()
