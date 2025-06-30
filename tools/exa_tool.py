from exa_py import Exa
import streamlit as st

def get_competitor_urls(url: str = None, description: str = None) -> list:
    """
    Fetch up to 5 competitor URLs using Exa AI based on a company URL or description.
    """
    if not (url or description):
        raise ValueError("Either URL or description must be provided.")

    exa_api_key = st.session_state.get("exa_api_key", None)
    if not exa_api_key:
        raise ValueError("Missing Exa API key in session state.")

    exa = Exa(api_key=exa_api_key)

    try:
        if url:
            result = exa.find_similar(
                url=url,
                num_results=5,
                exclude_source_domain=True,
                category="company"
            )
        else:
            result = exa.search(
                query=description,
                type="neural",
                category="company",
                use_autoprompt=True,
                num_results=5
            )

        urls = [item.url for item in result.results]
        return urls

    except Exception as e:
        st.error(f"❌ Error fetching competitor URLs from Exa: {str(e)}")
        return []
