from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ResearchOptions:
    report_length: str = "detailed"
    source_count: int = 4
    scrape_limit: int = 6000
    focus_areas: list[str] = field(default_factory=list)
    include_comparison_table: bool = True

    @property
    def target_words(self) -> int:
        return {"standard": 1200, "detailed": 1800, "deep": 2600}.get(self.report_length, 1800)


@dataclass
class SourceDocument:
    title: str
    url: str
    snippet: str
    content: str = ""

    @property
    def domain(self) -> str:
        value = self.url.replace("https://", "").replace("http://", "")
        return value.split("/")[0]


@dataclass
class PipelineResult:
    topic: str
    search_overview: str
    reader_synthesis: str
    report: str
    critic_feedback: str
    options: ResearchOptions = field(default_factory=ResearchOptions)
    sources: list[SourceDocument] = field(default_factory=list)
    entities: str = ""
    related_topics: str = ""
    key_stats: str = ""
    elapsed_seconds: float = 0.0

    def as_dict(self) -> dict:
        return {
            "topic":    self.topic,
            "search":   self.search_overview,
            "reader":   self.reader_synthesis,
            "writer":   self.report,
            "critic":   self.critic_feedback,
            "entities": self.entities,
            "topics":   self.related_topics,
            "stats":    self.key_stats,
            "elapsed":  self.elapsed_seconds,
            "options": {
                "report_length":           self.options.report_length,
                "source_count":            self.options.source_count,
                "scrape_limit":            self.options.scrape_limit,
                "focus_areas":             self.options.focus_areas,
                "include_comparison_table": self.options.include_comparison_table,
                "target_words":            self.options.target_words,
            },
            "sources": [
                {
                    "title":   s.title,
                    "url":     s.url,
                    "snippet": s.snippet,
                    "content": s.content,
                    "domain":  s.domain,
                }
                for s in self.sources
            ],
        }
