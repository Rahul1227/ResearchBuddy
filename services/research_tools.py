from __future__ import annotations

import os
import time

import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from tenacity import retry, stop_after_attempt, wait_exponential
from tavily import TavilyClient

from core.config import settings
from core.models import SourceDocument

_tavily_client = TavilyClient(api_key=settings.tavily_api_key or os.getenv("TAVILY_API_KEY"))

# Domains considered highly authoritative for badge display
AUTHORITATIVE_DOMAINS = frozenset({
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov", "arxiv.org",
    "acm.org", "ieee.org", "nih.gov", "who.int", "cdc.gov",
    "harvard.edu", "mit.edu", "stanford.edu", "ox.ac.uk", "cam.ac.uk",
    "ft.com", "reuters.com", "apnews.com", "bbc.com", "nytimes.com",
    "theguardian.com", "wired.com", "techcrunch.com", "arstechnica.com",
    "economist.com", "wsj.com", "bloomberg.com",
})


def score_source(domain: str) -> str:
    if domain in AUTHORITATIVE_DOMAINS:
        return "high"
    if any(domain.endswith(tld) for tld in (".edu", ".gov", ".org")):
        return "med"
    return "low"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def _tavily_search(query: str, max_results: int) -> dict:
    return _tavily_client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced",
    )


def search_web(query: str, max_results: int | None = None) -> list[SourceDocument]:
    try:
        results = _tavily_search(query, max_results or settings.search_results_limit)
    except Exception as exc:
        print(f"[search_web] Tavily error: {exc}")
        return []

    documents: list[SourceDocument] = []
    for item in results.get("results", []):
        documents.append(
            SourceDocument(
                title=item.get("title", "Untitled result"),
                url=item.get("url", ""),
                snippet=item.get("content", "").strip()[:420],
            )
        )
    return documents


def format_search_results(results: list[SourceDocument]) -> str:
    if not results:
        return "No search results were returned."
    chunks = []
    for i, item in enumerate(results, start=1):
        chunks.append(
            f"[{i}] {item.title}\nURL: {item.url}\nSnippet: {item.snippet}"
        )
    return "\n\n---\n\n".join(chunks)


def scrape_url_content(url: str, limit: int | None = None) -> str:
    try:
        resp = requests.get(
            url,
            timeout=12,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36"
                )
            },
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript", "form", "button"]):
            tag.decompose()
        # Prefer main / article content if available
        main = soup.find("main") or soup.find("article") or soup
        text = main.get_text(separator=" ", strip=True)
        clean_text = " ".join(text.split())
        return clean_text[: limit or settings.scrape_character_limit]
    except requests.exceptions.Timeout:
        return "Could not scrape URL: request timed out."
    except requests.exceptions.HTTPError as exc:
        return f"Could not scrape URL: HTTP {exc.response.status_code}."
    except Exception as exc:
        return f"Could not scrape URL: {exc}"


def enrich_sources(
    results: list[SourceDocument],
    max_sources: int | None = None,
    scrape_limit: int | None = None,
) -> list[SourceDocument]:
    enriched: list[SourceDocument] = []
    cap = max_sources or settings.scraped_sources_limit
    for item in results[:cap]:
        content = scrape_url_content(item.url, limit=scrape_limit)
        enriched.append(
            SourceDocument(
                title=item.title,
                url=item.url,
                snippet=item.snippet,
                content=content,
            )
        )
        # Brief pause to avoid hammering servers
        time.sleep(0.3)
    return enriched


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic."""
    return format_search_results(search_web(query))


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    return scrape_url_content(url)
