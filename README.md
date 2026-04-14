# ResearchBuddy — Multi-Agent AI Research System

ResearchBuddy is an intelligent research automation tool powered by a multi-agent pipeline. It takes any topic as input and automatically searches the web, scrapes key sources, writes a structured research report, and then critically evaluates it — all in one pipeline run.

Built with **LangChain**, **Google Gemini (gemini-2.5-flash)**, **Tavily Search**, and **Streamlit**.

---

## How It Works

The pipeline runs four specialized agents in sequence:

```
[Your Topic]
     ↓
[1] Search Agent     → Queries the web using Tavily and returns top results
     ↓
[2] Reader Agent     → Picks the best URL and deep-scrapes its content
     ↓
[3] Writer Chain     → Combines all data and writes a structured markdown report
     ↓
[4] Critic Chain     → Reviews the report and gives a quality score + feedback
     ↓
[Final Report + Feedback]
```

---

## Features

- Automated web search via **Tavily API**
- Intelligent URL selection and **web scraping** with BeautifulSoup
- Structured **research report** generation (Introduction, Key Findings, Conclusion, Sources)
- Built-in **AI critic** that scores and reviews the report (X/10)
- Clean **Streamlit web UI** with step-by-step progress tracking
- **CLI mode** for programmatic or scripted usage
- One-click **markdown download** of the final report

---

## Project Structure

```
ResearchBuddy/
├── app.py              # Streamlit web UI
├── pipeline.py         # CLI pipeline runner
├── agents.py           # All agent and chain definitions
├── tools.py            # web_search and scrape_url tools
├── requirements.txt    # Python dependencies
├── .env                # API keys 
└── .gitignore
```

---

## Prerequisites

- Python 3.10 or higher
- A **Google AI API key** (for Gemini) — get one at [aistudio.google.com](https://aistudio.google.com)
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
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

> The `.env` file is listed in `.gitignore` and will never be committed to version control.

---

## Running the App

### Option A — Streamlit Web UI (recommended)

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`.

1. Type a research topic in the input box
2. Click **Run Research Pipeline**
3. Watch each stage complete in real time
4. Read the final report and critic feedback
5. Download the report as a `.md` file

### Option B — Command Line

```bash
python pipeline.py
```

You will be prompted to enter a topic. The pipeline runs and prints all outputs to the terminal.

---

## Example Topics

- `"Latest advancements in quantum computing"`
- `"Impact of artificial intelligence on healthcare"`
- `"Climate change and renewable energy solutions"`
- `"History and future of space exploration"`

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Google Gemini `gemini-2.5-flash` |
| Agent Framework | LangChain |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup4 + requests |
| UI | Streamlit |
| Env Management | python-dotenv |

---

## Notes

- The system uses `temperature=0` for deterministic, factual outputs.
- Web scraping is limited to 3000 characters of clean text per URL to keep context concise.
- Search results are capped at 5 results to balance coverage and speed.
