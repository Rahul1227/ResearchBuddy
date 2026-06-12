# ResearchBuddy — Multi-Agent AI Research System

ResearchBuddy is an intelligent research automation tool powered by a six-step multi-agent pipeline. Enter any topic and the system automatically searches the web, scrapes and synthesizes sources, writes a structured long-form report, critically reviews it, extracts key entities and statistics, and suggests follow-up research directions — all in one run.

Built with **LangChain**, **Mistral Medium 3.5 (via NVIDIA NIM)**, **Tavily Search**, and **Streamlit**.

---

## How It Works

Six specialized agents run in sequence, each building on the work of the previous step:

```
[Your Topic]
     ↓
[01] Search Agent      → Queries the web via Tavily and summarizes top results
     ↓
[02] Reader Analyst    → Scrapes all sources and synthesizes a structured briefing
     ↓
[03] Writer Chain      → Writes a long-form, evidence-based markdown report
     ↓
[04] Critic Chain      → Reviews the report and gives a quality score (X/10)
     ↓
[05] Entity Extractor  → Maps people, orgs, technologies, stats, dates & places
     ↓
[06] Topic Suggester   → Generates six follow-up research directions
     ↓
[Final Report + Analysis + Sources + Citations + Related Topics]
```

---

## Features

- Automated web search via **Tavily API** with advanced search depth
- Full **multi-source scraping** using BeautifulSoup — cleans navigation, ads, and footers
- **Reader Analyst** synthesizes all sources into a structured research briefing before writing
- Configurable **report length**: Standard (~1200 words), Detailed (~1800), Deep Dive (~2600)
- Optional **comparison table** and up to 8 selectable **focus areas** (market impact, risks, ethics, etc.)
- Built-in **AI critic** that scores and reviews every report out of 10
- **Entity extraction** across six categories: people, organizations, technologies, statistics, dates, and places
- **Key statistics** panel extracted from the report
- Six **clickable follow-up topics** that instantly start a new research session
- Dark space-themed **Streamlit UI** with real-time step-by-step pipeline progress
- **Research history sidebar** — stores up to 20 previous sessions, each reloadable without re-running
- **Five results tabs**: Report, Analysis, Sources, Citations, Related Topics
- One-click download of the report as a **markdown file** or **styled HTML file**
- Full **CLI mode** for scripted or terminal usage

---

## Project Structure

```
ResearchBuddy/
├── core/
│   ├── agents.py              # All LLM chains and agents (search, reader, writer, critic, entities, topics)
│   ├── config.py              # Settings and environment variable loading
│   ├── models.py              # Pydantic data models (PipelineResult, ResearchOptions, SourceDocument)
│   └── pipeline.py            # Step-by-step and full pipeline orchestration
├── services/
│   └── research_tools.py      # Tavily web search + BeautifulSoup scraping helpers
├── ui/
│   ├── app.py                 # Streamlit app composition and session state management
│   ├── components.py          # Reusable UI blocks (score circle, source cards, entity tags, etc.)
│   └── styles.py              # CSS styling (dark theme with orange accents)
├── generate_report.py         # Generates the formal project report PDF (reportlab)
├── requirements.txt
├── .env
└── .gitignore
```

---

## Prerequisites

- Python 3.10 or higher
- An **NVIDIA API key** (for NVIDIA NIM / Mistral) — get one at [build.nvidia.com](https://build.nvidia.com)
- A **Tavily API key** (for web search) — get one at [tavily.com](https://tavily.com)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rahul1227/ResearchBuddy.git
cd ResearchBuddy
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root:

```
NVIDIA_API_KEY=your_nvidia_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> The `.env` file is listed in `.gitignore` and will never be committed to version control.

---

## Running the App

### Option A — Streamlit Web UI (recommended)

```bash
streamlit run ui/app.py
```

Then open your browser at `http://localhost:8501`.

1. Type a research topic — or click one of the **Try an Example** buttons
2. Optionally expand **Advanced Research Settings** to tune the report
3. Click **Run Research Pipeline** and watch each stage complete in real time
4. Browse results across the Report, Analysis, Sources, Citations, and Related Topics tabs
5. Download the report as `.md` or `.html`, or click a related topic to start a new run

### Option B — Command Line

```bash
python -m core.pipeline
```

You will be prompted to enter a topic. The pipeline runs and prints all outputs to the terminal.

---

## Advanced Settings

| Setting | Options | What It Controls |
|---|---|---|
| Report Length | Standard / Detailed / Deep Dive | Target word count (~1200 / ~1800 / ~2600) |
| Sources to Analyse | 3–8 | Number of web sources to scrape and analyze |
| Content Extract Per Source | 3000–10000 chars | How much text to read from each page |
| Comparison Table | On / Off | Whether to include a summary table in the report |
| Focus Areas | 8 selectable options | Which angles to emphasize (risks, market, ethics, etc.) |

---

## Example Topics

- `"LLM agents 2025"`
- `"CRISPR gene editing"`
- `"Fusion energy progress"`
- `"Quantum computing breakthroughs"`

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral Medium 3.5 `mistralai/mistral-medium-3.5-128b` (NVIDIA NIM) |
| Agent Framework | LangChain |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup4 + requests |
| Data Validation | Pydantic |
| UI | Streamlit |
| Env Management | python-dotenv |

---

## Notes

- All agents use `temperature=0` to `temperature=0.4` depending on the task — lower for precision (entity extraction), higher for creativity (topic suggestions).
- The pipeline synthesizes multiple scraped sources before writing the final report, rather than relying on a single URL.
- Web scraping is limited to a configurable character budget per source to keep context concise.
- All pipeline steps are wrapped in safe error handling — a single failed step produces a fallback message and does not crash the run.
- The Tavily search function uses automatic retry with exponential backoff to handle transient API errors.
