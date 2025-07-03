import streamlit as st
from tools.exa_tool import get_competitor_urls
from agents.firecrawl_agent import extract_competitor_info
from agents.deepseek_agent import ( generate_comparison_table, generate_strategy_report, generate_swot_report )
from agents.rag_agent import generate_company_context
import os
from components.pdf_exporter import generate_pdf
from streamlit_extras.stylable_container import stylable_container

import warnings
warnings.filterwarnings('ignore')

# Streamlit page setup
st.set_page_config(page_title="Comp_Intell-AI", layout="wide")
st.title("AI Competitor Intelligence System")

# --- Sidebar Theming with Gradient Background ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(145deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Logo (Text-Based) ---
st.sidebar.markdown("""
<h2 style='text-align: center; font-family: "Segoe UI", sans-serif; color: #6dd5ed;'>
     <b>Comp<span style="color:white;">Intell</span><span style="font-size:14px;">.AI</span></b>
</h2>
""", unsafe_allow_html=True)

# --- Sidebar Info Panel ---
st.sidebar.markdown("""
<div style="background-color:#1e1e2f; padding:18px; border-radius:10px; margin-top:12px;">
    
<h4 style="color:#6dd5ed; margin-bottom:5px;"> Who are we?</h4>
<p style="font-size:13px; color:white; margin-top:0;">
    We are an AI-first startup building tools to supercharge business decisions with data and intelligence.
</p>
    
<h4 style="color:#6dd5ed; margin-top:15px; margin-bottom:5px;"> What we do</h4>
<p style="font-size:13px; color:white; margin-top:0;">
    We analyze your documents, research competitors, generate strategies, and present it all as a beautiful report—instantly.
</p>

<h4 style="color:#6dd5ed; margin-top:15px; margin-bottom:5px;"> Our vision</h4>
<p style="font-size:13px; color:white; margin-top:0;">
    Democratizing competitive intelligence for every startup—no expensive consultants, just smart AI workflows.
</p>

</div>
""", unsafe_allow_html=True)

# Store keys in session state for later access
st.session_state["deepseek_api_key"] = st.secrets["DEEPSEEK_API_KEY"]
st.session_state["firecrawl_api_key"] = st.secrets["FIRECRAWL_API_KEY"]
st.session_state["exa_api_key"] = st.secrets["EXA_AI_API_KEY"]

# Warning if any API key is missing
# if not all([deepseek_api_key, firecrawl_api_key, exa_api_key]):
#     st.sidebar.warning("Please enter all required API keys to proceed.")

# Main inputs
st.markdown("###  Enter your Company's Information")
st.write(" ")


url_input = st.text_input(" Company's URL (optional)", placeholder="https://example.com")
description_input = st.text_input(" Company's Description", placeholder="E.g. AI-powered fitness app for runners")

st.write(" ")
st.write(" ")

# File uploader header
st.markdown("###  Upload your Company's Files")

# Expander for guidance


with stylable_container(
    key="file_hint",
    css_styles="""
        button {
            background-color: #e6f0ff;
            border: 1px solid #3399ff;
            color: #0059b3;
            padding: 0.5em;
            margin-top: 10px;
        }
    """,
):
    if st.button("❓ What files should I upload?"):
        st.markdown("""
        Help us generate richer business insights by uploading files such as:

        - **Annual Reports** – sales, revenue, growth stats  
        - **Mission/Vision Docs** – company goals and values  
        - **Marketing Strategy Files** – campaigns, customer personas  
        - **Product Brochures / Feature Sheets**  
        - **Customer Feedback Summaries**  
        - **Internal Policy Docs** – HR, pricing, sustainability  

        Accepted: `.pdf`, `.docx`, `.txt`
        """)


# File uploader
uploaded_files = st.file_uploader(
    "Upload internal documents (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

# Display uploaded file names and types
if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
    for file in uploaded_files:
        file_ext = file.name.split(".")[-1].upper()
        st.write(f"📄 `{file.name}` ({file_ext})")

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
