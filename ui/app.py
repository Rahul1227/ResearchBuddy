from __future__ import annotations

import time
from datetime import datetime

import streamlit as st

from core.config import settings
from core.models import ResearchOptions
from core.pipeline import run_pipeline_step
from ui.components import (
    parse_related_topics,
    reading_time,
    render_citations,
    render_entities,
    render_metrics,
    render_progress_bar,
    render_related_topics_display,
    render_score_circle,
    render_source_card,
    render_step_card,
)
from ui.styles import APP_STYLES


# ── Pipeline step definitions ─────────────────────────────────────────────────

PIPELINE_STEPS = [
    ("search",   "01", "Search Agent",      "Finds recent, reliable web coverage"),
    ("reader",   "02", "Reader Analyst",    "Synthesizes multiple sources into evidence notes"),
    ("writer",   "03", "Writer Chain",      "Builds a long-form structured report"),
    ("critic",   "04", "Critic Chain",      "Reviews quality, coverage & missing angles"),
    ("entities", "05", "Entity Extractor",  "Maps people, orgs, tech & key statistics"),
    ("topics",   "06", "Topic Suggester",   "Generates follow-up research directions"),
]


def _html(markup: str) -> None:
    # Strip leading whitespace per-line so Markdown never treats indented lines
    # as code blocks (4-space rule). HTML doesn't care about indentation.
    clean = "\n".join(ln.lstrip() for ln in markup.strip().splitlines())
    st.markdown(clean, unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────

def _init_state() -> None:
    defaults: dict = {
        "results":                  {},
        "running":                  False,
        "done":                     False,
        "pipeline_step":            0,      # which step to execute next (0-5)
        "pipeline_data":            {},     # intermediate data shared across steps
        "pipeline_t0":              0.0,    # wall-clock start time
        "report_length":            "detailed",
        "source_count":             4,
        "scrape_limit":             6000,
        "include_comparison_table": True,
        "focus_areas":              [],
        "history":                  [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ── Step state helper ─────────────────────────────────────────────────────────

def _step_state(step_name: str) -> str:
    results = st.session_state.results
    if step_name in results:
        return "done"
    if st.session_state.running and not st.session_state.done:
        # The first step not yet in results is currently running
        for key, *_ in PIPELINE_STEPS:
            if key not in results:
                return "running" if key == step_name else "waiting"
    return "waiting"


def _count_done_steps() -> int:
    results = st.session_state.results
    if not results:
        return 0
    return sum(1 for key, *_ in PIPELINE_STEPS if key in results)


# ── Header ────────────────────────────────────────────────────────────────────

def _render_header() -> None:
    _html(APP_STYLES)
    _html(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">{settings.app_tagline}</div>
            <h1>Research<span>Buddy</span></h1>
            <p class="hero-sub">
                A multi-agent pipeline that searches, synthesises, writes, critiques,
                and extracts deep insights — powered by Gemini and Tavily.
            </p>
            <div class="hero-badges">
                <span class="hero-badge">Gemini 2.5 Flash</span>
                <span class="hero-badge">Tavily Search</span>
                <span class="hero-badge">6-Agent Pipeline</span>
                <span class="hero-badge">Entity Extraction</span>
                <span class="hero-badge">Smart Citations</span>
            </div>
        </div>
        <div class="divider"></div>
        """
    )


# ── Sidebar ───────────────────────────────────────────────────────────────────

def _render_sidebar() -> None:
    with st.sidebar:
        _html('<div class="history-header">Research History</div>')

        history: list[dict] = st.session_state.history
        if not history:
            st.caption("Your research sessions will appear here.")
        else:
            for i, entry in enumerate(reversed(history)):
                score_tag = f" · {entry['score']}" if entry.get("score") else ""
                elapsed_tag = f" · {entry.get('elapsed', '')}s" if entry.get("elapsed") else ""
                _html(
                    f'<div class="history-item">'
                    f'<div class="history-topic">{entry["topic"]}</div>'
                    f'<div class="history-meta">{entry["timestamp"]}{score_tag}{elapsed_tag}</div>'
                    f'</div>'
                )
                if st.button("Load", key=f"load_hist_{i}", type="secondary"):
                    st.session_state.results = entry["results"]
                    st.session_state.done = True
                    st.session_state.running = False
                    st.rerun()

        st.divider()
        st.caption(f"Model: `{settings.model_name}`")
        if st.session_state.results.get("elapsed"):
            st.caption(f"Last run: **{st.session_state.results['elapsed']}s**")


# ── Input column ──────────────────────────────────────────────────────────────

def _render_input_column() -> bool:
    # Pre-populate from example/related-topic buttons before the widget is instantiated
    if "topic_input_pending" in st.session_state:
        st.session_state.topic_input = st.session_state.pop("topic_input_pending")
    st.text_input(
        "Research Topic",
        placeholder="e.g. Recursive language models and where they matter most",
        key="topic_input",
    )
    run_clicked = st.button("Run Research Pipeline", use_container_width=True)

    with st.expander("Advanced Research Settings", expanded=False):
        st.selectbox("Report Length", ["standard", "detailed", "deep"], key="report_length")
        st.slider("Sources To Analyse", min_value=3, max_value=8, key="source_count")
        st.slider(
            "Content Extract Per Source (chars)",
            min_value=3000, max_value=10000, step=500, key="scrape_limit",
        )
        st.checkbox("Include Comparison Table", key="include_comparison_table")
        st.multiselect(
            "Focus Areas",
            options=[
                "market impact",
                "technical architecture",
                "risks and limitations",
                "timeline and trend shifts",
                "business strategy",
                "research gaps",
                "ethical considerations",
                "regulatory landscape",
            ],
            key="focus_areas",
        )

    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress", "Quantum computing breakthroughs"]
    st.caption("TRY AN EXAMPLE")
    cols = st.columns(len(examples), gap="small")
    for col, example in zip(cols, examples):
        with col:
            if st.button(example, key=f"ex_{example}", type="primary", use_container_width=True):
                st.session_state.topic_input_pending = example
                st.session_state.results = {}
                st.session_state.pipeline_data = {}
                st.session_state.pipeline_step = 0
                st.session_state.pipeline_t0 = time.time()
                st.session_state.running = True
                st.session_state.done = False
                st.rerun()

    return run_clicked


# ── Pipeline column ───────────────────────────────────────────────────────────

def _render_pipeline_column() -> None:
    _html('<div class="section-heading">Pipeline</div>')
    done = _count_done_steps()
    render_progress_bar(done, len(PIPELINE_STEPS))
    for key, num, title, description in PIPELINE_STEPS:
        render_step_card(num, title, _step_state(key), description, key=key)


# ── Run pipeline ──────────────────────────────────────────────────────────────

def _run_pipeline_if_needed(run_clicked: bool) -> None:
    if run_clicked:
        topic = st.session_state.get("topic_input", "").strip()
        if not topic:
            st.warning("Please enter a research topic first.")
            return
        st.session_state.results = {}
        st.session_state.pipeline_data = {}
        st.session_state.pipeline_step = 0
        st.session_state.pipeline_t0 = time.time()
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

    if not st.session_state.running or st.session_state.done:
        return

    topic = st.session_state.topic_input
    options = ResearchOptions(
        report_length=st.session_state.report_length,
        source_count=st.session_state.source_count,
        scrape_limit=st.session_state.scrape_limit,
        focus_areas=st.session_state.focus_areas,
        include_comparison_table=st.session_state.include_comparison_table,
    )
    step = st.session_state.pipeline_step

    # Execute the current step
    updates, new_data = run_pipeline_step(
        step, topic, options, st.session_state.pipeline_data
    )
    st.session_state.results.update(updates)
    st.session_state.pipeline_data = new_data
    st.session_state.pipeline_step = step + 1

    # All 6 steps done (indices 0-5)
    if st.session_state.pipeline_step >= len(PIPELINE_STEPS):
        elapsed = round(time.time() - st.session_state.pipeline_t0, 1)
        st.session_state.results["elapsed"] = elapsed
        st.session_state.running = False
        st.session_state.done = True

        import re as _re
        score_match = _re.search(
            r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10",
            st.session_state.results.get("critic", ""),
            _re.IGNORECASE,
        )
        score = f"{score_match.group(1)}/10" if score_match else ""
        st.session_state.history.append({
            "topic":     topic,
            "timestamp": datetime.now().strftime("%b %d, %H:%M"),
            "score":     score,
            "elapsed":   elapsed,
            "results":   dict(st.session_state.results),
        })
        if len(st.session_state.history) > 20:
            st.session_state.history = st.session_state.history[-20:]

    st.rerun()


# ── HTML export helper ────────────────────────────────────────────────────────

def _build_html_export(results: dict) -> str:
    topic   = results.get("topic", "Research Report")
    report  = results.get("writer", "").replace("`", "\\`").replace("${", "\\${")
    sources = results.get("sources", [])
    critic  = results.get("critic", "")
    ts      = datetime.now().strftime("%Y-%m-%d %H:%M")

    sources_html = "".join(
        f'<li><a href="{s.get("url","")}" target="_blank">{s.get("title","Untitled")}</a> '
        f'— <em>{s.get("domain","")}</em></li>'
        for s in sources
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{topic} — ResearchBuddy</title>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  :root{{--bg:#07070d;--fg:#e8e4dc;--accent:#ff8c32;--card:rgba(255,255,255,0.04);--border:rgba(255,255,255,0.09);}}
  *{{box-sizing:border-box;}}
  body{{background:var(--bg);color:var(--fg);font-family:system-ui,sans-serif;max-width:900px;margin:0 auto;padding:2rem 1.5rem 4rem;line-height:1.75;}}
  h1,h2,h3{{font-weight:800;letter-spacing:-.02em;}}
  h1{{font-size:2rem;color:#f0ebe0;border-bottom:2px solid var(--accent);padding-bottom:.5rem;margin-bottom:1.5rem;}}
  h2{{font-size:1.4rem;color:#f0ebe0;margin-top:2rem;}}
  h3{{font-size:1.1rem;color:#f0ebe0;}}
  a{{color:var(--accent);}}
  p,li{{font-size:1rem;color:#cdc8bf;}}
  code{{background:rgba(255,140,50,0.1);color:var(--accent);border-radius:4px;padding:.1rem .35rem;font-size:.9em;}}
  pre{{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow:auto;}}
  blockquote{{border-left:3px solid var(--accent);padding-left:1rem;color:#a09890;margin:1rem 0;}}
  table{{border-collapse:collapse;width:100%;margin:1rem 0;}}
  th{{background:rgba(255,140,50,0.12);color:var(--accent);text-align:left;padding:.5rem .9rem;border:1px solid var(--border);font-size:.85rem;text-transform:uppercase;letter-spacing:.08em;}}
  td{{padding:.5rem .9rem;border:1px solid var(--border);color:#cdc8bf;}}
  tr:hover td{{background:rgba(255,255,255,0.02);}}
  .meta{{font-family:monospace;font-size:.75rem;color:#6d6760;margin-bottom:2rem;letter-spacing:.08em;text-transform:uppercase;}}
  .sources{{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--border);}}
  .sources ul{{padding-left:1.2rem;}}
  .critic{{background:var(--card);border:1px solid rgba(80,200,120,0.2);border-radius:12px;padding:1.2rem 1.5rem;margin-top:2rem;}}
  .critic-title{{font-family:monospace;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:#50c878;margin-bottom:.8rem;}}
  .footer{{margin-top:4rem;text-align:center;font-family:monospace;font-size:.7rem;color:#555;letter-spacing:.1em;}}
</style>
</head>
<body>
<div class="meta">ResearchBuddy · Generated {ts}</div>
<div id="report-content"></div>
<div class="sources">
  <h2>Sources</h2>
  <ul>{sources_html}</ul>
</div>
<div class="critic">
  <div class="critic-title">Quality Assessment</div>
  <pre style="background:none;border:none;padding:0;white-space:pre-wrap;color:#cdc8bf;font-size:.9rem;">{critic}</pre>
</div>
<div class="footer">Generated by ResearchBuddy · Multi-Agent AI Research System</div>
<script>
  const md = `{report}`;
  document.getElementById('report-content').innerHTML = marked.parse(md);
</script>
</body>
</html>"""


# ── Results rendering ─────────────────────────────────────────────────────────

def _render_results() -> None:
    results = st.session_state.results
    if not results:
        return

    sources  = results.get("sources", [])
    report   = results.get("writer", "")
    domains  = sorted({s.get("domain", "") for s in sources if s.get("domain")})
    elapsed  = results.get("elapsed", "")

    _html('<div class="divider"></div>')
    _html('<div class="section-heading">Results</div>')

    render_metrics([
        ("Sources Reviewed",  str(len(sources))),
        ("Unique Domains",    str(len(domains))),
        ("Report Words",      str(len(report.split()))),
        ("Reading Time",      reading_time(report)),
        ("Pipeline Time",     f"{elapsed}s" if elapsed else "—"),
    ])

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_report, tab_analysis, tab_sources, tab_citations, tab_related = st.tabs([
        "📄  Report",
        "🔬  Analysis",
        "🌐  Sources",
        "📚  Citations",
        "🔭  Related Topics",
    ])

    # ── Report tab ────────────────────────────────────────────────────────────
    with tab_report:
        if results.get("search"):
            with st.expander("Search Agent Output", expanded=False):
                _html(
                    f'<div class="result-panel">'
                    f'<div class="result-panel-title">Search Agent</div>'
                    f'<div class="result-content">{results["search"]}</div>'
                    f'</div>'
                )
        if results.get("reader"):
            with st.expander("Reader Synthesis", expanded=False):
                _html(
                    f'<div class="result-panel">'
                    f'<div class="result-panel-title">Reader Analyst Output</div>'
                    f'<div class="result-content">{results["reader"]}</div>'
                    f'</div>'
                )

        if results.get("options"):
            opts = results["options"]
            render_metrics(
                [
                    ("Report Mode",   opts.get("report_length", "detailed").title()),
                    ("Target Words",  str(opts.get("target_words", ""))),
                    ("Focus Areas",   str(len(opts.get("focus_areas", [])))),
                ],
                title="Report Configuration",
            )

        _html(
            """
            <div class="report-shell">
                <div class="panel-label orange">Final Research Report</div>
            """
        )
        st.markdown(report)
        _html("</div>")

        col_md, col_html = st.columns(2)
        with col_md:
            st.download_button(
                label="⬇ Download Markdown",
                data=report,
                file_name=f"research_{int(time.time())}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_html:
            html_export = _build_html_export(results)
            st.download_button(
                label="⬇ Download HTML",
                data=html_export,
                file_name=f"research_{int(time.time())}.html",
                mime="text/html",
                use_container_width=True,
            )

    # ── Analysis tab ──────────────────────────────────────────────────────────
    with tab_analysis:
        if results.get("critic"):
            _html(
                """
                <div class="feedback-shell">
                    <div class="panel-label green">Critic Feedback</div>
                """
            )
            render_score_circle(results["critic"])
            st.markdown(results["critic"])
            _html("</div>")

        if results.get("entities"):
            _html('<div class="section-heading" style="margin-top:1.5rem;font-size:1.15rem">Key Entities</div>')
            render_entities(results["entities"])

        if results.get("stats"):
            _html('<div class="section-heading" style="margin-top:1.5rem;font-size:1.15rem">Key Statistics</div>')
            _html(
                f'<div class="result-panel"><div class="result-panel-title">Quantitative Findings</div>'
                f'<div class="result-content">{results["stats"]}</div></div>'
            )

    # ── Sources tab ───────────────────────────────────────────────────────────
    with tab_sources:
        if sources:
            _html(f'<div class="section-heading" style="font-size:1.15rem">{len(sources)} Sources Reviewed</div>')
            for index, source in enumerate(sources, start=1):
                render_source_card(source, index)
        else:
            st.caption("No sources available.")

    # ── Citations tab ─────────────────────────────────────────────────────────
    with tab_citations:
        render_citations(sources)
        st.caption(
            "Citation format: Author/Title. Domain. Year. URL. "
            "For academic use, verify publication details directly."
        )

    # ── Related topics tab ────────────────────────────────────────────────────
    with tab_related:
        if results.get("topics"):
            render_related_topics_display(results["topics"])
            topics_list = parse_related_topics(results["topics"])
            if topics_list:
                st.markdown("**Research any of these topics:**")
                cols = st.columns(2)
                for i, topic in enumerate(topics_list):
                    with cols[i % 2]:
                        if st.button(topic, key=f"rt_{i}", type="secondary", use_container_width=True):
                            st.session_state.topic_input_pending = topic
                            st.session_state.results = {}
                            st.session_state.running = True
                            st.session_state.done = False
                            st.rerun()
        else:
            st.caption("No related topics generated.")


# ── Main app ──────────────────────────────────────────────────────────────────

def render_app() -> None:
    st.set_page_config(
        page_title="ResearchBuddy · AI Research Agent",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    _init_state()
    _render_sidebar()
    _render_header()

    col_input, col_spacer, col_pipeline = st.columns([5, 0.4, 4])
    with col_input:
        run_clicked = _render_input_column()
    with col_pipeline:
        _render_pipeline_column()

    _run_pipeline_if_needed(run_clicked)
    _render_results()


if __name__ == "__main__":
    render_app()
