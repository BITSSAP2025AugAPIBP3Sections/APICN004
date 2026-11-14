"""Generate report/architecture.svg — clean high-level architecture."""
from pathlib import Path

W, H = 1400, 860

BG = "#0D1117"
BLUE   = "#58A6FF"
PURPLE = "#BC8CFF"
GREEN  = "#3FB950"
ORANGE = "#F0883E"
CYAN   = "#39C5CF"
RED    = "#F85149"
MUTED  = "#8B949E"
DIM    = "#484F58"

def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def defs():
    return """<defs>
  <pattern id="dots" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="1" fill="#1C2128" opacity="0.8"/>
  </pattern>

  <filter id="drop" x="-10%" y="-10%" width="120%" height="120%">
    <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000" flood-opacity="0.5"/>
  </filter>

  <filter id="glow-b"><feGaussianBlur stdDeviation="3" result="b"/>
    <feFlood flood-color="#58A6FF" flood-opacity="0.3" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="glow-p"><feGaussianBlur stdDeviation="3" result="b"/>
    <feFlood flood-color="#BC8CFF" flood-opacity="0.3" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="glow-g"><feGaussianBlur stdDeviation="3" result="b"/>
    <feFlood flood-color="#3FB950" flood-opacity="0.3" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="glow-o"><feGaussianBlur stdDeviation="3" result="b"/>
    <feFlood flood-color="#F0883E" flood-opacity="0.3" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="glow-r"><feGaussianBlur stdDeviation="3" result="b"/>
    <feFlood flood-color="#F85149" flood-opacity="0.3" result="c"/>
    <feComposite in="c" in2="b" operator="in" result="g"/>
    <feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>

  <marker id="arr" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#484F58"/>
  </marker>
  <marker id="arr-b" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#58A6FF"/>
  </marker>
  <marker id="arr-g" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#3FB950"/>
  </marker>
  <marker id="arr-o" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#F0883E"/>
  </marker>
  <marker id="arr-p" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#BC8CFF"/>
  </marker>
  <marker id="arr-r" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">
    <polygon points="0 0, 10 4, 0 8" fill="#F85149"/>
  </marker>
</defs>"""

def layer(x, y, w, h, stroke, glow_id, fill_top, fill_bot, label, sublabel=""):
    return f"""
<rect x="{x+5}" y="{y+5}" width="{w}" height="{h}" rx="14" fill="#000" opacity="0.4" filter="url(#drop)"/>
<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"
      fill="{fill_bot}" stroke="{stroke}" stroke-width="2" filter="url(#{glow_id})"/>
<rect x="{x}" y="{y}" width="{w}" height="42" rx="14" fill="{fill_top}" opacity="0.6"/>
<rect x="{x}" y="{y+28}" width="{w}" height="14" fill="{fill_bot}" opacity="0.9"/>
<text x="{x+24}" y="{y+28}" font-size="15" font-weight="700" fill="{stroke}" letter-spacing="0.5">{esc(label)}</text>
{'<text x="'+str(x+w-22)+'" y="'+str(y+28)+'" font-size="10" fill="'+MUTED+'" text-anchor="end">'+esc(sublabel)+'</text>' if sublabel else ''}
"""

def box(x, y, w, h, stroke, glow_id, title, lines, rx=10):
    out = [
        f'<rect x="{x+3}" y="{y+3}" width="{w}" height="{h}" rx="{rx}" fill="#000" opacity="0.35"/>',
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="#0D1117" stroke="{stroke}" stroke-width="1.6" filter="url(#{glow_id})" opacity="0.97"/>',
        f'<text x="{x+w//2}" y="{y+26}" font-size="13" font-weight="700" fill="{stroke}" text-anchor="middle">{esc(title)}</text>',
        f'<line x1="{x+16}" y1="{y+33}" x2="{x+w-16}" y2="{y+33}" stroke="{stroke}" stroke-width="0.6" opacity="0.25"/>',
    ]
    for i,(txt,col) in enumerate(lines):
        out.append(f'<text x="{x+w//2}" y="{y+50+i*19}" font-size="10" fill="{col}" text-anchor="middle">{esc(txt)}</text>')
    return "\n".join(out)

def arrow(x1,y1,x2,y2, col="arr", label="", lx_off=8, ly_off=0):
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col.replace("arr","").replace("-","") or "#484F58"}" stroke-width="1.8" opacity="0.7" marker-end="url(#{col})"/>']
    # fix: extract colour from marker id
    stroke_map = {"arr":"#484F58","arr-b":BLUE,"arr-g":GREEN,"arr-o":ORANGE,"arr-p":PURPLE,"arr-r":RED}
    sc = stroke_map.get(col, "#484F58")
    out[0] = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{sc}" stroke-width="1.8" opacity="0.7" marker-end="url(#{col})"/>'
    if label:
        mx,my=(x1+x2)//2,(y1+y2)//2
        out.append(f'<rect x="{mx+lx_off-4}" y="{my+ly_off-8}" width="{len(label)*6.6+8}" height="17" rx="4" fill="{BG}" opacity="0.9"/>')
        out.append(f'<text x="{mx+lx_off+len(label)*3.3}" y="{my+ly_off+4}" font-size="9.5" fill="{sc}" text-anchor="middle">{esc(label)}</text>')
    return "\n".join(out)

def bidiarrow(x1,y1,x2,y2,col_id,label=""):
    sc_map={"arr-b":BLUE,"arr-g":GREEN,"arr-o":ORANGE,"arr-p":PURPLE,"arr-r":RED,"arr":DIM}
    sc=sc_map.get(col_id,DIM)
    vert=(x1==x2)
    if vert:
        off_l,off_r=f'x1="{x1-4}" y1="{y1}" x2="{x2-4}" y2="{y2}"',f'x1="{x1+4}" y1="{y2}" x2="{x2+4}" y2="{y1}"'
    else:
        off_l,off_r=f'x1="{x1}" y1="{y1-4}" x2="{x2}" y2="{y2-4}"',f'x1="{x2}" y1="{y1+4}" x2="{x1}" y2="{y2+4}"'
    out=[f'<line {off_l} stroke="{sc}" stroke-width="1.7" opacity="0.7" marker-end="url(#{col_id})"/>',
         f'<line {off_r} stroke="{sc}" stroke-width="1.7" opacity="0.7" marker-end="url(#{col_id})"/>']
    if label:
        mx,my=(x1+x2)//2,(y1+y2)//2
        out.append(f'<rect x="{mx+6}" y="{my-8}" width="{len(label)*6.6+8}" height="17" rx="4" fill="{BG}" opacity="0.9"/>')
        out.append(f'<text x="{mx+10+len(label)*3.3}" y="{my+4}" font-size="9.5" fill="{sc}" text-anchor="middle">{esc(label)}</text>')
    return "\n".join(out)

# ─── build SVG ────────────────────────────────────────────────────────────────
P = []
P.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
         f'font-family="\'JetBrains Mono\',\'Fira Code\',Consolas,monospace">')
P.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
P.append(f'<rect width="{W}" height="{H}" fill="url(#dots)"/>')
P.append(defs())

# ── TITLE ──────────────────────────────────────────────────────────────────────
P.append(f'<text x="{W//2}" y="38" font-size="22" font-weight="700" fill="#E6EDF3" text-anchor="middle" letter-spacing="0.4">'
         f'APICN004  ·  Indian Income Tax RAG VoiceBot</text>')
P.append(f'<text x="{W//2}" y="60" font-size="11" fill="{MUTED}" text-anchor="middle">'
         f'Four interaction modes — one shared RAG pipeline — grounded, cited, streaming answers</text>')

# ── LAYER A: STREAMLIT APPLICATION (y=75..245) ────────────────────────────────
P.append(layer(40, 75, W-80, 170, BLUE, "glow-b",
               "#0D2240", "#080F1A",
               "▣  STREAMLIT APPLICATION  ·  src/app.py",
               "st.audio_input  ·  st.write_stream  ·  st.audio(autoplay)  ·  session_state history"))

MODE = [("TITO","Text In\nText Out","#58A6FF"),
        ("TIVO","Text In\nVoice Out","#A371F7"),
        ("VITO","Voice In\nText Out","#39C5CF"),
        ("VIVO","Voice In\nVoice Out","#3FB950")]
mw, gap = 290, 28
mx0 = 40 + (W-80 - 4*mw - 3*gap)//2
for i,(nm,lb,col) in enumerate(MODE):
    mx = mx0 + i*(mw+gap)
    P.append(f'<rect x="{mx}" y="118" width="{mw}" height="112" rx="10" fill="{BG}" stroke="{col}" stroke-width="1.6" opacity="0.95"/>')
    P.append(f'<rect x="{mx}" y="118" width="{mw}" height="36" rx="10" fill="{col}" opacity="0.12"/>')
    P.append(f'<text x="{mx+mw//2}" y="142" font-size="16" font-weight="700" fill="{col}" text-anchor="middle">{nm}</text>')
    for j,line in enumerate(lb.split("\n")):
        P.append(f'<text x="{mx+mw//2}" y="{167+j*18}" font-size="10.5" fill="{MUTED}" text-anchor="middle">{line}</text>')

# ── LAYER B: SPEECH LAYER (y=260..355) ───────────────────────────────────────
P.append(layer(40, 260, W-80, 95, PURPLE, "glow-p",
               "#1A0A30", "#100620",
               "◎  SPEECH LAYER  ·  src/speech/",
               "Handles voice input and output — bypassed for TITO / TIVO input, TITO / VITO output"))

# STT box
P.append(box(70, 292, 600, 56, PURPLE, "glow-p", "STT  ·  faster-whisper  (local)",
             [("Whisper base model · @lru_cache · groq Whisper API option", MUTED)]))
# TTS box
P.append(box(730, 292, 630, 56, "#A371F7", "glow-p", "TTS  ·  edge-tts  en-IN-NeerjaNeural",
             [("sentence-group streaming → first audio in ~1.2 s · piper option", MUTED)]))

# ── LAYER C: RAG PIPELINE (y=375..555) ───────────────────────────────────────
P.append(layer(40, 375, W-80, 180, GREEN, "glow-g",
               "#0A2218", "#060F10",
               "⚙  RAG PIPELINE  ·  src/rag/",
               "src/rag/core.py · answer_question(question, history, top_k) → {answer, sources, timings}"))

# Retriever box (left)
P.append(box(70, 416, 580, 122, CYAN, "glow-g", "Retriever  ·  ChromaDB  ·  cosine",
             [("all-MiniLM-L6-v2  ·  384-dim  ·  top-k = 6", "#C9D1D9"),
              ("Year-aware: FY / AY detection → biased re-query", MUTED),
              ("FAQ-hint: $in filter for FAQ / guidance docs", MUTED)]))

# LLM box (right)
P.append(box(730, 416, 630, 122, ORANGE, "glow-o", "LLM Engine  ·  Streaming SSE",
             [("System prompt: answer ONLY from corpus · cite doc+page", "#C9D1D9"),
              ("slm qwen2.5:3b (Ollama)  ·  groq llama-3.3-70b  ·  openai / anthropic", MUTED),
              ("openai / anthropic / openrouter  ·  max_tokens=1800", MUTED)]))

# context arrow Retriever → LLM
P.append(arrow(650, 477, 730, 477, "arr-g", "context chunks"))

# ── LAYER D: KNOWLEDGE BASE (y=570..770) ─────────────────────────────────────
P.append(layer(40, 570, W-80, 200, ORANGE, "glow-o",
               "#2A1A06", "#160D03",
               "🗄  KNOWLEDGE BASE",
               "Built offline once via python src/rag/ingest.py  ·  index/ is gitignored and rebuilt locally"))

# ChromaDB
P.append(box(70, 614, 580, 60, "#D2A8FF", "glow-o", "ChromaDB Vector Store  ·  index/",
             [("5,757 chunks  ·  384-dim  ·  metadata: {doc, page, fy_tag}", MUTED)]))

# Ingestion pipeline
P.append(box(70, 686, 580, 74, "#2EA198", "glow-o", "Ingestion Pipeline  ·  src/rag/ingest.py",
             [("PyMuPDF  →  chunk (900 / 150)  →  all-MiniLM-L6-v2  →  ChromaDB", MUTED),
              ("fy_tag per budget year  ·  deterministic  ·  manifest.json", "#484F58")]))

# Corpus
P.append(box(730, 614, 630, 142, RED, "glow-r", "Corpus  ·  data/*.pdf  ·  11 documents",
             [("Income-tax Act 1961  (171 MB  ·  1,117 pages)", "#C9D1D9"),
              ("Budget speeches  FY 2022-23 → 2025-26  (5 files)", MUTED),
              ("FAQs on BIS / FIIs / Transition  +  Crypto guide  (5 files)", MUTED),
              ("gitignored · Act distributed via GitHub Release", "#484F58")]))

# ── ARROWS between layers ─────────────────────────────────────────────────────
CX = W//2   # centre-x for vertical arrows

# UI ↕ Speech (bidirectional, left=stt, right=tts)
P.append(bidiarrow(360, 245, 360, 260, "arr-p", "voice/text"))
P.append(bidiarrow(1045, 245, 1045, 260, "arr-p", "voice/text"))

# Speech ↕ Core (question down, answer stream up) — direction shown by arrowheads
P.append(arrow(CX-28, 355, CX-28, 375, "arr-g"))
P.append(arrow(CX+28, 375, CX+28, 355, "arr-p"))

# Retriever → ChromaDB
P.append(arrow(360, 538, 360, 570, "arr-o", "vector search"))

# ChromaDB → Ingestion (read/build)
P.append(arrow(360, 674, 360, 686, "arr-o"))

# Corpus → Ingestion (horizontal)
P.append(arrow(730, 685, 650, 685, "arr-r", "PDF pages"))

# ── FOOTER ────────────────────────────────────────────────────────────────────
P.append(f'<line x1="40" y1="{H-38}" x2="{W-40}" y2="{H-38}" stroke="{DIM}" stroke-width="0.7" opacity="0.4"/>')

badges = [
    ("Python 3.11", BLUE), ("ChromaDB", PURPLE), ("sentence-transformers", GREEN),
    ("edge-tts", ORANGE), ("faster-whisper", CYAN), ("Ollama", RED),
    ("Streamlit", BLUE),
]
bx = 50
for txt, col in badges:
    bw = len(txt)*7.5+18
    P.append(f'<rect x="{bx}" y="{H-30}" width="{bw}" height="20" rx="5" fill="{col}" opacity="0.12" stroke="{col}" stroke-width="1"/>')
    P.append(f'<text x="{bx+bw//2}" y="{H-16}" font-size="9.5" fill="{col}" text-anchor="middle">{esc(txt)}</text>')
    bx += bw + 10

P.append("</svg>")

out = Path("report/architecture.svg")
out.write_text("\n".join(P), encoding="utf-8")
print(f"Saved {out}  ({out.stat().st_size//1024} KB)")
