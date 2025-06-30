Perfect, Pratham --- now we're flying full throttle into **v2.0 of your Competitive Intelligence Engine**. Here's your clarified vision, now structured and detailed for development in **LangChain + Streamlit**, with **DeepSeek + Firecrawl + Exa + File-based RAG**.

* * * * *

🎯 FINAL SYSTEM DESIGN OVERVIEW
-------------------------------

### ✅ **Sidebar (API keys only --- no login!)**

-   🔑 DeepSeek API Key

-   🔑 Firecrawl API Key

-   🔑 Exa API Key

### ✅ **Main Section**

| Element | Description |
| --- | --- |
| 🔗 **Company URL or Description** | Identify your business --- either a domain or a 1-liner |
| 📎 **File Upload** | Upload internal documents (brochures, pricing, pitch decks) |
| 🚀 **Analyze Button** | Triggers entire competitor intelligence pipeline |
| 📄 **Outputs (Post-button)** |  |
| → 🔍 **Top 5 Competitor URLs** | Pulled using Exa |
| → 📊 **Comparison Table** | Extracted via Firecrawl, analyzed via DeepSeek |
| → 🎯 **Strategy Suggestions** | DeepSeek insights on pricing, market gaps, GTM |
| → 📚 **File-Aware Insights** | RAG-enabled strategy using uploaded files |
| → 💥 **SWOT Generator** | Strengths, Weaknesses, Opportunities, Threats |
| → 📥 **Export to PDF** | One-click export of all above content into report |

* * * * *

🧠 INTERNAL FLOW (Behind the Scenes)
------------------------------------

```
graph TD
    A[User Inputs] --> B[Exa AI]
    B --> C[Get 5 Competitor URLs]
    C --> D[Firecrawl Scraping]
    D --> E[LangChain Agent - Data Extraction]
    E --> F1[Comparison Table]
    E --> F2[DeepSeek Analysis Agent]
    F2 --> G1[Strategy Suggestions]
    F2 --> G2[SWOT Report]
    F2 --> G3[Insights from Uploaded File (RAG)]
    G1 --> H[PDF Export]
    G2 --> H
    G3 --> H
    F1 --> H

```

* * * * *

🧱 MODULE-BY-MODULE LAYOUT (PLANNING STAGE)
-------------------------------------------

### 🔧 **1\. Sidebar -- API Key Capture**

Use `st.sidebar.text_input()` for:

-   `deepseek_api_key`

-   `firecrawl_api_key`

-   `exa_api_key`

→ Store them in `st.session_state` so the rest of the app uses them smoothly.

* * * * *

### 🧠 **2\. Competitor Discovery via Exa AI**

-   Input: URL or description

-   Call:

    ```
    exa.find_similar(url=...) or exa.search(description)

    ```

-   Return **5 competitor URLs** as a list

* * * * *

### 🕷️ **3\. Structured Scraping via Firecrawl**

-   For each competitor URL:

    -   Crawl subpages using `url/*`

    -   Pass prompt & schema to `FirecrawlApp.extract(...)`

-   Schema to extract:

    -   `company_name`, `pricing`, `key_features`, `tech_stack`, `marketing_focus`, `customer_feedback`

* * * * *

### 🤖 **4\. LangChain Agent: DeepSeek-Powered Comparison + Insights**

Define a tool/agent that:

-   Converts structured Firecrawl outputs to a JSON blob

-   Sends prompt to DeepSeek like:

    > "Given this data on 5 companies, compare them across features, pricing, marketing..."

**Outputs:**

-   🧮 Table of comparisons (Company, Features, Stack, etc.)

-   🧠 Suggestions on pricing, product gaps, unique angles

* * * * *

### 📎 **5\. File Upload + RAG**

-   Upload: `st.file_uploader()` → PDF/DOCX/TXT

-   Convert using LangChain loaders

-   Chunk → embed → store in **FAISS or Chroma**

-   Define a **RAG Tool** that uses:

    -   `ConversationalRetrievalChain`

    -   DeepSeek as LLM

-   Feed it a task like:

    > "Using the uploaded document and competitor data, suggest a unique growth roadmap."

* * * * *

### 🧩 **6\. SWOT Generator**

Send prompt to DeepSeek:

> "From this data, generate a SWOT analysis matrix for our company. Use uploaded documents + scraped competitor info."

Return:

```
**Strengths**:
- Our product is simpler to use...
**Weaknesses**:
- Pricing lacks clarity...
**Opportunities**:
- Competitors miss B2B SMB segment...
**Threats**:
- New entrants with freemium plans...

```

* * * * *

### 📥 **7\. PDF Export**

Use `pdfkit`, `WeasyPrint`, or `html-pdf-node` (if you want JS integration later).

Export includes:

-   Competitor list

-   Comparison table

-   Strategy suggestions

-   SWOT matrix

-   File-aware insights

* * * * *

🗂️ RECOMMENDED FILE STRUCTURE
------------------------------

```
project_root/
│
├── app.py                    # Streamlit UI
├── agents/
│   ├── deepseek_agent.py     # DeepSeek-based strategy + SWOT
│   ├── rag_agent.py          # RAG chain using uploaded files
│   └── firecrawl_agent.py    # Scrapes and extracts info
│
├── tools/
│   ├── exa_tool.py           # Wraps Exa API calls
│   ├── deepseek_llm.py       # Custom wrapper for DeepSeek API
│   └── rag_tools.py          # RAG vector store + retriever setup
│
├── components/
│   ├── comparison_table.py   # Creates styled table
│   ├── swot_visualizer.py    # Optional: shows SWOT in cool format
│   └── pdf_exporter.py       # Converts everything into PDF
│
├── data/
│   └── uploaded_docs/        # Temporary upload path
│
└── utils/
    └── prompts.py            # Prompt templates

```

* * * * *

🧭 NEXT STEPS: WHAT YOU CAN ASK ME
----------------------------------

Here's what I can help you with from here:

-   ✅ Define prompt templates for DeepSeek (comparison, strategy, SWOT, etc.)

-   ✅ Build custom DeepSeek wrapper for LangChain (`LLM` class)

-   ✅ Design each LangChain agent with the right tools

-   ✅ Help build the RAG pipeline from uploaded files

-   ✅ Set up PDF export logic

* * * * *

You're now set to create a **zero-login, API-powered, multi-agent competitive intelligence dashboard** that rivals premium SaaS solutions --- but open, composable, and yours. ⚙️📊

Let me know which part you'd like to build first --- and I'll walk you through it with full clarity.