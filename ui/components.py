from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import datetime

import streamlit as st


def _html(markup: str) -> None:
    """Render raw HTML via st.markdown, safe against Markdown code-block detection."""
    clean = "\n".join(ln.lstrip() for ln in markup.strip().splitlines())
    st.markdown(clean, unsafe_allow_html=True)


# ── Step Card ────────────────────────────────────────────────────────────────

STEP_ICONS = {
    "search":   "🔍",
    "reader":   "📖",
    "writer":   "✍",
    "critic":   "🎯",
    "entities": "🏷",
    "topics":   "🔭",
}


def render_step_card(num: str, title: str, state: str, description: str = "", key: str = "") -> None:
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
    }
    label, css_class = status_map.get(state, ("", ""))
    card_class = {"running": "active", "done": "done"}.get(state, "")
    icon = STEP_ICONS.get(key, "◆")
    scan_html = '<div class="step-scan"></div>' if state == "running" else ""
    desc_html = (
        f'<div class="step-desc">{description}</div>' if description else ""
    )
    _html(
        f'<div class="step-card {card_class}">'
        f'{scan_html}'
        f'<div class="step-header">'
        f'<div class="step-icon">{icon}</div>'
        f'<div><span class="step-num">{num}</span>'
        f'<span class="step-title" style="margin-left:.4rem">{title}</span></div>'
        f'<span class="step-status {css_class}">{label}</span>'
        f'</div>'
        f'{desc_html}'
        f'</div>'
    )


# ── Pipeline Progress Bar ─────────────────────────────────────────────────────

def render_progress_bar(done: int, total: int) -> None:
    pct = int(done / total * 100) if total else 0
    _html(
        f'<div class="pipe-progress-wrap">'
        f'<div class="pipe-progress-bar" style="width:{pct}%"></div>'
        f'</div>'
    )


# ── Metrics Grid ──────────────────────────────────────────────────────────────

def render_metrics(metrics: Iterable[tuple[str, str]], title: str = "Research Snapshot") -> None:
    cards = "".join(
        f'<div class="metric-card"><div class="metrics-kicker">{lbl}</div>'
        f'<div class="metric-value">{val}</div></div>'
        for lbl, val in metrics
    )
    _html(
        f'<div class="metrics-shell">'
        f'<div class="panel-label orange">{title}</div>'
        f'<div class="report-meta-grid">{cards}</div>'
        f'</div>'
    )


# ── Source Card ───────────────────────────────────────────────────────────────

_TRUSTED_DOMAINS = {
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov", "arxiv.org",
    "acm.org", "ieee.org", "nih.gov", "who.int", "harvard.edu", "mit.edu",
    "stanford.edu", "ox.ac.uk", "cam.ac.uk", "ft.com", "reuters.com",
    "apnews.com", "bbc.com", "nytimes.com", "theguardian.com",
    "wired.com", "techcrunch.com", "arstechnica.com",
}

def _source_badge(domain: str) -> str:
    if domain in _TRUSTED_DOMAINS:
        return '<span class="source-badge badge-high">Authoritative</span>'
    if any(domain.endswith(tld) for tld in (".edu", ".gov", ".org")):
        return '<span class="source-badge badge-med">Institutional</span>'
    return '<span class="source-badge badge-low">Web</span>'


def render_source_card(source: dict, index: int) -> None:
    domain = source.get("domain", "Unknown domain")
    url    = source.get("url", "")
    url_html = f'<a href="{url}" target="_blank">{url}</a>' if url else ""
    _html(
        f'<div class="source-card">'
        f'<div class="source-card-top">'
        f'<span class="source-index">Source {index}</span>'
        f'<span class="source-domain">{domain}</span>'
        f'{_source_badge(domain)}'
        f'</div>'
        f'<div class="source-title">{source.get("title", "Untitled source")}</div>'
        f'<div class="source-snippet">{source.get("snippet", "")}</div>'
        f'<div class="source-url">{url_html}</div>'
        f'</div>'
    )


# ── Entity Tags ───────────────────────────────────────────────────────────────

_ENTITY_CSS = {
    "people":        ("ep", "People"),
    "person":        ("ep", "People"),
    "organizations": ("eo", "Organizations"),
    "organization":  ("eo", "Organizations"),
    "technologies":  ("et", "Technologies"),
    "technology":    ("et", "Technologies"),
    "dates":         ("ed", "Key Dates"),
    "date":          ("ed", "Key Dates"),
    "statistics":    ("es", "Statistics"),
    "statistic":     ("es", "Statistics"),
    "places":        ("el", "Places"),
    "place":         ("el", "Places"),
}


def render_entities(entities_text: str) -> None:
    if not entities_text or not entities_text.strip():
        return

    sections: dict[str, list[str]] = {}
    current_key = ""
    for line in entities_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Detect category headers like "PEOPLE:" or "ORGANIZATIONS:"
        upper = line.upper().rstrip(":")
        matched_key = next(
            (k for k in _ENTITY_CSS if upper.startswith(k.upper())), None
        )
        if matched_key:
            current_key = matched_key
            sections.setdefault(current_key, [])
        elif current_key and line.startswith("-"):
            item = line.lstrip("- ").strip()
            if item:
                sections[current_key].append(item)
        elif current_key and not line.endswith(":"):
            # comma-separated on same line
            items = [i.strip() for i in line.split(",") if i.strip()]
            sections[current_key].extend(items)

    if not sections:
        st.caption(entities_text)
        return

    html_parts = ['<div class="entity-section">']
    for key, items in sections.items():
        if not items:
            continue
        css_class, label = _ENTITY_CSS.get(key, ("et", key.title()))
        html_parts.append(f'<div class="entity-category">{label}</div>')
        html_parts.append('<div class="entity-grid">')
        for item in items[:8]:
            # Use just the name part before " — " if present
            tag_text = item.split("—")[0].split("–")[0].strip()
            if tag_text:
                html_parts.append(f'<span class="entity-tag {css_class}">{tag_text}</span>')
        html_parts.append('</div>')
    html_parts.append('</div>')
    _html("".join(html_parts))


# ── Related Topics ────────────────────────────────────────────────────────────

def parse_related_topics(topics_text: str) -> list[str]:
    topics = []
    for line in topics_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Strip leading numbering like "1." or "1)"
        cleaned = re.sub(r"^\d+[\.\)]\s*", "", line)
        # Take just the topic name before " — "
        topic_name = cleaned.split("—")[0].split("–")[0].strip()
        if topic_name and len(topic_name) > 4:
            topics.append(topic_name)
    return topics[:6]


def render_related_topics_display(topics_text: str) -> None:
    topics = parse_related_topics(topics_text)
    if not topics:
        st.caption("No related topics generated.")
        return

    chips = "".join(
        f'<div class="related-chip"><span class="related-num">{i+1}.</span>{t}</div>'
        for i, t in enumerate(topics)
    )
    _html(
        f'<div class="related-shell">'
        f'<div class="panel-label orange">Follow-Up Research Directions</div>'
        f'<div class="related-desc">Topics worth exploring next — click any below to research it.</div>'
        f'<div class="related-grid">{chips}</div>'
        f'</div>'
    )


# ── Citations ─────────────────────────────────────────────────────────────────

def render_citations(sources: list[dict]) -> None:
    if not sources:
        st.caption("No sources to cite.")
        return

    year = datetime.now().year
    items_html = ""
    for i, src in enumerate(sources, start=1):
        title  = src.get("title", "Untitled")
        domain = src.get("domain", "")
        url    = src.get("url", "")
        url_link = f'<a href="{url}" target="_blank">{url}</a>' if url else url
        items_html += (
            f'<div class="citation-item">'
            f'  <span class="citation-num-tag">[{i}]</span>'
            f'  <span>{title}. <em>{domain}</em>. {year}. {url_link}</span>'
            f'</div>'
        )

    _html(
        f'<div class="citation-shell">'
        f'<div class="panel-label orange">Source Citations</div>'
        f'<div class="citation-list">{items_html}</div>'
        f'</div>'
    )


# ── Score Circle ──────────────────────────────────────────────────────────────

def render_score_circle(critic_text: str) -> None:
    match = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", critic_text, re.IGNORECASE)
    score_str = match.group(1) if match else "?"

    verdict_match = re.search(r"One line verdict[:\s]+(.+?)(?:\n|$)", critic_text, re.IGNORECASE)
    verdict = verdict_match.group(1).strip() if verdict_match else ""

    _html(
        f'<div class="score-display">'
        f'<div class="score-circle">{score_str}'
        f'<span style="font-size:.75rem;opacity:.6">/10</span></div>'
        f'<div class="score-info">'
        f'<div class="score-label">Quality Score</div>'
        f'<div class="score-verdict">{verdict}</div>'
        f'</div>'
        f'</div>'
    )


# ── Reading Time ──────────────────────────────────────────────────────────────

def reading_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"
