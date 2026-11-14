from src.rag.ingest import chunk_text, fy_tag_for


def test_chunk_text_basic_overlap():
    text = "word " * 400  # 2000 chars
    chunks = chunk_text(text, size=200, overlap=50)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)
    # deterministic
    assert chunks == chunk_text(text, size=200, overlap=50)


def test_chunk_text_empty():
    assert chunk_text("", 100, 10) == []
    assert chunk_text("   \n  ", 100, 10) == []


def test_chunk_text_short():
    assert chunk_text("hello world", 900, 150) == ["hello world"]


def test_fy_tag_budget_files():
    assert fy_tag_for("bs202223.pdf") == "FY2022-23"
    assert fy_tag_for("bs2023_24.pdf") == "FY2023-24"
    assert fy_tag_for("bs2024_25(I).pdf") == "FY2024-25"
    assert fy_tag_for("bs2025_26.pdf") == "FY2025-26"


def test_fy_tag_non_budget():
    assert fy_tag_for("Income-tax-Act-1961_2026.pdf") == "general"
    assert fy_tag_for("FAQs-on-FIIs-Exemption.pdf") == "general"
