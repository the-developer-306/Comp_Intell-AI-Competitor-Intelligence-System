from fpdf import FPDF
from io import BytesIO
from datetime import datetime

# 🧼 Helper function to strip unsupported characters
def sanitize_text(text):
    if not isinstance(text, str):
        text = str(text)
    return text.encode("latin-1", "ignore").decode("latin-1")

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, sanitize_text("AI Competitor Intelligence Report"), ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, sanitize_text(f"🔹 {title}"), ln=True)
        self.ln(2)

    def add_multiline(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, sanitize_text(text))
        self.ln(3)

def generate_pdf(
    competitor_urls: list,
    competitor_data: list,
    comparison_table_md: str,
    strategy_report: str,
    swot_report: str
):
    pdf = PDFReport()
    pdf.add_page()

    # Cover metadata
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 10, sanitize_text(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"), ln=True)
    pdf.ln(5)

    # Section 1: Competitor URLs
    pdf.section_title("Competitor URLs")
    url_text = "\n".join(f"- {url}" for url in competitor_urls)
    pdf.add_multiline(url_text)

    # Section 2: Competitor Data
    pdf.section_title("Detailed Competitor Data")
    for comp in competitor_data:
        pdf.set_font("Arial", "B", 11)
        comp_title = f"📌 {comp.get('company_name', 'N/A')} ({comp.get('competitor_url', '')})"
        pdf.cell(0, 8, sanitize_text(comp_title), ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.add_multiline(f"Pricing: {comp.get('pricing', 'N/A')}")
        pdf.add_multiline(f"Key Features: {', '.join(comp.get('key_features', []))}")
        pdf.add_multiline(f"Tech Stack: {', '.join(comp.get('tech_stack', []))}")
        pdf.add_multiline(f"Marketing Focus: {comp.get('marketing_focus', 'N/A')}")
        pdf.add_multiline(f"Customer Feedback: {comp.get('customer_feedback', 'N/A')}")
        pdf.ln(3)

    # Section 3: Comparison Table
    pdf.section_title("Comparison Table")
    pdf.add_multiline(comparison_table_md)

    # Section 4: Strategy
    pdf.section_title("Growth Strategy Suggestions")
    pdf.add_multiline(strategy_report)

    # Section 5: SWOT
    pdf.section_title("SWOT Analysis")
    pdf.add_multiline(swot_report)

    # Output as BytesIO
    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # 'S' = return as string
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

