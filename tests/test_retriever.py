from src.rag.retriever import detect_fy


def test_detect_fy_direct():
    assert detect_fy("slab rates for FY 2024-25") == "FY2024-25"
    assert detect_fy("tax in FY2023-24 please") == "FY2023-24"


def test_detect_ay_maps_back_one_year():
    # AY 2025-26 corresponds to FY 2024-25
    assert detect_fy("limits for AY 2025-26") == "FY2024-25"


def test_detect_bare_year_pair():
    assert detect_fy("what changed in 2024-25 budget") == "FY2024-25"


def test_detect_none():
    assert detect_fy("what is the section 80C limit") is None
