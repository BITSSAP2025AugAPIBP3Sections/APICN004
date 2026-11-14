"""Generate report/pipeline.svg — the request data-flow through the one shared pipeline."""
from pathlib import Path

W, H = 1180, 1000
BG = "#0D1117"
BLUE="#58A6FF"; PURPLE="#BC8CFF"; GREEN="#3FB950"; ORANGE="#F0883E"
CYAN="#39C5CF"; RED="#F85149"; MUTED="#8B949E"; DIM="#484F58"; INK="#C9D1D9"

def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

DEFS = """<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="11" cy="11" r="1" fill="#1C2128" opacity="0.8"/>
  </pattern>
  <filter id="drop" x="-12%" y="-12%" width="124%" height="124%">
    <feDropShadow dx="0" dy="5" stdDeviation="9" flood-color="#000" flood-opacity="0.5"/>
  </filter>
  <filter id="gb"><feGaussianBlur stdDeviation="3" result="b"/><feFlood flood-color="#58A6FF" flood-opacity="0.28" result="c"/><feComposite in="c" in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="gg"><feGaussianBlur stdDeviation="4" result="b"/><feFlood flood-color="#3FB950" flood-opacity="0.3" result="c"/><feComposite in="c" in2="b" operator="in" result="g"/><feMerge><feMergeNode in="g"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <marker id="m" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,11 4.5,0 9" fill="#6E7681"/></marker>
  <marker id="mb" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,11 4.5,0 9" fill="#58A6FF"/></marker>
  <marker id="mg" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,11 4.5,0 9" fill="#3FB950"/></marker>
  <marker id="mp" markerWidth="11" markerHeight="9" refX="9" refY="4.5" orient="auto"><polygon points="0 0,11 4.5,0 9" fill="#BC8CFF"/></marker>
</defs>"""

P=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
   f'font-family="\'JetBrains Mono\',\'Fira Code\',Consolas,monospace">',
   f'<rect width="{W}" height="{H}" fill="{BG}"/>',
   f'<rect width="{W}" height="{H}" fill="url(#dots)"/>', DEFS]

CX = W//2

# ── title ──
P.append(f'<text x="{CX}" y="42" font-size="21" font-weight="700" fill="#E6EDF3" text-anchor="middle" letter-spacing="0.4">Request Flow — one pipeline, four modes</text>')
P.append(f'<text x="{CX}" y="64" font-size="11" fill="{MUTED}" text-anchor="middle">Modes differ only in how the question enters and how the answer leaves · the RAG core is identical</text>')

def panel(x,y,w,h,stroke,fid,title,sub=""):
    o=[f'<rect x="{x+4}" y="{y+4}" width="{w}" height="{h}" rx="14" fill="#000" opacity="0.4" filter="url(#drop)"/>',
       f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#080E16" stroke="{stroke}" stroke-width="2" filter="url(#{fid})"/>',
       f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="14" fill="{stroke}" opacity="0.12"/>',
       f'<rect x="{x}" y="{y+28}" width="{w}" height="12" fill="#080E16"/>',
       f'<text x="{x+22}" y="{y+27}" font-size="14" font-weight="700" fill="{stroke}">{esc(title)}</text>']
    if sub: o.append(f'<text x="{x+w-20}" y="{y+27}" font-size="10" fill="{MUTED}" text-anchor="end">{esc(sub)}</text>')
    return "\n".join(o)

def chip(x,y,w,col,label,desc):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="40" rx="8" fill="{BG}" stroke="{col}" stroke-width="1.4"/>'
            f'<text x="{x+16}" y="{y+25}" font-size="11.5" font-weight="600" fill="{col}">{esc(label)}</text>'
            + (f'<text x="{x+w-14}" y="{y+25}" font-size="9.5" fill="{MUTED}" text-anchor="end">{esc(desc)}</text>' if desc else ''))

def varrow(y1,y2,mk="m",label="",x=CX):
    sc={"m":"#6E7681","mb":BLUE,"mg":GREEN,"mp":PURPLE}[mk]
    o=[f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{sc}" stroke-width="2" opacity="0.8" marker-end="url(#{mk})"/>']
    if label:
        o.append(f'<rect x="{x+10}" y="{(y1+y2)//2-9}" width="{len(label)*7+14}" height="18" rx="5" fill="{BG}" opacity="0.92" stroke="{sc}" stroke-width="0.8"/>')
        o.append(f'<text x="{x+17+len(label)*3.5}" y="{(y1+y2)//2+4}" font-size="10" fill="{sc}" text-anchor="middle">{esc(label)}</text>')
    return "\n".join(o)

# ── INPUT panel ──
IX, IW = 90, W-180
P.append(panel(IX, 90, IW, 128, BLUE, "gb", "① INPUT · Streamlit UI", "src/app.py"))
P.append(chip(IX+30, 142, 440, BLUE, "text box", "TITO / TIVO"))
P.append(chip(IX+30, 142+52, 440, CYAN, "🎙 st.audio_input → STT", "VITO / VIVO"))
# merge marker
P.append(f'<text x="{IX+IW-250}" y="178" font-size="12" fill="{INK}" text-anchor="middle">→ question</text>')
P.append(f'<text x="{IX+IW-250}" y="196" font-size="10" fill="{MUTED}" text-anchor="middle">(plain text)</text>')

P.append(varrow(218, 262, "mb", "question"))

# ── CORE panel ──
CY, CH = 262, 420
P.append(panel(IX, CY, IW, CH, GREEN, "gg", "② CORE PIPELINE", "src/rag/core.py · answer_question / stream_answer"))

STEPS=[("1","Retriever.search(question)","→ top-k chunks · ChromaDB cosine · year-aware + FAQ-hint", CYAN),
       ("2","build_context(hits)","→ context with [source: doc p.page] markers", PURPLE),
       ("3","llm.stream_chat(question, context)","→ grounded answer · streamed tokens (SSE)", ORANGE),
       ("4","dedupe_sources(hits)","→ citations (doc, page) from metadata, never model text", RED)]
sx, sw = IX+34, IW-68
for i,(n,fn,desc,col) in enumerate(STEPS):
    sy = CY+58 + i*86
    P.append(f'<rect x="{sx+4}" y="{sy+4}" width="{sw}" height="68" rx="10" fill="#000" opacity="0.3"/>')
    P.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="68" rx="10" fill="{BG}" stroke="{col}" stroke-width="1.5"/>')
    P.append(f'<circle cx="{sx+34}" cy="{sy+34}" r="18" fill="{col}" opacity="0.16" stroke="{col}" stroke-width="1.5"/>')
    P.append(f'<text x="{sx+34}" y="{sy+40}" font-size="17" font-weight="700" fill="{col}" text-anchor="middle">{n}</text>')
    P.append(f'<text x="{sx+66}" y="{sy+29}" font-size="13.5" font-weight="600" fill="{INK}">{esc(fn)}</text>')
    P.append(f'<text x="{sx+66}" y="{sy+51}" font-size="10.5" fill="{MUTED}">{esc(desc)}</text>')
    if i<3:
        ay=sy+68
        P.append(f'<line x1="{sx+34}" y1="{ay}" x2="{sx+34}" y2="{ay+18}" stroke="{DIM}" stroke-width="1.6" marker-end="url(#m)"/>')

P.append(varrow(CY+CH, CY+CH+44, "mg", "answer + sources"))

# ── OUTPUT panel ──
OY, OH = CY+CH+44, 150
P.append(panel(IX, OY, IW, OH, BLUE, "gb", "③ OUTPUT · Streamlit UI", "src/app.py"))
P.append(chip(IX+30, OY+52, IW-60, BLUE, "markdown answer  +  Sources expander", "TITO / VITO"))
P.append(chip(IX+30, OY+52+52, IW-60, PURPLE, "TTS(answer) → st.audio (autoplay)", "TIVO / VIVO"))

# ── side rail: modes legend ──
P.append(f'<text x="{CX}" y="{OY+OH+40}" font-size="10.5" fill="{MUTED}" text-anchor="middle">'
         f'TITO text→text   ·   TIVO text→voice   ·   VITO voice→text   ·   VIVO voice→voice   ·   history kept in st.session_state (multi-turn)</text>')

P.append("</svg>")
Path("report/pipeline.svg").write_text("\n".join(P), encoding="utf-8")
print("Saved report/pipeline.svg")
