from __future__ import annotations

from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from core.config import settings
from services.research_tools import scrape_url, web_search

_NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"


def get_llm(temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(
        model=settings.model_name,
        api_key=settings.nvidia_api_key,
        base_url=_NVIDIA_BASE_URL,
        temperature=temperature,
        max_tokens=16384,
        model_kwargs={"top_p": 1.0, "reasoning_effort": "high"},
    )


def build_search_agent():
    return create_agent(model=get_llm(), tools=[web_search])


def build_reader_agent():
    return create_agent(model=get_llm(), tools=[scrape_url])


# ── Reader Synthesis ──────────────────────────────────────────────────────────

reader_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a senior research analyst. Synthesize source material into a high-signal briefing. "
        "Compare sources, call out uncertainty, and preserve important facts, dates, and names.",
    ),
    (
        "human",
        """Topic: {topic}

Research Goals:
{focus_context}

Search Overview:
{search_overview}

Source Dossier:
{source_dossier}

Produce a synthesis covering:
- What matters most right now
- Consensus and disagreements across sources
- Key evidence, data, and concrete examples
- Emerging patterns, second-order effects, and strategic implications
- Gaps, caveats, or claims requiring verification
- URLs worth citing directly
""",
    ),
])
reader_synthesis_chain = reader_prompt | get_llm() | StrOutputParser()


# ── Writer ────────────────────────────────────────────────────────────────────

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Produce detailed, well-structured markdown reports "
        "that read like polished analyst briefings. Use only evidence provided — never invent facts.",
    ),
    (
        "human",
        """Write a comprehensive research report on the topic below.

Topic: {topic}

Report Target:
- Target length: at least {target_words} words
- Report mode: {report_length}
- Focus areas: {focus_context}
- Include comparison table: {include_comparison_table}

Search Overview:
{search_overview}

Analyst Synthesis:
{reader_synthesis}

Primary Source Notes:
{source_dossier}

Requirements:
- Use markdown headings and subheadings throughout.
- Open with a concise Executive Summary.
- Include at least 5 substantive findings with implications and concrete examples.
- Include a comparison or summary table where data supports it.
- Include a section titled **Strategic Implications** or **Why This Matters**.
- Include a section on risks, limitations, or open questions.
- End with **Next Steps / Practical Takeaways**.
- Close with a **Sources** section listing every URL referenced.
- Keep the tone factual, professional, and nuanced.
- This is a long-form report — honour the target word count.
""",
    ),
])
writer_chain = writer_prompt | get_llm() | StrOutputParser()


# ── Critic ────────────────────────────────────────────────────────────────────

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a demanding but constructive research editor. Evaluate reports for factual grounding, "
        "clarity, structure, coverage, and practical usefulness.",
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

Missing Angles:
- ...
- ...

One line verdict:
...""",
    ),
])
critic_chain = critic_prompt | get_llm() | StrOutputParser()


# ── Entity Extractor ──────────────────────────────────────────────────────────

entities_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an information-extraction specialist. Extract structured entities from research content "
        "with high precision. Only include entities explicitly mentioned in the text.",
    ),
    (
        "human",
        """Extract notable entities from the research report below.

Report:
{report}

Format your response with these labelled sections.
List each entry on its own line starting with "- ":

PEOPLE:
- [Full name] — [role or context]

ORGANIZATIONS:
- [Name] — [type or context]

TECHNOLOGIES:
- [Name] — [what it is]

DATES:
- [Date/period] — [significance]

STATISTICS:
- [Metric/number] — [what it measures]

PLACES:
- [Location] — [relevance]

Keep each section to the 5–7 most important entries. Only include sections that have meaningful data.
""",
    ),
])
entities_chain = entities_prompt | get_llm(temperature=0.1) | StrOutputParser()


# ── Related Topics ────────────────────────────────────────────────────────────

related_topics_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a research librarian who suggests specific, insightful follow-up research directions.",
    ),
    (
        "human",
        """Based on this research on "{topic}", suggest exactly 6 related topics for deeper investigation.

Report excerpt:
{report_excerpt}

Output exactly 6 numbered lines in this format:
1. [Specific Topic Name] — [one sentence on why it's relevant]
2. ...

Make topics specific and actionable. Avoid generic or vague suggestions.
""",
    ),
])
related_topics_chain = related_topics_prompt | get_llm(temperature=0.4) | StrOutputParser()


# ── Key Statistics Extractor ──────────────────────────────────────────────────

stats_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You extract the most important quantitative facts from research reports.",
    ),
    (
        "human",
        """Extract the 5 most important statistics, numbers, or quantitative findings from this report.

Report:
{report}

Return a simple list, one per line:
- [Statistic or number] ([brief context])

Only include numbers explicitly stated in the report.
""",
    ),
])
key_stats_chain = stats_prompt | get_llm(temperature=0.0) | StrOutputParser()
