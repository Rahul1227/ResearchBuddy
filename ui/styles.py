APP_STYLES = """
<style>
html, body, [class*="css"] { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; color: #e8e4dc; }

.stApp {
    background: #07070d;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(90,70,200,0.07) 0%, transparent 55%);
}

/* ── Animations ─────────────────────────────────────────────────────── */
@keyframes scan      { from{transform:translateY(-250%);} to{transform:translateY(250%);} }
@keyframes pulse-glow {
  0%,100%{ box-shadow:0 0 8px rgba(255,140,50,.2), inset 0 0 0 rgba(255,140,50,0); }
  50%    { box-shadow:0 0 28px rgba(255,140,50,.5), inset 0 0 12px rgba(255,140,50,.04); }
}
@keyframes badge-pop  { 0%{opacity:0;transform:scale(.85);} 100%{opacity:1;transform:scale(1);} }

/* ── Layout ─────────────────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1460px; }

/* ── Hero ───────────────────────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 2.8rem 1rem 2rem;
}
.hero-eyebrow {
    font-size: 0.7rem; font-weight: 600; letter-spacing: 0.28em; text-transform: uppercase;
    color: #ff8c32; margin-bottom: 0.9rem; opacity: 0.9;
    font-family: ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace;
}
.hero h1 {
    font-size: clamp(2.8rem, 6vw, 5.2rem);
    font-weight: 800; line-height: 1; letter-spacing: -0.04em;
    color: #f0ebe0; margin: 0 0 1rem;
}
.hero h1 span {
    background: linear-gradient(135deg, #ffb347 0%, #ff8c32 40%, #ff5a1a 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub {
    font-size: 1.05rem; font-weight: 300; color: #a09890;
    max-width: 620px; margin: 0 auto; line-height: 1.75;
}
.hero-badges {
    display: flex; justify-content: center;
    gap: 0.6rem; margin-top: 1.4rem; flex-wrap: wrap;
}
.hero-badge {
    font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase;
    font-family: ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace;
    color: #8d867e; background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09); border-radius: 99px; padding: 0.28rem 0.85rem;
    animation: badge-pop .4s ease both;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

/* ── Input ──────────────────────────────────────────────────────────── */
.stTextInput>div>div>input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,140,50,0.25) !important; border-radius: 12px !important;
    color: #f0ebe0 !important;
    font-size: 1.05rem !important; padding: 0.85rem 1rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput>div>div>input:focus {
    border-color: #ff8c32 !important; box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
.stTextInput>label {
    font-family: ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace !important;
    font-size: 0.76rem !important; letter-spacing: 0.18em !important;
    text-transform: uppercase !important; color: #ff8c32 !important; font-weight: 500 !important;
}

/* ── Primary Button ─────────────────────────────────────────────────── */
.stButton>button, .stDownloadButton>button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-weight: 700 !important; font-size: 0.98rem !important; letter-spacing: 0.04em !important;
    border: none !important; border-radius: 12px !important; padding: 0.8rem 2.2rem !important;
    transition: transform .15s, box-shadow .15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    white-space: normal !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    text-align: center !important;
}
.stButton>button:hover, .stDownloadButton>button:hover {
    transform: translateY(-2px) !important; box-shadow: 0 8px 28px rgba(255,140,50,0.45) !important;
}
.stButton>button p, .stDownloadButton>button p {
    white-space: normal !important; text-align: center !important;
    line-height: 1.35 !important; margin: 0 !important;
}
/* Secondary buttons */
[data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.04) !important;
    color: #c9c2b7 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    box-shadow: none !important;
    font-size: 0.86rem !important; font-weight: 400 !important;
    white-space: normal !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    text-align: center !important;
}
[data-testid="baseButton-secondary"] p {
    white-space: normal !important; text-align: center !important;
    line-height: 1.35 !important; margin: 0 !important;
}
[data-testid="baseButton-secondary"]:hover {
    border-color: rgba(255,140,50,0.3) !important; color: #ff8c32 !important;
    transform: translateY(-1px) !important; box-shadow: none !important;
}
/* Equal-height cards when buttons are inside columns */
[data-testid="column"] .stButton { height: 100%; }
[data-testid="column"] .stButton>button {
    height: 100% !important; min-height: 80px !important;
}
[data-testid="column"] .stButton>button p {
    font-size: 0.9rem !important; font-weight: 600 !important; letter-spacing: 0.01em !important;
}

/* ── Section Heading ────────────────────────────────────────────────── */
.section-heading {
    font-size: 1.5rem; font-weight: 700; color: #f0ebe0; margin: 0 0 1rem;
}

/* ── Step Cards ─────────────────────────────────────────────────────── */
.step-card {
    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem;
    position: relative; overflow: hidden; transition: border-color .3s, background .3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.45); background: rgba(255,140,50,0.035);
    animation: pulse-glow 2.2s ease-in-out infinite;
}
.step-card.done { border-color: rgba(80,200,120,0.3); background: rgba(80,200,120,0.025); }
.step-card::before {
    content:''; position:absolute; left:0; top:0; bottom:0; width:3px;
    background:rgba(255,255,255,0.05);
}
.step-card.active::before { background: linear-gradient(180deg,#ff8c32,#ff5a1a); }
.step-card.done::before   { background: #50c878; }
.step-scan {
    position:absolute; top:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,rgba(255,140,50,.8),transparent);
    animation:scan 1.8s linear infinite;
}
.step-header { display:flex; align-items:center; gap:0.75rem; margin-bottom:0.3rem; }
.step-icon {
    width:30px; height:30px; border-radius:8px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    background:rgba(255,255,255,0.06); font-size:0.85rem;
}
.step-card.active .step-icon { background:rgba(255,140,50,0.15); }
.step-card.done .step-icon   { background:rgba(80,200,120,0.12); }
.step-num, .panel-label, .metrics-kicker {
    font-family: ui-monospace, 'Cascadia Code', Menlo, Consolas, monospace;
}
.step-num   { font-size:.63rem; letter-spacing:.15em; color:#ff8c32; opacity:.7; }
.step-title { font-size:.9rem; font-weight:700; color:#f0ebe0; }
.step-status { margin-left:auto; font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace; font-size:.63rem; letter-spacing:.1em; }
.status-waiting { color:#444; }
.status-running { color:#ff8c32; }
.status-done    { color:#50c878; }
.step-desc { font-size:.83rem; color:#7a746d; margin-top:.2rem; line-height:1.5; }

/* ── Pipeline Progress Bar ──────────────────────────────────────────── */
.pipe-progress-wrap { height:3px; background:rgba(255,255,255,0.05); border-radius:99px; margin:.8rem 0 1.2rem; overflow:hidden; }
.pipe-progress-bar  { height:100%; background:linear-gradient(90deg,#ff8c32,#ff5a1a); border-radius:99px; transition:width .5s ease; }

/* ── Result Panels ──────────────────────────────────────────────────── */
.result-panel {
    background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07);
    border-radius:16px; padding:1.4rem 1.6rem; margin:.7rem 0 1.5rem;
}
.result-panel-title {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
    color:#ff8c32; margin-bottom:.9rem; padding-bottom:.7rem; border-bottom:1px solid rgba(255,140,50,0.15);
}
.result-content { font-size:.98rem; line-height:1.8; color:#cdc8bf; white-space:pre-wrap; }

.report-shell, .feedback-shell, .metrics-shell {
    background:rgba(255,255,255,0.025); border-radius:18px; padding:1.8rem 2rem; margin-bottom:1.5rem;
}
.report-shell  { border:1px solid rgba(255,140,50,0.2); }
.feedback-shell{ border:1px solid rgba(80,200,120,0.2); }
.metrics-shell { border:1px solid rgba(255,255,255,0.08); }

.panel-label { font-size:.72rem; letter-spacing:.2em; text-transform:uppercase; margin-bottom:1rem; padding-bottom:.7rem; }
.orange{ color:#ff8c32; border-bottom:1px solid rgba(255,140,50,0.15); }
.green { color:#50c878; border-bottom:1px solid rgba(80,200,120,0.15); }
.blue  { color:#64b5f6; border-bottom:1px solid rgba(100,181,246,0.15); }
.purple{ color:#b39ddb; border-bottom:1px solid rgba(179,157,219,0.15); }

/* ── Metrics Grid ───────────────────────────────────────────────────── */
.report-meta-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(110px,1fr)); gap:.9rem; margin-bottom:1.5rem;
}
.metric-card {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:14px; padding:1rem 1.1rem; transition:border-color .2s;
}
.metric-card:hover { border-color:rgba(255,140,50,0.2); }
.metrics-kicker { font-size:.68rem; letter-spacing:.14em; text-transform:uppercase; color:#8d867e; margin-bottom:.4rem; }
.metric-value { font-size:1.4rem; color:#f0ebe0; font-weight:700; }
.metric-sub   { font-size:.75rem; color:#6d6760; margin-top:.15rem; }

/* ── Source Cards ───────────────────────────────────────────────────── */
.source-card {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:14px; padding:1rem 1.2rem; margin-bottom:.9rem;
    transition:border-color .2s, transform .15s;
}
.source-card:hover { border-color:rgba(255,140,50,0.2); transform:translateX(3px); }
.source-card-top { display:flex; justify-content:space-between; align-items:center; gap:.8rem; margin-bottom:.45rem; }
.source-index, .source-domain {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.68rem; letter-spacing:.12em;
}
.source-index  { color:#ff8c32; }
.source-domain { color:#8d867e; }
.source-badge {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.6rem; letter-spacing:.1em; text-transform:uppercase;
    padding:.15rem .5rem; border-radius:99px; border:1px solid;
}
.badge-high{ color:#50c878; border-color:rgba(80,200,120,0.4);  background:rgba(80,200,120,0.07); }
.badge-med { color:#ffb347; border-color:rgba(255,179,71,0.4);  background:rgba(255,179,71,0.07); }
.badge-low { color:#888;    border-color:rgba(136,136,136,0.3); background:rgba(136,136,136,0.05);}
.source-title   { font-size:.95rem; color:#f0ebe0; margin-bottom:.4rem; font-weight:600; }
.source-snippet { font-size:.9rem; line-height:1.65; color:#c9c2b7; }
.source-url     { font-size:.88rem; margin-top:.45rem; color:#9f988f; word-break:break-word; }
.source-url a   { color:#ff8c32; text-decoration:none; }
.source-url a:hover { text-decoration:underline; }

/* ── Entity Tags ────────────────────────────────────────────────────── */
.entity-section { margin:1rem 0 1.4rem; }
.entity-category {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.66rem; letter-spacing:.14em; text-transform:uppercase;
    color:#8d867e; margin-bottom:.5rem; margin-top:.9rem;
}
.entity-grid { display:flex; flex-wrap:wrap; gap:.45rem; }
.entity-tag {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.7rem; padding:.28rem .75rem;
    border-radius:99px; letter-spacing:.07em; border:1px solid; transition:all .2s; cursor:default;
}
.entity-tag:hover { transform:translateY(-1px); }
.ep { color:#f48fb1; border-color:rgba(244,143,177,.35); background:rgba(244,143,177,.07); }
.eo { color:#80cbc4; border-color:rgba(128,203,196,.35); background:rgba(128,203,196,.07); }
.et { color:#90caf9; border-color:rgba(144,202,249,.35); background:rgba(144,202,249,.07); }
.ed { color:#ffcc80; border-color:rgba(255,204,128,.35); background:rgba(255,204,128,.07); }
.es { color:#a5d6a7; border-color:rgba(165,214,167,.35); background:rgba(165,214,167,.07); }
.el { color:#ce93d8; border-color:rgba(206,147,216,.35); background:rgba(206,147,216,.07); }

/* ── Score Circle ───────────────────────────────────────────────────── */
.score-display { display:flex; align-items:center; gap:1.2rem; margin:1rem 0 1.4rem; }
.score-circle {
    width:68px; height:68px; border-radius:50%; border:2.5px solid #50c878;
    display:flex; align-items:center; justify-content:center;
    font-size:1.35rem; font-weight:800;
    color:#50c878; flex-shrink:0;
}
.score-info    { display:flex; flex-direction:column; gap:.25rem; }
.score-label   { font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace; font-size:.68rem; letter-spacing:.12em; color:#8d867e; text-transform:uppercase; }
.score-verdict { font-size:.92rem; color:#cdc8bf; line-height:1.55; }

/* ── Related Topics ─────────────────────────────────────────────────── */
.related-shell { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:16px; padding:1.4rem 1.6rem; margin-bottom:1.5rem; }
.related-desc  { font-size:.88rem; color:#8d867e; margin-bottom:.9rem; line-height:1.6; }
.related-grid  { display:flex; flex-wrap:wrap; gap:.5rem; }
.related-chip  {
    font-size:.86rem; color:#c9c2b7; background:rgba(255,255,255,0.035);
    border:1px solid rgba(255,255,255,0.09); border-radius:10px; padding:.4rem .95rem;
    transition:all .2s; cursor:default;
}
.related-num   { font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace; color:#ff8c32; font-size:.7rem; margin-right:.4rem; }

/* ── Citations ──────────────────────────────────────────────────────── */
.citation-shell { background:rgba(255,255,255,0.025); border:1px solid rgba(255,255,255,0.07); border-radius:16px; padding:1.4rem 1.6rem; margin-bottom:1.5rem; }
.citation-item {
    display:flex; gap:.8rem; margin-bottom:.9rem; align-items:flex-start;
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.78rem; line-height:1.7; color:#bdb8b0;
    padding-bottom:.9rem; border-bottom:1px solid rgba(255,255,255,0.05);
}
.citation-item:last-child { border-bottom:none; margin-bottom:0; padding-bottom:0; }
.citation-num-tag {
    font-size:.68rem; color:#ff8c32; font-weight:700;
    background:rgba(255,140,50,0.1); border:1px solid rgba(255,140,50,0.25);
    border-radius:6px; padding:.1rem .45rem; flex-shrink:0; margin-top:.1rem;
}
.citation-item a { color:#ff8c32; text-decoration:none; }
.citation-item a:hover { text-decoration:underline; }

/* ── History Sidebar ────────────────────────────────────────────────── */
.history-header {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.68rem; letter-spacing:.2em; text-transform:uppercase;
    color:#8d867e; margin-bottom:.8rem; padding-bottom:.5rem; border-bottom:1px solid rgba(255,255,255,0.06);
}
.history-item {
    background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.07);
    border-radius:10px; padding:.7rem .9rem; margin-bottom:.5rem; cursor:pointer; transition:border-color .2s;
}
.history-item:hover { border-color:rgba(255,140,50,0.3); }
.history-topic { font-size:.88rem; color:#d4cec5; }
.history-meta  { font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace; font-size:.62rem; color:#6d6760; margin-top:.3rem; }

/* ── Tabs ───────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] { background:transparent !important; gap:.4rem; }
.stTabs [data-baseweb="tab"] {
    background:rgba(255,255,255,0.03) !important; border:1px solid rgba(255,255,255,0.07) !important;
    border-radius:8px !important; color:#8d867e !important;
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace !important;
    font-size:.72rem !important; letter-spacing:.1em !important;
    text-transform:uppercase !important; padding:.35rem .9rem !important;
}
.stTabs [aria-selected="true"] {
    background:rgba(255,140,50,0.09) !important; border-color:rgba(255,140,50,0.3) !important; color:#ff8c32 !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { background-color:transparent !important; }

/* ── Sidebar ────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background:rgba(7,7,13,0.97) !important; border-right:1px solid rgba(255,255,255,0.06) !important;
}
[data-testid="stSidebar"] .block-container { padding:1.5rem 1rem !important; }

/* ── Markdown Content ───────────────────────────────────────────────── */
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3 { color:#f7f1e7; line-height:1.15; font-weight:700; }
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] li  { font-size:1.05rem; line-height:1.8; }
div[data-testid="stMarkdownContainer"] code {
    background:rgba(255,140,50,0.1) !important; color:#ff8c32 !important;
    border-radius:4px !important; padding:.1rem .35rem !important;
}
div[data-testid="stMarkdownContainer"] blockquote {
    border-left:3px solid #ff8c32; padding-left:1rem; color:#a09890; margin:1rem 0;
}
div[data-testid="stMarkdownContainer"] table { border-collapse:collapse; width:100%; }
div[data-testid="stMarkdownContainer"] th {
    background:rgba(255,140,50,0.1); color:#ff8c32;
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace;
    font-size:.8rem; letter-spacing:.1em; text-transform:uppercase;
    padding:.6rem 1rem; border:1px solid rgba(255,255,255,0.08);
}
div[data-testid="stMarkdownContainer"] td {
    padding:.55rem 1rem; border:1px solid rgba(255,255,255,0.06); font-size:.95rem; color:#cdc8bf;
}
div[data-testid="stMarkdownContainer"] tr:hover td { background:rgba(255,255,255,0.02); }

details summary {
    font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace !important;
    font-size:.75rem !important; color:#a09890 !important; letter-spacing:.1em !important; cursor:pointer;
}
.notice { font-family:ui-monospace,'Cascadia Code',Menlo,Consolas,monospace; font-size:.72rem; color:#605850; text-align:center; margin-top:3rem; letter-spacing:.08em; }

/* ── Responsive ─────────────────────────────────────────────────────── */
@media (max-width:900px) {
    .block-container { padding:1.5rem 1.1rem 3rem; }
    .report-meta-grid { grid-template-columns:1fr 1fr; }
}
</style>
"""
