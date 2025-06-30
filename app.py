import streamlit as st
from tools.exa_tool import get_competitor_urls
from agents.firecrawl_agent import extract_competitor_info
from agents.deepseek_agent import ( generate_comparison_table, generate_strategy_report, generate_swot_report )
from agents.rag_agent import generate_company_context
import os
from components.pdf_exporter import generate_pdf

import warnings
warnings.filterwarnings('ignore')

# Streamlit page setup
st.set_page_config(page_title="🧠 AI Competitor Intelligence", layout="wide")
st.title("AI Competitor Intelligence Agent")

# Sidebar for API keys
st.sidebar.header("🔐 API Keys")
deepseek_api_key = st.sidebar.text_input("DeepSeek API Key", type="password")
firecrawl_api_key = st.sidebar.text_input("Firecrawl API Key", type="password")
exa_api_key = st.sidebar.text_input("Exa API Key", type="password")

# Store keys in session state for later access
if deepseek_api_key:
    st.session_state["deepseek_api_key"] = deepseek_api_key
if firecrawl_api_key:
    st.session_state["firecrawl_api_key"] = firecrawl_api_key
if exa_api_key:
    st.session_state["exa_api_key"] = exa_api_key

# Warning if any API key is missing
if not all([deepseek_api_key, firecrawl_api_key, exa_api_key]):
    st.sidebar.warning("Please enter all required API keys to proceed.")

# Main inputs
st.markdown("### 👇 Enter Company Info")
col1, col2 = st.columns(2)

with col1:
    url_input = st.text_input("🔗 Company's URL", placeholder="https://example.com")
    description_input = st.text_input("📝 Company's Description", placeholder="E.g. AI-powered fitness app for runners")

with col2:
    # File uploader
    st.markdown("### 📁 Upload Company's Files (Optional)")
    uploaded_files = st.file_uploader(
        "Upload internal documents (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )
st.write(" ")

# Analyze button
analyze_button = st.button("Analyze Competitors")

# === RESULTS DISPLAY ===
if "competitor_data" in st.session_state:

    st.subheader("🔗 Competitor URLs")
    for url in st.session_state["competitor_urls"]:
        st.markdown(f"- [{url}]({url})")

    st.subheader("📌 Detailed Competitor Data")
    for comp in st.session_state["competitor_data"]:
        with st.expander(f"{comp.get('company_name', 'N/A')}"):
            st.markdown(f"**URL**: {comp.get('competitor_url', '')}")
            st.markdown(f"**Pricing**: {comp.get('pricing', 'N/A')}")
            st.markdown(f"**Key Features**: {', '.join(comp.get('key_features', []))}")
            st.markdown(f"**Tech Stack**: {', '.join(comp.get('tech_stack', []))}")
            st.markdown(f"**Marketing Focus**: {comp.get('marketing_focus', 'N/A')}")
            st.markdown(f"**Customer Feedback**: {comp.get('customer_feedback', 'N/A')}")

    st.subheader("📊 Competitor Comparison Table")
    st.markdown(st.session_state["comparison_table_md"], unsafe_allow_html=True)

    st.subheader("🚀 Growth Strategy Suggestions")
    st.markdown(st.session_state["strategy_report"])

    st.subheader("🧠 SWOT Analysis")
    st.markdown(st.session_state["swot_report"])

    # === PDF DOWNLOAD SECTION ===
    st.subheader("📥 Download Your Report")

    pdf_bytes = generate_pdf(
        competitor_urls=st.session_state["competitor_urls"],
        competitor_data=st.session_state["competitor_data"],
        comparison_table_md=st.session_state["comparison_table_md"],
        strategy_report=st.session_state["strategy_report"],
        swot_report=st.session_state["swot_report"]
    )

    st.download_button(
        label="Download Complete Intelligence Report (PDF)",
        data=pdf_bytes,
        file_name="competitor_intelligence_report.pdf",
        mime="application/pdf"
    )


if analyze_button:

    if not (url_input or description_input):
        st.error("🚫 Please provide either a URL or a description of your company.")
    else:

        # ------------------------------------------------------------------------------------------ Fetch Competitor URLs using EXA AI
        with st.spinner("🔍 Fetching competitor URLs from Exa..."):
            competitor_urls = get_competitor_urls(url=url_input, description=description_input)

        if competitor_urls:
            st.success("✅ Found competitor URLs:")
            for comp_url in competitor_urls:
                st.markdown(f"- 🔗 [{comp_url}]({comp_url})")
        else:
            st.warning("⚠️ No competitors found. Try a different input.")
            st.stop()

        # ------------------------------------------------------------------------------------------ Fetch Competitor data using Firecrawl
        competitor_data = []

        for comp_url in competitor_urls:
            with st.spinner(f"🔍 Scraping {comp_url}..."):
                info = extract_competitor_info(comp_url)
                if info:
                    competitor_data.append(info)

        st.session_state["competitor_data"] = competitor_data

        if competitor_data:
            st.success("✅ Data extracted from all competitors.")
            # st.write(competitor_data)
            st.subheader("🏢 Competitor Snapshots")

            for comp in competitor_data:
                with st.expander(f"🔍 {comp['company_name']}"):
                    st.markdown(f"**🌐 URL**: [{comp['competitor_url']}]({comp['competitor_url']})")
                    st.markdown(f"**💰 Pricing**: {comp['pricing']}")
                    st.markdown(f"**⚙️ Key Features**: {', '.join(comp['key_features'])}")
                    st.markdown(f"**🧪 Tech Stack**: {', '.join(comp['tech_stack'])}")
                    st.markdown(f"**🎯 Marketing Focus**: {comp['marketing_focus']}")
                    st.markdown(f"**💬 Customer Feedback**: {comp['customer_feedback']}")

        else:
            st.error("🚫 No competitor data could be extracted.")
            st.stop()

        # ---------------------------------------------------------------------------------------- Comparision using DEEPSEEK

        with st.spinner("📊 Generating comparison table with DeepSeek..."):
            comparison_markdown = generate_comparison_table(competitor_data)
            st.markdown(comparison_markdown, unsafe_allow_html=True)

        # ----------------------------------------------------------------------------------------- RAG Architecture

        company_context = ""
        if uploaded_files:
            file_paths = []
            for file in uploaded_files:
                file_path = os.path.join("data/uploaded_docs", file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                file_paths.append(file_path)

            with st.spinner("📚 Processing internal documents with RAG..."):
                company_context = generate_company_context(file_paths)

        # ----------------------------------------------------------------------------------------- Strategy, SWOT generation using DEEPSEEK

        if competitor_data and company_context:
            with st.spinner("🎯 Creating strategy report..."):
                strategy = generate_strategy_report(competitor_data, company_context)
                st.subheader("🚀 Growth Strategy")
                st.markdown(strategy)

            with st.spinner("🧠 Generating SWOT analysis..."):
                swot = generate_swot_report(competitor_data, company_context)
                st.subheader("📊 SWOT Analysis")
                st.markdown(swot)


        # Save final outputs into session_state to persist them across reruns
        st.session_state["competitor_urls"] = competitor_urls
        st.session_state["competitor_data"] = competitor_data
        st.session_state["comparison_table_md"] = comparison_markdown
        st.session_state["strategy_report"] = strategy
        st.session_state["swot_report"] = swot


        # ----------------------------------------------------------------------------------------- PDF exporting

        with st.spinner("📥 Preparing downloadable PDF report..."):
            pdf_bytes = generate_pdf(
                competitor_urls=competitor_urls,
                competitor_data=competitor_data,
                comparison_table_md=comparison_markdown,  # from DeepSeek
                strategy_report=strategy,
                swot_report=swot
            )

            st.download_button(
                label="📥 Download Full Intelligence Report (PDF)",
                data=pdf_bytes,
                file_name="competitor_intelligence_report.pdf",
                mime="application/pdf"
            )
