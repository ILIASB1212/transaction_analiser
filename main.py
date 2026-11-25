import nest_asyncio
nest_asyncio.apply()

import os
from dotenv import load_dotenv
load_dotenv()
from src.schemas.Schemas import CustomerRecords, TransactionAnalysis

from pydantic_ai import Agent

# defining LLM
model = "google-cloud:gemini-2.5-flash" 




import json

with open("data/bank.json", encoding="utf-8") as f:
    CUSTOMERS = json.load(f)



transaction_agent = Agent(
    model,
    deps_type=CustomerRecords,
    output_type=TransactionAnalysis,
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


st.title("Transaction Analysis System")
query=st.text_area("Enter a transaction description (include customer_id):")

result1 = transaction_agent.run_async(
    query,
    deps=records,
)