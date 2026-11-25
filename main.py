

import os
from dotenv import load_dotenv
load_dotenv()
from src.schemas.Schemas import CustomerRecords, TransactionAnalysis

from pydantic_ai import Agent
from src.retriver.inject_context import get_customer_profile, get_customer_transaction_history
# defining LLM
model = "groq:openai/gpt-oss-20b"




import json

with open("data/bank.json", encoding="utf-8") as f:
    CUSTOMERS = json.load(f)



transaction_agent = Agent(
    model,
    deps_type=CustomerRecords,
    output_type=TransactionAnalysis,
    tools=[
        get_customer_profile,
        get_customer_transaction_history
    ],
    system_prompt=(
        """ 
        You are a bank's transaction analysis system. 
        Given a raw transaction description "
        "that includes a customer_id, 
        you MUST call your tools first to look up that customer's "
        "profile and past transaction history before deciding anything. 
        Compare the new "transaction's country, amount, and timing 
        against their real history. Flag anything "
        "genuinely inconsistent with their pattern: 
        a country they have never transacted in, "
        "an amount far outside their normal range, 
        or odd timing combined with either. 
        Do NOT "
        "flag a large amount just because it is large 
        if it matches how this specific customer "
        normally spends.
        
        """
    ),
)



records = CustomerRecords(
    customers=CUSTOMERS
)


import streamlit as st
import asyncio

async def analise_transaction(query:str):
    result = await transaction_agent.run(
                query,
                deps=records,
            )
    return result.output


st.title("Transaction Analysis System")
query=st.text_area("Enter a transaction description (include customer_id):")

if st.button("Analyze Transaction"):

    if query.strip():

        with st.spinner("Analyzing transaction..."):

            result =asyncio.run(analise_transaction(query))

        st.markdown(result)
        st.json(result.model_dump())