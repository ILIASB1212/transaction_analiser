
import asyncio
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.exceptions import (
    UnexpectedModelBehavior,
    ModelRequestRejectedError,
)

from src.schemas.Schemas import (
    CustomerRecords,
    TransactionAnalysis,
)

from src.retriver.inject_context import (
    get_customer_profile,
    get_customer_transaction_history,
)

from dashboard import (
    apply_styles,
    render_header,
    render_dashboard,
    render_empty_state,
)

# Environment variables
load_dotenv()

st.set_page_config(
    page_title="Transaction Intelligence",
    page_icon="💳",
    layout="wide",
)

# Load customer data
DATA_PATH = Path(__file__).parent / "data" / "bank.json"

with open(DATA_PATH, encoding="utf-8") as f:
    CUSTOMERS = json.load(f)

# Dependency injection
records = CustomerRecords(customers=CUSTOMERS)

MODEL = "groq:openai/gpt-oss-20b"

SYSTEM_PROMPT = """
You are a bank transaction analysis assistant.

Before analyzing a transaction, retrieve the customer's
profile and historical transactions using your tools.

Compare the new transaction against the customer's
historical spending patterns, considering:

- Transaction amount
- Transaction category
- Country and city
- Historical spending behavior

All transaction amounts are denominated in MAD.

Do not invent missing information.
Do not assess transaction timing because the historical
dataset does not contain timestamps.

Do not flag a large transaction solely because it is large.
Base your assessment on the customer's actual history.

Return a structured TransactionAnalysis.
"""


async def analyse_transaction(query: str):

    transaction_agent = Agent(
        MODEL,
        deps_type=CustomerRecords,
        output_type=TransactionAnalysis,
        tools=[
            get_customer_profile,
            get_customer_transaction_history,
        ],
        system_prompt=SYSTEM_PROMPT,
    )

    result = await transaction_agent.run(
        query,
        deps=records,
    )

    return result.output


# Initialize interface
apply_styles()
render_header()

if "assessment" not in st.session_state:
    st.session_state.assessment = None


with st.form("transaction_form"):

    query = st.text_area(
        "Transaction description",
        placeholder=(
            "Customer CUST-0040 spent 150 MAD "
            "on shopping in Marrakech, Morocco."
        ),
        height=120,
    )

    submitted = st.form_submit_button(
        "Run risk assessment",
        type="primary",
    )


if submitted:

    st.session_state.assessment = None

    if not query.strip():

        st.warning("Please enter a transaction description.")

    else:

        try:

            with st.spinner("Analyzing customer transaction..."):

                result = asyncio.run(
                    analyse_transaction(query)
                )

                st.session_state.assessment = result

        except (
            UnexpectedModelBehavior,
            ModelRequestRejectedError,
        ):

            st.error(
                "Analysis failed. Please provide a valid customer ID, "
                "amount, category and transaction location."
            )


# Render assessment
if st.session_state.assessment is not None:

    render_dashboard(st.session_state.assessment)

else:

    render_empty_state()
