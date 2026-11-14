# Corpus — Indian Income Tax (India)

Place all corpus PDFs in this folder. Ingestion (`python src/rag/ingest.py`) picks up every
`*.pdf` present here.

## Expected files

| File | Source | Committed? |
|------|--------|-----------|
| `Income-tax-Act-1961_2026_2026-06-18_02-47-37_b9326c_en.pdf` | Income-tax Act 1961 (~171 MB) | **No — via GitHub Release** |
| `bs202223.pdf`, `bs2023_24.pdf`, `bs2024_25(I).pdf`, `bs2024_25.pdf`, `bs2025_26.pdf` | Union Budget speeches | Yes |
| `FAQs-on-BIS-Exemption.pdf`, `FAQs-on-FIIs-Exemption.pdf`, `FAQs-on-Transition-Provisions.pdf`, `Updated-FQAs-on-Interplay&Transitions.pdf` | Government FAQs | Yes |
| `E-Book-Guidance-Note-Crypto-Asset-Reporting-Obligations.pdf` | Crypto / VDA guidance | Yes |

The Income-tax Act PDF exceeds GitHub's 100 MB limit, so it is attached as a **Release asset**.
Download it from the repository's Releases page and place it here with the exact filename.

`*.pdf` files are gitignored by default. Ingestion runs with whatever subset is present and
warns on `stderr` about any missing expected file; the full corpus is needed for the complete
official test bank (sections 80C, 112A, 115BBH, 194S, 206C, and residential-status questions).
