import json
from tools.deepseek_llm import DeepSeekLLM
import streamlit as st

from utils.prompts import (
    STRATEGY_SYSTEM_PROMPT,
    STRATEGY_USER_PROMPT,
    SWOT_SYSTEM_PROMPT,
    SWOT_USER_PROMPT,
    COMPARISION_USER_PROMPT,
    COMPARISION_SYSTEM_PROMPT
)
# Instantiate once
def get_llm():
    return DeepSeekLLM(api_key=st.session_state["deepseek_api_key"])


def generate_comparison_table(competitor_data: list) -> str:
    llm = get_llm()
    
    user_prompt = COMPARISION_USER_PROMPT.format(
        competitor_data=json.dumps(competitor_data, indent=2),
    )

    return llm.generate(
        system_prompt=COMPARISION_SYSTEM_PROMPT,
        user_prompt=user_prompt
    )


def generate_strategy_report(competitor_data: list, company_context: str) -> str:
    llm = get_llm()

    user_prompt = STRATEGY_USER_PROMPT.format(
        competitor_data=json.dumps(competitor_data, indent=2),
        company_context=company_context
    )

    return llm.generate(
        system_prompt=STRATEGY_SYSTEM_PROMPT,
        user_prompt=user_prompt
    )


def generate_swot_report(competitor_data: list, company_context: str) -> str:
    llm = get_llm()

    user_prompt = SWOT_USER_PROMPT.format(
        competitor_data=json.dumps(competitor_data, indent=2),
        company_context=company_context
    )

    return llm.generate(
        system_prompt=SWOT_SYSTEM_PROMPT,
        user_prompt=user_prompt
    )
