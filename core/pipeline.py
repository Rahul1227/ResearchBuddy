from __future__ import annotations

import time

from core.agents import (
    build_search_agent,
    critic_chain,
    entities_chain,
    key_stats_chain,
    reader_synthesis_chain,
    related_topics_chain,
    writer_chain,
)
from core.models import PipelineResult, ResearchOptions, SourceDocument
from services.research_tools import enrich_sources, format_search_results, search_web


def _safe_invoke(chain, inputs: dict, fallback: str = "") -> str:
    try:
        return chain.invoke(inputs)
    except Exception as exc:
        return f"{fallback} [Error: {exc}]"


def build_source_dossier(sources: list[SourceDocument]) -> str:
    if not sources:
        return "No source dossier available."
    chunks = []
    for i, src in enumerate(sources, start=1):
        chunks.append(
            f"Source {i}: {src.title}\n"
            f"URL: {src.url}\n"
            f"Snippet: {src.snippet}\n"
            f"Extracted Content: {src.content}"
        )
    return "\n\n".join(chunks)


def build_focus_context(options: ResearchOptions) -> str:
    if not options.focus_areas:
        return "No special focus areas. Optimise for breadth, relevance, and depth."
    return ", ".join(options.focus_areas)


def run_pipeline_step(step_index: int, topic: str, options: ResearchOptions, data: dict) -> tuple[dict, dict]:
    """Run one step of the pipeline.

    Returns (result_updates, updated_data) where result_updates is merged into
    st.session_state.results and updated_data replaces st.session_state.pipeline_data.
    """
    data = dict(data)

    if step_index == 0:
        try:
            search_agent = build_search_agent()
            response = search_agent.invoke(
                {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
            )
            search_overview: str = response["messages"][-1].content
        except Exception as exc:
            search_overview = f"Search agent encountered an error: {exc}"

        search_results = search_web(topic, max_results=options.source_count + 2) or []
        enriched_sources = enrich_sources(
            search_results,
            max_sources=options.source_count,
            scrape_limit=options.scrape_limit,
        )
        data["search_overview"]  = search_overview
        data["enriched_sources"] = enriched_sources
        data["search_digest"]    = format_search_results(search_results)
        data["source_dossier"]   = build_source_dossier(enriched_sources)
        data["focus_context"]    = build_focus_context(options)

        sources_as_dicts = [
            s.model_dump() if hasattr(s, "model_dump") else vars(s)
            for s in enriched_sources
        ]
        updates = {"search": search_overview, "sources": sources_as_dicts, "topic": topic}
        return updates, data

    if step_index == 1:
        reader_synthesis = _safe_invoke(
            reader_synthesis_chain,
            {
                "topic":           topic,
                "focus_context":   data["focus_context"],
                "search_overview": f"{data['search_overview']}\n\nStructured Results:\n{data['search_digest']}",
                "source_dossier":  data["source_dossier"],
            },
            fallback="Reader synthesis unavailable.",
        )
        data["reader_synthesis"] = reader_synthesis
        return {"reader": reader_synthesis}, data

    if step_index == 2:
        report = _safe_invoke(
            writer_chain,
            {
                "topic":                    topic,
                "target_words":             options.target_words,
                "report_length":            options.report_length,
                "focus_context":            data["focus_context"],
                "include_comparison_table": "yes" if options.include_comparison_table else "no",
                "search_overview":          data["search_overview"],
                "reader_synthesis":         data["reader_synthesis"],
                "source_dossier":           data["source_dossier"],
            },
            fallback="Report generation unavailable.",
        )
        data["report"] = report
        opts_dict = {
            "report_length": options.report_length,
            "target_words":  options.target_words,
            "focus_areas":   options.focus_areas,
        }
        return {"writer": report, "options": opts_dict}, data

    if step_index == 3:
        critic_feedback = _safe_invoke(
            critic_chain,
            {"report": data["report"]},
            fallback="Critic feedback unavailable.",
        )
        data["critic_feedback"] = critic_feedback
        return {"critic": critic_feedback}, data

    if step_index == 4:
        entities = _safe_invoke(
            entities_chain,
            {"report": data["report"][:8000]},
            fallback="",
        )
        data["entities"] = entities
        return {"entities": entities}, data

    if step_index == 5:
        related_topics = _safe_invoke(
            related_topics_chain,
            {"topic": topic, "report_excerpt": data["report"][:3000]},
            fallback="",
        )
        key_stats = _safe_invoke(
            key_stats_chain,
            {"report": data["report"][:6000]},
            fallback="",
        )
        return {"topics": related_topics, "stats": key_stats}, data

    raise ValueError(f"Invalid step_index: {step_index}")


def run_research_pipeline(topic: str, options: ResearchOptions | None = None) -> dict:
    t0 = time.time()
    options = options or ResearchOptions()

    # ── Step 1: Search ────────────────────────────────────────────────────────
    try:
        search_agent = build_search_agent()
        search_response = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
        )
        search_overview: str = search_response["messages"][-1].content
    except Exception as exc:
        search_overview = f"Search agent encountered an error: {exc}"

    search_results = search_web(topic, max_results=options.source_count + 2) or []

    enriched_sources = enrich_sources(
        search_results,
        max_sources=options.source_count,
        scrape_limit=options.scrape_limit,
    )
    search_digest  = format_search_results(search_results)
    source_dossier = build_source_dossier(enriched_sources)
    focus_context  = build_focus_context(options)

    # ── Step 2: Reader Synthesis ──────────────────────────────────────────────
    reader_synthesis = _safe_invoke(
        reader_synthesis_chain,
        {
            "topic":          topic,
            "focus_context":  focus_context,
            "search_overview": f"{search_overview}\n\nStructured Results:\n{search_digest}",
            "source_dossier": source_dossier,
        },
        fallback="Reader synthesis unavailable.",
    )

    # ── Step 3: Writer ────────────────────────────────────────────────────────
    report = _safe_invoke(
        writer_chain,
        {
            "topic":                   topic,
            "target_words":            options.target_words,
            "report_length":           options.report_length,
            "focus_context":           focus_context,
            "include_comparison_table": "yes" if options.include_comparison_table else "no",
            "search_overview":         search_overview,
            "reader_synthesis":        reader_synthesis,
            "source_dossier":          source_dossier,
        },
        fallback="Report generation unavailable.",
    )

    # ── Step 4: Critic ────────────────────────────────────────────────────────
    critic_feedback = _safe_invoke(
        critic_chain,
        {"report": report},
        fallback="Critic feedback unavailable.",
    )

    # ── Step 5: Entity Extraction ─────────────────────────────────────────────
    entities = _safe_invoke(
        entities_chain,
        {"report": report[:8000]},
        fallback="",
    )

    # ── Step 6: Related Topics ────────────────────────────────────────────────
    related_topics = _safe_invoke(
        related_topics_chain,
        {"topic": topic, "report_excerpt": report[:3000]},
        fallback="",
    )

    # ── Step 7: Key Statistics ────────────────────────────────────────────────
    key_stats = _safe_invoke(
        key_stats_chain,
        {"report": report[:6000]},
        fallback="",
    )

    elapsed = round(time.time() - t0, 1)

    return PipelineResult(
        topic=topic,
        search_overview=search_overview,
        reader_synthesis=reader_synthesis,
        report=report,
        critic_feedback=critic_feedback,
        options=options,
        sources=enriched_sources,
        entities=entities,
        related_topics=related_topics,
        key_stats=key_stats,
        elapsed_seconds=elapsed,
    ).as_dict()


def main() -> None:
    topic = input("\nEnter a research topic: ").strip()
    results = run_research_pipeline(topic)

    for section, key in [
        ("SEARCH OVERVIEW",   "search"),
        ("READER SYNTHESIS",  "reader"),
        ("FINAL REPORT",      "writer"),
        ("CRITIC FEEDBACK",   "critic"),
        ("ENTITIES",          "entities"),
        ("RELATED TOPICS",    "topics"),
    ]:
        print(f"\n{'='*60}\n{section}\n{'='*60}")
        print(results.get(key, ""))

    print(f"\nCompleted in {results.get('elapsed', '?')}s")


if __name__ == "__main__":
    main()
