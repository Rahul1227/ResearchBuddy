from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = "ResearchBuddy"
    app_tagline: str = "Multi-Agent AI Research System"
    google_api_key: str | None = os.getenv("GOOGLE_API_KEY")
    tavily_api_key: str | None = os.getenv("TAVILY_API_KEY")
    model_name: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    search_results_limit: int = int(os.getenv("SEARCH_RESULTS_LIMIT", "6"))
    scraped_sources_limit: int = int(os.getenv("SCRAPED_SOURCES_LIMIT", "3"))
    scrape_character_limit: int = int(os.getenv("SCRAPE_CHARACTER_LIMIT", "5000"))


settings = Settings()
