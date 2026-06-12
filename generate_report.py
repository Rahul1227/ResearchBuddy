"""Generate the formal project report PDF for ResearchBuddy."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.platypus import Frame, PageTemplate
from reportlab.platypus.doctemplate import NextPageTemplate
import os

# ── Palette ───────────────────────────────────────────────────────────────────
BLACK      = colors.HexColor("#111111")
BODY       = colors.HexColor("#1A1A1A")
DARK_GREY  = colors.HexColor("#555555")
MID_GREY   = colors.HexColor("#888888")
LIGHT_GREY = colors.HexColor("#F2F2F2")
RULE_GREY  = colors.HexColor("#CCCCCC")
WHITE      = colors.white

PAGE_W, PAGE_H = A4
MARGIN    = 2.5 * cm
CONTENT_W = PAGE_W - 2 * MARGIN


# ── Styles ────────────────────────────────────────────────────────────────────
def build_styles() -> dict:
    S = {}
    S["cover_title"] = ParagraphStyle(
        "cover_title", fontName="Helvetica-Bold", fontSize=34,
        leading=42, textColor=BLACK, alignment=TA_CENTER, spaceAfter=6,
    )
    S["cover_subtitle"] = ParagraphStyle(
        "cover_subtitle", fontName="Helvetica", fontSize=13,
        leading=19, textColor=DARK_GREY, alignment=TA_CENTER, spaceAfter=3,
    )
    S["cover_label"] = ParagraphStyle(
        "cover_label", fontName="Helvetica-Bold", fontSize=9,
        leading=13, textColor=MID_GREY, alignment=TA_CENTER,
        spaceBefore=6, spaceAfter=1,
    )
    S["cover_value"] = ParagraphStyle(
        "cover_value", fontName="Helvetica", fontSize=11,
        leading=16, textColor=BLACK, alignment=TA_CENTER, spaceAfter=2,
    )
    S["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=20,
        leading=26, textColor=BLACK, spaceBefore=0, spaceAfter=4,
    )
    S["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=13,
        leading=18, textColor=BLACK, spaceBefore=14, spaceAfter=3,
    )
    S["h3"] = ParagraphStyle(
        "h3", fontName="Helvetica-Bold", fontSize=11,
        leading=16, textColor=BLACK, spaceBefore=8, spaceAfter=2,
    )
    S["body"] = ParagraphStyle(
        "body", fontName="Helvetica", fontSize=10.5,
        leading=16.5, textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=7,
    )
    S["body_small"] = ParagraphStyle(
        "body_small", fontName="Helvetica", fontSize=10,
        leading=15, textColor=BODY, alignment=TA_JUSTIFY, spaceAfter=5,
    )
    S["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica", fontSize=10.5,
        leading=16, textColor=BODY, leftIndent=16, bulletIndent=4, spaceAfter=3,
    )
    S["bullet_bold"] = ParagraphStyle(
        "bullet_bold", fontName="Helvetica-Bold", fontSize=10.5,
        leading=16, textColor=BLACK, leftIndent=0, spaceAfter=1,
    )
    S["bullet_desc"] = ParagraphStyle(
        "bullet_desc", fontName="Helvetica", fontSize=10.5,
        leading=16, textColor=BODY, leftIndent=16, spaceAfter=7,
    )
    S["caption"] = ParagraphStyle(
        "caption", fontName="Helvetica-Oblique", fontSize=9,
        leading=13, textColor=MID_GREY, alignment=TA_CENTER, spaceAfter=8,
    )
    S["toc_h1"] = ParagraphStyle(
        "toc_h1", fontName="Helvetica-Bold", fontSize=11,
        leading=16, textColor=BLACK,
    )
    S["toc_h2"] = ParagraphStyle(
        "toc_h2", fontName="Helvetica", fontSize=10,
        leading=15, textColor=DARK_GREY, leftIndent=10,
    )
    return S


# ── Header / Footer ───────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE_GREY)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, PAGE_H - 1.5 * cm, PAGE_W - MARGIN, PAGE_H - 1.5 * cm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MID_GREY)
    canvas.drawString(MARGIN, PAGE_H - 1.25 * cm,
                      "ResearchBuddy — Multi-Agent AI Research System")
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 1.25 * cm,
                           "Project Report  |  M.Tech CSE")
    canvas.setStrokeColor(RULE_GREY)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, 1.5 * cm, PAGE_W - MARGIN, 1.5 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GREY)
    canvas.drawCentredString(PAGE_W / 2, 1.0 * cm, str(canvas.getPageNumber()))
    canvas.restoreState()


def on_cover_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(BLACK)
    canvas.setLineWidth(1.5)
    canvas.line(MARGIN, PAGE_H - 1.2 * cm, PAGE_W - MARGIN, PAGE_H - 1.2 * cm)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.2 * cm, PAGE_W - MARGIN, 1.2 * cm)
    canvas.restoreState()


# ── Helpers ───────────────────────────────────────────────────────────────────
def section_rule():
    return HRFlowable(width="100%", thickness=1.0, color=BLACK,
                      spaceAfter=10, spaceBefore=2)


def light_rule():
    return HRFlowable(width="100%", thickness=0.4, color=RULE_GREY,
                      spaceAfter=4, spaceBefore=4)


def b(text: str) -> str:
    return f"<b>{text}</b>"


def bullet(text: str, S: dict) -> Paragraph:
    return Paragraph(f"•  {text}", S["bullet"])


def th_ps(name: str) -> ParagraphStyle:
    return ParagraphStyle(name, fontName="Helvetica-Bold", fontSize=10,
                          textColor=WHITE, alignment=TA_CENTER, leading=14)


def td_ps(name: str = "td") -> ParagraphStyle:
    return ParagraphStyle(name, fontName="Helvetica", fontSize=9.5,
                          leading=14, textColor=BODY)


def table_style(n_data_rows: int) -> TableStyle:
    cmds = [
        ("BACKGROUND",    (0, 0), (-1, 0),  BLACK),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.8, DARK_GREY),
    ]
    for i in range(1, n_data_rows + 1):
        bg = LIGHT_GREY if i % 2 == 1 else WHITE
        cmds.append(("BACKGROUND", (0, i), (-1, i), bg))
    return TableStyle(cmds)


def section_start(story: list, heading: str, S: dict):
    story.append(PageBreak())
    story.append(Paragraph(heading, S["h1"]))
    story.append(section_rule())
    story.append(Spacer(1, 0.1 * cm))


# ── Build Document ────────────────────────────────────────────────────────────
def build_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=2.2 * cm, bottomMargin=2.2 * cm,
        title="ResearchBuddy — Project Report",
        author="Rahul Yadav",
        subject="Multi-Agent AI Research System",
    )
    S = build_styles()
    story = []

    # ── Cover ─────────────────────────────────────────────────────────────────
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H,
                        leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0)
    normal_frame = Frame(MARGIN, 2.0 * cm, CONTENT_W, PAGE_H - 4.0 * cm,
                         leftPadding=0, rightPadding=0,
                         topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate("cover",  frames=[cover_frame],  onPage=on_cover_page),
        PageTemplate("normal", frames=[normal_frame], onPage=on_page),
    ])

    story.append(NextPageTemplate("cover"))
    story.append(Spacer(1, 5.0 * cm))
    story.append(Paragraph("ResearchBuddy", S["cover_title"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Multi-Agent AI Research System", S["cover_subtitle"]))
    story.append(Paragraph("A Detailed Project Report", S["cover_subtitle"]))
    story.append(Spacer(1, 2.5 * cm))
    story.append(HRFlowable(width="40%", thickness=1.0, color=BLACK,
                             spaceAfter=2.5 * cm, spaceBefore=0,
                             hAlign="CENTER"))
    def cover_row(label, value):
        story.append(Paragraph(label, S["cover_label"]))
        story.append(Paragraph(value, S["cover_value"]))

    cover_row("Submitted By",      "Rahul Yadav")
    cover_row("Enrollment Number", "25535037")
    cover_row("Branch",            "M.Tech Computer Science and Engineering")
    cover_row("Date",              "June 2026")

    story.append(NextPageTemplate("normal"))
    story.append(PageBreak())

    # ── Table of Contents ─────────────────────────────────────────────────────
    story.append(Paragraph("Table of Contents", S["h1"]))
    story.append(section_rule())
    story.append(Spacer(1, 0.2 * cm))

    toc_items = [
        ("1",   "Introduction",                    "h1"),
        ("2",   "System Overview",                 "h1"),
        ("3",   "Architecture",                    "h1"),
        ("4",   "The Six-Step Research Pipeline",  "h1"),
        ("4.1", "Step 1: Search Agent",            "h2"),
        ("4.2", "Step 2: Reader Analyst",          "h2"),
        ("4.3", "Step 3: Writer Chain",            "h2"),
        ("4.4", "Step 4: Critic Chain",            "h2"),
        ("4.5", "Step 5: Entity Extractor",        "h2"),
        ("4.6", "Step 6: Topic Suggester",         "h2"),
        ("5",   "Data Flow",                       "h1"),
        ("6",   "Technologies Used",               "h1"),
        ("7",   "User Interface",                  "h1"),
        ("8",   "Key Features",                    "h1"),
        ("9",   "Error Handling and Reliability",  "h1"),
        ("10",  "Configuration and Customization", "h1"),
        ("11",  "Conclusion",                      "h1"),
    ]

    toc_n_h1 = ParagraphStyle("tn1", fontName="Helvetica-Bold", fontSize=10.5,
                               textColor=BLACK, alignment=TA_CENTER, leading=16)
    toc_n_h2 = ParagraphStyle("tn2", fontName="Helvetica", fontSize=10,
                               textColor=MID_GREY, alignment=TA_CENTER, leading=15)

    toc_rows = []
    for num, title, level in toc_items:
        n_ps = toc_n_h1 if level == "h1" else toc_n_h2
        t_ps = S["toc_h1"] if level == "h1" else S["toc_h2"]
        toc_rows.append([Paragraph(num, n_ps), Paragraph(title, t_ps)])

    toc_tbl = Table(toc_rows, colWidths=[CONTENT_W * 0.10, CONTENT_W * 0.90])
    toc_cmds = [
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",  (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]
    for i, (_, _, level) in enumerate(toc_items):
        if level == "h1":
            toc_cmds += [
                ("BACKGROUND",    (0, i), (-1, i), WHITE),
                ("TOPPADDING",    (0, i), (-1, i), 7),
                ("BOTTOMPADDING", (0, i), (-1, i), 7),
                ("LINEBELOW",     (0, i), (-1, i), 0.3, RULE_GREY),
            ]
        else:
            toc_cmds += [
                ("BACKGROUND",    (0, i), (-1, i), LIGHT_GREY),
                ("TOPPADDING",    (0, i), (-1, i), 4),
                ("BOTTOMPADDING", (0, i), (-1, i), 4),
            ]
    toc_tbl.setStyle(TableStyle(toc_cmds))
    story.append(toc_tbl)

    # ── 1. Introduction ───────────────────────────────────────────────────────
    section_start(story, "1.  Introduction", S)

    story.append(Paragraph(
        "ResearchBuddy is a software system that uses multiple artificial intelligence agents "
        "to carry out research on any topic a user provides. Instead of asking a single AI "
        "model to do everything at once, the system breaks the research process into six "
        "clear steps. Each step is handled by a dedicated agent that is good at that specific "
        "task. Together, these agents work in order, passing information from one to the next, "
        "until a complete, well-structured research report is produced.",
        S["body"]))

    story.append(Paragraph(
        "The system is designed to work like a team of human researchers. One agent searches "
        "the web for information. Another reads and understands what was found. A third writes "
        "the report. A fourth reviews it for quality. The remaining two extract key facts and "
        "suggest topics for further study. This division of work makes each part of the process "
        "more focused and produces better results than a single model could achieve alone.",
        S["body"]))

    story.append(Paragraph(
        "ResearchBuddy is built using Python and connects to Google's Gemini language model "
        "for text generation, the Tavily API for web search, and Streamlit for the user "
        "interface. The system produces professional-grade output within one to two minutes "
        "of a user entering their topic.",
        S["body"]))

    story.append(Spacer(1, 0.2 * cm))
    story.append(Paragraph(b("Objectives"), S["h3"]))
    for obj in [
        "Automate the full research workflow from search to report",
        "Use specialized AI agents for each phase of research",
        "Provide results in a clean, readable, downloadable format",
        "Let users adjust settings to control depth and focus of research",
        "Give quality feedback on each generated report automatically",
    ]:
        story.append(bullet(obj, S))

    # ── 2. System Overview ────────────────────────────────────────────────────
    section_start(story, "2.  System Overview", S)

    story.append(Paragraph(
        "ResearchBuddy takes a topic as input and produces four main outputs: a long-form "
        "research report, a quality review of that report, a list of important entities found "
        "in the report, and a set of related topics to explore next. The system also shows the "
        "user a list of all sources it used, complete with titles and links.",
        S["body"]))

    story.append(Paragraph(
        "The system follows a linear pipeline. Each step depends on the output of the previous "
        "step, so the agents run one after another in a fixed order. This ensures that "
        "information is built up gradually and each agent has everything it needs before it "
        "starts working.",
        S["body"]))

    story.append(Spacer(1, 0.2 * cm))

    td = td_ps()
    pipe_rows = [
        [Paragraph(b("Step"), th_ps("th1")), Paragraph(b("Agent"), th_ps("th2")),
         Paragraph(b("What It Does"), th_ps("th3")), Paragraph(b("Output"), th_ps("th4"))],
        [Paragraph("01", td), Paragraph("Search Agent",    td),
         Paragraph("Searches the web for relevant sources",    td),
         Paragraph("Sources list and text summary",            td)],
        [Paragraph("02", td), Paragraph("Reader Analyst",   td),
         Paragraph("Reads all sources and extracts key facts", td),
         Paragraph("Structured research briefing",             td)],
        [Paragraph("03", td), Paragraph("Writer Chain",     td),
         Paragraph("Writes the full research report",          td),
         Paragraph("Detailed markdown report",                 td)],
        [Paragraph("04", td), Paragraph("Critic Chain",     td),
         Paragraph("Reviews the report and gives a score",     td),
         Paragraph("Feedback and quality score",               td)],
        [Paragraph("05", td), Paragraph("Entity Extractor", td),
         Paragraph("Pulls out names, dates, stats, places",    td),
         Paragraph("Labeled entity list",                      td)],
        [Paragraph("06", td), Paragraph("Topic Suggester",  td),
         Paragraph("Recommends six follow-up topics",          td),
         Paragraph("Six topic suggestions",                    td)],
    ]
    col_w = CONTENT_W / 4
    pipe_tbl = Table(pipe_rows,
                     colWidths=[col_w * 0.45, col_w * 1.05, col_w * 1.5, col_w * 1.0])
    pipe_tbl.setStyle(table_style(6))
    story.append(pipe_tbl)
    story.append(Paragraph("Table 1: Summary of the Six-Step Pipeline", S["caption"]))

    story.append(Paragraph(
        "The total time to complete all six steps is typically between 30 and 90 seconds, "
        "depending on how many sources are analyzed and how long the report needs to be. "
        "The user can see the progress of each step in real time through the interface.",
        S["body"]))

    # ── 3. Architecture ───────────────────────────────────────────────────────
    section_start(story, "3.  Architecture", S)

    story.append(Paragraph(
        "The system is divided into three main layers: the core layer, the services layer, "
        "and the user interface layer. Each layer has a clear responsibility and they "
        "communicate through defined interfaces.",
        S["body"]))

    story.append(Spacer(1, 0.2 * cm))

    mono = ParagraphStyle("mono", fontName="Courier", fontSize=9, leading=14,
                           textColor=DARK_GREY)
    arch_rows = [
        [Paragraph(b("Layer"), th_ps("al1")), Paragraph(b("Files"), th_ps("al2")),
         Paragraph(b("Responsibility"), th_ps("al3"))],
        [Paragraph("Core Layer",     td_ps("a1")),
         Paragraph("core/agents.py\ncore/pipeline.py\ncore/models.py\ncore/config.py", mono),
         Paragraph("AI agents, pipeline runner, data structures, and configuration.",
                   td_ps("a2"))],
        [Paragraph("Services Layer", td_ps("b1")),
         Paragraph("services/research_tools.py", mono),
         Paragraph("Web search via Tavily API and content scraping.", td_ps("b2"))],
        [Paragraph("UI Layer",       td_ps("c1")),
         Paragraph("ui/app.py\nui/components.py\nui/styles.py", mono),
         Paragraph("Streamlit interface, reusable display components, and styling.",
                   td_ps("c2"))],
    ]
    arch_tbl = Table(arch_rows,
                     colWidths=[CONTENT_W * 0.20, CONTENT_W * 0.32, CONTENT_W * 0.48])
    arch_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0), BLACK),
        ("BACKGROUND",    (0, 1), (-1, 1), LIGHT_GREY),
        ("BACKGROUND",    (0, 2), (-1, 2), WHITE),
        ("BACKGROUND",    (0, 3), (-1, 3), LIGHT_GREY),
        ("GRID",          (0, 0), (-1, -1), 0.4, RULE_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, 0),  0.8, DARK_GREY),
    ]))
    story.append(arch_tbl)
    story.append(Paragraph("Table 2: System Architecture Layers", S["caption"]))
    story.append(Spacer(1, 0.2 * cm))

    for heading, body_text in [
        ("Core Layer",
         "The core layer is the brain of the system. The file core/agents.py contains all "
         "seven AI chains and agents. Each agent is set up with a carefully written system "
         "prompt that tells the AI exactly what role it should play and what format its output "
         "should follow. The file core/pipeline.py runs all six steps in order and handles any "
         "errors that occur. The file core/models.py defines the data structures used to pass "
         "information between parts of the system. The file core/config.py reads settings from "
         "environment variables so the system can be configured without changing the code."),
        ("Services Layer",
         "The services layer connects the system to the outside world. The file "
         "services/research_tools.py sends search queries to the Tavily API and visits each "
         "source URL to download and clean the page content. Unwanted elements like navigation "
         "menus and advertisements are removed, and the main text is returned for the agents."),
        ("User Interface Layer",
         "The user interface layer is built with Streamlit. The file ui/app.py manages the "
         "main application flow, including reading user input, starting the pipeline, and "
         "displaying results. The file ui/components.py provides reusable display blocks "
         "such as source cards, quality score circles, and entity tags. The file ui/styles.py "
         "contains all the CSS styling."),
    ]:
        story.append(KeepTogether([
            Paragraph(heading, S["h2"]),
            Paragraph(body_text, S["body"]),
        ]))

    # ── 4. Pipeline ───────────────────────────────────────────────────────────
    section_start(story, "4.  The Six-Step Research Pipeline", S)

    story.append(Paragraph(
        "The pipeline is the core workflow of ResearchBuddy. It runs six agents in sequence. "
        "Each agent receives the outputs of the agents that ran before it. This section "
        "explains what each agent does, what inputs it receives, and what output it produces.",
        S["body"]))

    pipeline_steps = [
        ("Step 1: Search Agent",
         "The Search Agent is the first step in the pipeline. Its job is to find relevant "
         "and recent information about the research topic on the web. It uses LangChain's "
         "agent framework with the Tavily web search tool. The agent sends the topic to the "
         "Tavily API, which performs an advanced web search and returns up to eight results. "
         "Each result includes a title, a URL, and a short snippet of text. The agent then "
         "reads all of these results and writes a short summary paragraph capturing the "
         "main findings.",
         [
             "Uses Google Gemini 2.5 Flash as the language model",
             "Search depth is set to advanced for more thorough results",
             "Returns up to eight sources from the web",
             "Temperature is set to 0.2 for consistent, focused output",
         ]),
        ("Step 2: Reader Analyst",
         "The Reader Analyst receives the search results and the full text of each web page "
         "that was found. Before this step runs, the pipeline visits each source URL and "
         "downloads the full page content using a web scraper built with the BeautifulSoup "
         "library. The scraper removes menus, footers, and scripts, keeping only the main "
         "article text. The Reader Analyst then receives all of this cleaned content, the "
         "original search summary, and any focus areas the user selected. It acts as a "
         "senior research analyst and writes a structured briefing.",
         [
             "The most important developments happening right now on the topic",
             "Points of agreement and disagreement across different sources",
             "Key evidence, statistics, and concrete examples",
             "Emerging patterns and second-order effects",
             "Gaps in the available information and important caveats",
         ]),
        ("Step 3: Writer Chain",
         "The Writer Chain is the central agent of the system. It takes everything gathered "
         "so far and writes a complete, long-form research report. It receives the topic, "
         "the search summary, the reader briefing, all source content, the user's focus areas, "
         "and the chosen report length. The agent is instructed never to invent facts or "
         "include anything not supported by the sources.",
         [
             "Standard: approximately 1200 words",
             "Detailed: approximately 1800 words",
             "Deep Dive: approximately 2600 words",
         ]),
        ("Step 4: Critic Chain",
         "The Critic Chain acts as a quality reviewer. After the report is written, it reads "
         "the report and evaluates it against five criteria: factual grounding, clarity of "
         "writing, structure and organization, coverage of the topic, and practical usefulness "
         "to the reader. The quality score is shown as a circle graphic in the Analysis tab.",
         [
             "A score out of ten in the format Score: X/10",
             "A list of strengths found in the report",
             "A list of areas that could be improved",
             "A list of important angles that are missing",
             "A one-line verdict summarizing the overall quality",
         ]),
        ("Step 5: Entity Extractor",
         "The Entity Extractor reads the report and pulls out important named items such as "
         "people, organizations, technologies, statistics, places, and dates. The agent "
         "receives the first 8000 characters of the report and is set to a very low "
         "temperature of 0.1 for precise, consistent output. It only extracts entities "
         "explicitly mentioned in the text.",
         [
             "People: Names along with their roles or titles",
             "Organizations: Names along with their type",
             "Technologies: Names along with a brief description",
             "Dates: Time periods along with their significance",
             "Statistics: Numerical measurements and what they represent",
             "Places: Locations and why they are relevant",
         ]),
        ("Step 6: Topic Suggester",
         "The Topic Suggester is the final step. It reads the report and suggests six specific "
         "topics that the user could explore next. The agent is set to a temperature of 0.4 "
         "to allow slightly more creative suggestions while still staying relevant. Each "
         "suggestion includes a topic name and one sentence explaining why it is worth "
         "exploring. The suggestions appear as clickable buttons in the Related Topics tab.",
         []),
    ]

    for step_title, step_body, step_bullets in pipeline_steps:
        items = [
            Paragraph(step_title, S["h2"]),
            Paragraph(step_body, S["body"]),
        ]
        for b_text in step_bullets:
            items.append(bullet(b_text, S))
        story.append(KeepTogether(items[:3]))
        for item in items[3:]:
            story.append(item)

    # ── 5. Data Flow ──────────────────────────────────────────────────────────
    section_start(story, "5.  Data Flow", S)

    story.append(Paragraph(
        "This section describes how data moves through the system from the moment a user "
        "enters a topic to the moment the final report is displayed.",
        S["body"]))

    story.append(Spacer(1, 0.1 * cm))

    flow_steps = [
        ("1.  User Input",
         "The user types a research topic into the text field and optionally adjusts "
         "settings such as report length, number of sources, content size per source, "
         "whether to include a comparison table, and which focus areas to cover. "
         "These settings are bundled into a ResearchOptions data object."),
        ("2.  Web Search",
         "The pipeline calls the Tavily API with the topic and receives up to eight "
         "search results. Each result contains a title, a URL, and a short text snippet. "
         "These are stored as SourceDocument objects."),
        ("3.  Content Scraping",
         "For each source URL, the scraper downloads the web page, parses the HTML with "
         "BeautifulSoup, removes navigation, footers, ads, and scripts, and returns the "
         "main article text. A short delay of 0.3 seconds is used between requests."),
        ("4.  Search Agent Processing",
         "The Search Agent reads all scraped content and writes a short text summary "
         "of what was found, providing a high-level overview of the topic."),
        ("5.  Data Preparation",
         "Three helper functions prepare data for the Reader Analyst: one builds a "
         "formatted source dossier, one formats the search results into a readable digest, "
         "and one converts the user's focus area selections into a text string."),
        ("6.  Reader Synthesis",
         "The Reader Analyst receives the topic, the search summary, the source dossier, "
         "and the focus context. It produces a structured briefing organizing the most "
         "important information."),
        ("7.  Report Writing",
         "The Writer Chain receives all previous outputs plus the target word count "
         "and produces a full markdown research report."),
        ("8.  Analysis Steps",
         "The Critic Chain, Entity Extractor, and Topic Suggester all run after the "
         "report is written. They receive different portions of the report and produce "
         "their outputs independently."),
        ("9.  Result Aggregation",
         "All outputs are collected into a PipelineResult data object containing the "
         "report, critic feedback, entities, related topics, key statistics, elapsed "
         "time, and the list of sources."),
        ("10.  Display",
         "The Streamlit interface reads the PipelineResult and displays the content "
         "across five tabs. The result is saved to session history for later access."),
    ]

    for step_name, description in flow_steps:
        story.append(KeepTogether([
            Paragraph(b(step_name), S["h3"]),
            Paragraph(description, S["body"]),
        ]))

    # ── 6. Technologies Used ──────────────────────────────────────────────────
    section_start(story, "6.  Technologies Used", S)

    story.append(Paragraph(
        "ResearchBuddy is built using a carefully chosen set of open-source libraries and "
        "cloud APIs. Each technology was selected because it is reliable, well-maintained, "
        "and suited to its specific role in the system.",
        S["body"]))

    for heading, body_text in [
        ("Language Model",
         "All AI agents use Google Gemini 2.5 Flash. This model was chosen because it is "
         "fast, cost-effective, and capable of following complex instructions accurately. "
         "Different agents use different temperature settings — lower values (0.0 to 0.2) "
         "for tasks needing precision such as entity extraction, higher values (0.4) for "
         "tasks that benefit from creativity such as topic suggestion."),
        ("LangChain",
         "LangChain is the agent framework used to build and run the AI chains. "
         "It provides the tools to connect a language model to a system prompt, bind "
         "external tools like web search, parse output, and run chains in sequence. "
         "The system uses LangChain version 0.2 or newer."),
        ("Tavily API",
         "Tavily is a search API designed specifically for use with AI systems. It returns "
         "clean, structured results from the web, including titles, URLs, and content "
         "snippets. ResearchBuddy uses Tavily's advanced search depth setting to get the "
         "most thorough results available."),
        ("BeautifulSoup and Requests",
         "These libraries download and parse web page content. BeautifulSoup reads the "
         "HTML structure of each page and identifies the main article content, removing "
         "menus, advertisements, comment sections, and footers. The requests library "
         "handles the HTTP connections with a timeout to prevent waiting too long for "
         "slow pages."),
        ("Streamlit",
         "Streamlit is a Python library for building interactive web applications. "
         "It converts Python code into a fully functional web interface without requiring "
         "any separate frontend code. ResearchBuddy uses Streamlit version 1.35 or newer "
         "and makes use of its columns, tabs, expanders, session state, and download "
         "button features."),
    ]:
        story.append(KeepTogether([
            Paragraph(heading, S["h2"]),
            Paragraph(body_text, S["body"]),
        ]))

    story.append(Paragraph("Supporting Libraries", S["h2"]))
    mono2 = ParagraphStyle("mono2", fontName="Courier", fontSize=9.5,
                            textColor=DARK_GREY, leading=14)
    tech_data = [
        ("Pydantic",      "2.5.0+", "Data validation and type-safe data structures"),
        ("tiktoken",      "0.6.0+", "Counting tokens in text before sending to the model"),
        ("orjson",        "3.9.0+", "Fast JSON serialization for saving and loading results"),
        ("python-dotenv", "1.0.0+", "Loading API keys from an environment file"),
        ("tenacity",      "8.2.0+", "Automatic retry with backoff for failed API calls"),
        ("aiohttp",       "3.9.0+", "Async HTTP support for concurrent operations"),
        ("lxml",          "latest", "HTML parsing backend used with BeautifulSoup"),
    ]
    tech_rows = [[Paragraph(b("Library"), th_ps("lh1")),
                  Paragraph(b("Version"), th_ps("lh2")),
                  Paragraph(b("Purpose"),  th_ps("lh3"))]]
    for lib, ver, purpose in tech_data:
        tech_rows.append([Paragraph(lib, mono2),
                          Paragraph(ver, td_ps("v")),
                          Paragraph(purpose, td_ps("p"))])
    tech_tbl = Table(tech_rows,
                     colWidths=[CONTENT_W * 0.22, CONTENT_W * 0.15, CONTENT_W * 0.63])
    tech_tbl.setStyle(table_style(len(tech_data)))
    story.append(tech_tbl)
    story.append(Paragraph("Table 3: Supporting Libraries and Their Roles", S["caption"]))

    # ── 7. User Interface ─────────────────────────────────────────────────────
    section_start(story, "7.  User Interface", S)

    story.append(Paragraph(
        "The user interface is built with Streamlit and follows a dark space-themed design. "
        "It is divided into several main areas described below.",
        S["body"]))

    for heading, body_text in [
        ("Header",
         "The top of the page shows the ResearchBuddy name and tagline along with animated "
         "graphics. Below the header is a row of technology badges showing which AI model "
         "and tools are in use."),
        ("Input Area",
         "Below the header, the page splits into two columns. The left column contains the "
         "input controls. The user types their research topic into a text field at the top. "
         "Below the text field is an expandable Advanced Settings section where the user "
         "can fine-tune the research process."),
    ]:
        story.append(KeepTogether([
            Paragraph(heading, S["h2"]),
            Paragraph(body_text, S["body"]),
        ]))

    settings_data = [
        ("Report Length",           "Standard / Detailed / Deep Dive",
         "Target word count of the report"),
        ("Number of Sources",       "3 to 8",
         "How many web sources to analyze"),
        ("Content Size per Source", "3000 to 10000 characters",
         "How much text to extract per page"),
        ("Comparison Table",        "On or Off",
         "Whether to include a table in the report"),
        ("Focus Areas",             "8 topics to choose from",
         "Which aspects of the topic to emphasize"),
    ]
    settings_rows = [[Paragraph(b("Setting"), th_ps("sh1")),
                      Paragraph(b("Options"),  th_ps("sh2")),
                      Paragraph(b("What It Controls"), th_ps("sh3"))]]
    for name, opts, ctrl in settings_data:
        settings_rows.append([Paragraph(name, td_ps("sn")),
                               Paragraph(opts, td_ps("so")),
                               Paragraph(ctrl, td_ps("sc2"))])
    settings_tbl = Table(settings_rows,
                         colWidths=[CONTENT_W * 0.26,
                                    CONTENT_W * 0.30,
                                    CONTENT_W * 0.44])
    settings_tbl.setStyle(table_style(len(settings_data)))
    story.append(settings_tbl)
    story.append(Paragraph("Table 4: Advanced Settings Available to the User", S["caption"]))
    story.append(Spacer(1, 0.1 * cm))

    for heading, body_text in [
        ("Pipeline Progress Display",
         "The right column shows the current state of the pipeline. A progress bar at the "
         "top fills in as steps complete. Below it are six step cards, one for each pipeline "
         "step. Each card shows the step number, name, and description, along with a status "
         "badge that shows WAITING, RUNNING with an animated indicator, or DONE."),
        ("Results Tabs",
         "Once the pipeline finishes, the results appear below the input area in five tabs: "
         "Report, Analysis, Sources, Citations, and Related Topics."),
        ("Sidebar and History",
         "The sidebar shows the research history for the current session. Up to 20 previous "
         "searches are stored. Each entry shows the topic, the time the search was run, the "
         "quality score, and how long it took. A Load button next to each entry restores that "
         "result for review."),
        ("Quick Example Buttons",
         "Below the topic input field, four example topic buttons are shown. Clicking any "
         "of them fills in the topic field and starts the research automatically."),
    ]:
        story.append(KeepTogether([
            Paragraph(heading, S["h2"]),
            Paragraph(body_text, S["body"]),
        ]))

    # ── 8. Key Features ───────────────────────────────────────────────────────
    section_start(story, "8.  Key Features", S)

    features = [
        ("Fully Automated Research Pipeline",
         "The user only needs to enter a topic. The system handles everything else, "
         "from searching the web to writing and reviewing the report."),
        ("Real-Time Progress Visibility",
         "The user can watch each step of the pipeline complete in real time. "
         "Step cards update from WAITING to RUNNING to DONE as the pipeline progresses."),
        ("Configurable Report Depth",
         "Users can choose between a standard, detailed, or deep dive report. "
         "They can also select specific focus areas to make the report more relevant."),
        ("Quality Scoring",
         "Every report receives an automatic quality review from the Critic Chain. "
         "The score out of ten gives the user an immediate sense of thoroughness."),
        ("Entity and Statistics Extraction",
         "The system automatically identifies and displays important names, organizations, "
         "technologies, dates, statistics, and places mentioned in the report."),
        ("Downloadable Output",
         "Reports can be downloaded as markdown files or as standalone HTML files. "
         "This makes the output easy to share or archive."),
        ("Session History",
         "The sidebar keeps a record of all searches in the current session. "
         "Users can reload any previous result without running the pipeline again."),
        ("Follow-up Research Integration",
         "The six related topic suggestions are clickable. This allows the user to "
         "continue exploring a subject area without leaving the interface."),
        ("Source Transparency",
         "All sources used in the research are listed with their titles, domains, "
         "and direct links. Academic-style citations are also generated automatically."),
        ("Error Resilience",
         "All pipeline steps are wrapped in error handling. If one step fails, the "
         "system continues with a fallback message and does not crash."),
    ]

    for feat_name, feat_desc in features:
        story.append(KeepTogether([
            Paragraph(f"•  {b(feat_name)}", S["bullet_bold"]),
            Paragraph(feat_desc, S["bullet_desc"]),
        ]))

    # ── 9. Error Handling and Reliability ─────────────────────────────────────
    section_start(story, "9.  Error Handling and Reliability", S)

    story.append(Paragraph(
        "ResearchBuddy is designed to handle errors gracefully so that a single failure "
        "does not stop the entire pipeline.",
        S["body"]))

    for heading, body_text in [
        ("Safe Agent Invocation",
         "Every agent call is wrapped in a safe-invoke function that catches any exception "
         "and returns a fallback message instead of crashing. This allows the pipeline to "
         "continue with the next step."),
        ("Retry Logic for API Calls",
         "The Tavily API search function uses the tenacity library to automatically retry "
         "failed requests with exponential backoff. This handles temporary network issues "
         "and rate limit errors."),
        ("Scraping Timeouts",
         "The web scraper uses a timeout setting to avoid waiting forever for slow or "
         "unresponsive servers. If a page cannot be loaded in time, the scraper skips it "
         "and moves on to the next source."),
        ("Input Validation",
         "Data passed between pipeline steps is validated using Pydantic data classes, "
         "ensuring each step receives properly formatted input."),
        ("Streamlit Session State Management",
         "The user interface uses Streamlit session state carefully to prevent duplicate "
         "runs and lost results. Completed results are saved to session history."),
    ]:
        story.append(KeepTogether([
            Paragraph(heading, S["h2"]),
            Paragraph(body_text, S["body"]),
        ]))

    # ── 10. Configuration and Customization ───────────────────────────────────
    section_start(story, "10.  Configuration and Customization", S)

    story.append(Paragraph(
        "ResearchBuddy reads its configuration from a .env file stored in the project "
        "directory. This makes it easy to change key settings without modifying any code.",
        S["body"]))

    mono3 = ParagraphStyle("mono3", fontName="Courier", fontSize=9.5,
                            textColor=DARK_GREY, leading=14)
    config_data = [
        ("NVIDIA_API_KEY",          "Required",         "API key for NVIDIA NIM (Mistral model)"),
        ("TAVILY_API_KEY",         "Required",         "API key for the Tavily web search service"),
        ("NVIDIA_MODEL",           "mistralai/mistral-medium-3.5-128b", "Which NVIDIA NIM model to use"),
        ("SEARCH_RESULTS_LIMIT",   "6",                "Maximum number of search results to fetch"),
        ("SCRAPED_SOURCES_LIMIT",  "3",                "Maximum number of sources to scrape fully"),
        ("SCRAPE_CHARACTER_LIMIT", "5000",             "Maximum characters to extract per web page"),
    ]
    config_rows = [[Paragraph(b("Variable"),   th_ps("ch1")),
                    Paragraph(b("Default"),     th_ps("ch2")),
                    Paragraph(b("Description"), th_ps("ch3"))]]
    for var, default, desc in config_data:
        config_rows.append([Paragraph(var, mono3),
                             Paragraph(default, td_ps("dv")),
                             Paragraph(desc, td_ps("dd"))])
    config_tbl = Table(config_rows,
                       colWidths=[CONTENT_W * 0.30,
                                  CONTENT_W * 0.18,
                                  CONTENT_W * 0.52])
    config_tbl.setStyle(table_style(len(config_data)))
    story.append(config_tbl)
    story.append(Paragraph("Table 5: Environment Variables for Configuration", S["caption"]))
    story.append(Spacer(1, 0.2 * cm))

    story.append(Paragraph(
        "In addition to the environment file, the user can change many settings through "
        "the Advanced Settings panel each time they run a search. These in-session settings "
        "override the defaults for that particular run without changing the permanent "
        "configuration.",
        S["body"]))

    story.append(Paragraph(
        "The system is also designed to be extensible. New agents can be added to "
        "core/agents.py by following the same pattern used for existing chains. "
        "The pipeline in core/pipeline.py can be updated to include additional steps. "
        "New UI components can be added to ui/components.py without changing the main "
        "application logic.",
        S["body"]))

    # ── 11. Conclusion ────────────────────────────────────────────────────────
    section_start(story, "11.  Conclusion", S)

    for para in [
        "ResearchBuddy demonstrates how a multi-agent system can produce results that are "
        "significantly better than what a single AI model could achieve on its own. "
        "By assigning a specific role to each agent and passing information through a "
        "structured pipeline, the system produces research reports that are thorough, "
        "evidence-based, and well-organized.",

        "The system is practical and ready to use. It connects to real-time web search, "
        "scrapes and cleans content from actual web pages, and generates reports in a "
        "format that users can download and share. The quality review step adds a layer "
        "of self-assessment that helps users understand the reliability of each report.",

        "The project also shows good software engineering practices. The code is divided "
        "into clear layers with well-defined responsibilities. Error handling is built in "
        "at every stage. Configuration is separate from code. The user interface is clean, "
        "informative, and easy to use.",

        "ResearchBuddy is a strong example of how modern AI tools such as large language "
        "models, web search APIs, and agent frameworks can be combined to build systems "
        "that solve real problems and provide genuine value to users.",
    ]:
        story.append(Paragraph(para, S["body"]))

    story.append(Spacer(1, 1.0 * cm))
    story.append(HRFlowable(width="100%", thickness=0.8, color=BLACK,
                             spaceAfter=6, spaceBefore=2))
    story.append(Spacer(1, 0.4 * cm))

    label_ps = ParagraphStyle("cl", fontName="Helvetica-Bold", fontSize=10,
                               textColor=DARK_GREY)
    value_ps = ParagraphStyle("cv", fontName="Helvetica", fontSize=10.5,
                               textColor=BLACK)
    closing_data = [
        ("Submitted By",      "Rahul Yadav"),
        ("Enrollment Number", "25535037"),
        ("Branch",            "M.Tech Computer Science and Engineering"),
        ("Date",              "June 2026"),
    ]
    closing_rows = [[Paragraph(lbl, label_ps), Paragraph(val, value_ps)]
                    for lbl, val in closing_data]
    closing_tbl = Table(closing_rows,
                        colWidths=[CONTENT_W * 0.30, CONTENT_W * 0.70])
    closing_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_GREY),
        ("BOX",           (0, 0), (-1, -1), 0.5, RULE_GREY),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 14),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.3, RULE_GREY),
    ]))
    story.append(closing_tbl)

    doc.build(story)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "Report.pdf")
    build_pdf(out)
