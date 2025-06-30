COMPARISION_SYSTEM_PROMPT = "You are an expert market analyst generating structured comparison tables."

COMPARISION_USER_PROMPT = """
    Analyze the following competitor data and return a markdown table comparing them.
    Only use these columns: Company, Pricing, Key Features, Tech Stack, Marketing Focus, Customer Feedback

    Use short bullet points or summaries for clarity. For Company, include name and URL.

    Data:
    {competitor_data}    
"""

STRATEGY_SYSTEM_PROMPT = "You are a strategic AI assistant for business growth."

STRATEGY_USER_PROMPT = """
    Use the provided internal company knowledge and competitor insights to generate a comprehensive growth strategy.

    ### Tasks:
    1. Identify market gaps competitors are missing.
    2. Recommend new features, marketing angles, and pricing strategies.
    3. Suggest technical improvements or differentiators.
    4. Provide positioning strategies against current competitors.

    ### Company Internal Context:
    {company_context}

    ### Competitor Analysis Data:
    {competitor_data}
"""

SWOT_SYSTEM_PROMPT = "You are a senior business consultant generating a SWOT report."

SWOT_USER_PROMPT = """
    Based on the company’s internal knowledge and market competitors, produce a SWOT analysis for the company.

    Use the format:

    ### Strengths:
    - ...
    ### Weaknesses:
    - ...
    ### Opportunities:
    - ...
    ### Threats:
    - ...

    ### Company Internal Context:
    {company_context}

    ### Competitor Analysis Data:
    {competitor_data}
"""
