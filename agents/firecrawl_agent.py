from firecrawl import FirecrawlApp
from typing import Optional, List
from pydantic import BaseModel, Field
import streamlit as st

# Define the data schema for structured extraction
class CompetitorDataSchema(BaseModel):
    company_name: str = Field(description="Name of the company")
    pricing: str = Field(description="Pricing details, tiers, and plans")
    key_features: List[str] = Field(description="Main features and capabilities of the product/service")
    tech_stack: List[str] = Field(description="Technologies, frameworks, and tools used")
    marketing_focus: str = Field(description="Main marketing angles and target audience")
    customer_feedback: str = Field(description="Customer testimonials, reviews, and feedback")

def extract_competitor_info(competitor_url: str) -> Optional[dict]:
    try:
        app = FirecrawlApp(api_key=st.session_state["firecrawl_api_key"])

        # Include all subpages with wildcard i.e. /*
        url_pattern = f"{competitor_url}/*"

        extraction_prompt = """
            Extract detailed information about the company's offerings, including:
            - Company name and basic information
            - Pricing details, plans, and tiers
            - Key features and main capabilities
            - Technology stack and technical details
            - Marketing focus and target audience
            - Customer feedback and testimonials

            Use the full website content for your answer.
        """

        response = app.extract(
            [url_pattern],
            prompt= extraction_prompt,
            schema= CompetitorDataSchema.model_json_schema(),
        )

        if response.success:
            data = response.data
            return {
                "competitor_url": competitor_url,
                "company_name": data.get('company_name', 'N/A'),
                "pricing": data.get('pricing', 'N/A'),
                "key_features": data.get('key_features', [])[:5],
                "tech_stack": data.get('tech_stack', [])[:5],
                "marketing_focus": data.get('marketing_focus', 'N/A'),
                "customer_feedback": data.get('customer_feedback', 'N/A')
            }
        else:
            st.warning(f"⚠️ Firecrawl failed for {competitor_url}")
            return None

    except Exception as e:
        st.warning(f"⚠️ Error scraping {competitor_url}: {str(e)}")
        return None
