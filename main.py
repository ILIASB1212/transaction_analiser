

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



from html import escape
from pydantic_ai.exceptions import UnexpectedModelBehavior, ModelRequestRejectedError

st.set_page_config(page_title="Transaction Intelligence", page_icon="◈", layout="wide")

st.markdown("""
<style>
.stApp {background:#f3f6fa;color:#14243b;}
[data-testid="stHeader"] {background:transparent;}
.block-container {max-width:1160px;padding-top:2.5rem;padding-bottom:3rem;}
.stApp h1,.stApp h2,.stApp h3 {color:#14243b;}
.stApp label,.stApp label p {color:#34465f;}
[data-testid="stTextArea"] textarea {background:#fff;color:#14243b;border:1px solid #cbd5e1;border-radius:12px;font-size:15px;}
.stButton button {background:#163b68;color:white;border:0;border-radius:10px;font-weight:650;min-height:44px;}
.stButton button:hover {background:#24558a;color:white;}
.ti-hero {background:#102740;color:white;border-radius:20px;padding:32px 36px;margin-bottom:28px;position:relative;overflow:hidden;}
.ti-hero:after {content:"";position:absolute;right:-48px;top:-110px;width:320px;height:320px;border:1px solid #ffffff24;border-radius:50%;box-shadow:0 0 0 35px #ffffff08,0 0 0 70px #ffffff05;pointer-events:none;}
.ti-kicker {font-size:11px;letter-spacing:.16em;font-weight:700;color:#8db4db;text-transform:uppercase;}
.ti-hero h1 {color:#fff;font-size:34px;letter-spacing:-1.2px;margin:10px 0 5px;padding:0;}
.ti-hero p {color:#c0d1e3;font-size:14px;margin:0;}
.ti-section {font-size:19px;font-weight:700;letter-spacing:-.3px;color:#14243b;margin:26px 0 14px;}
.ti-grid {display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;}
.ti-card {background:white;border:1px solid #dce4ee;border-radius:15px;padding:20px;min-height:148px;box-shadow:0 3px 12px #14243b06;min-width:0;}
.ti-label {display:flex;align-items:center;gap:9px;color:#53657c;font-size:12px;font-weight:650;}
.ti-icon {display:grid;place-items:center;background:#edf3fa;color:#285786;width:30px;height:30px;border-radius:8px;flex-shrink:0;}
.ti-value {font-size:clamp(18px,2.1vw,28px);font-weight:750;letter-spacing:-.7px;margin:16px 0 4px;color:#14243b;overflow-wrap:anywhere;line-height:1.2;}
.ti-meta {font-size:11px;color:#64748b;}
.ti-track {height:6px;background:#e8eef5;border-radius:8px;margin-top:12px;overflow:hidden;}
.ti-fill {height:100%;border-radius:8px;}
.ti-report {background:white;border:1px solid #dce4ee;border-radius:16px;padding:26px 28px;margin-top:18px;box-shadow:0 3px 12px #14243b06;}
.ti-report-head {display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;border-bottom:1px solid #e8edf4;padding-bottom:15px;}
.ti-report-title {font-size:18px;font-weight:700;color:#14243b;}
.ti-status {font-size:11px;font-weight:700;padding:6px 11px;border-radius:20px;}
.ti-report-body {font-size:15px;line-height:1.8;color:#34465f;padding-top:16px;white-space:pre-wrap;overflow-wrap:anywhere;}
.ti-foot {font-size:11px;color:#64748b;margin-top:16px;}
@media(max-width:850px){.ti-grid{grid-template-columns:repeat(2,minmax(0,1fr));}.ti-hero{padding:25px;}}
@media(max-width:480px){.ti-grid{grid-template-columns:1fr;}.ti-hero h1{font-size:26px;}.ti-report{padding:18px;}}
</style>
<div class="ti-hero"><div class="ti-kicker">Risk intelligence / Analyst workspace</div><h1>Transaction intelligence</h1><p>Evaluate individual transactions against customer spending history.</p></div>
""", unsafe_allow_html=True)

st.caption("SYNTHETIC DATA  ·  GPT-OSS-20B  ·  MAD")
with st.form("transaction_form"):
    query = st.text_area("Transaction description", placeholder="Customer CUST-0040 spent 150 MAD on shopping in Marrakech, Morocco.", height=110)
    submitted = st.form_submit_button("Run risk assessment", type="primary")

if submitted:
    st.session_state.pop("assessment", None)
    if not query.strip():
        st.warning("Enter a customer ID, amount, category and location.")
    else:
        try:
            with st.spinner("Assessing transaction against customer history..."):
                st.session_state["assessment"] = asyncio.run(analise_transaction(query)).model_dump(mode="json")
        except (UnexpectedModelBehavior, ModelRequestRejectedError):
            st.error("The assessment could not be completed. Check the customer ID, amount, category and location, then try again.")

def metric(label, value, subtitle, path, extra=""):
    icon = f'<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    return f'<div class="ti-card"><div class="ti-label"><span class="ti-icon">{icon}</span>{escape(label)}</div><div class="ti-value">{escape(value)}</div><div class="ti-meta">{escape(subtitle)}</div>{extra}</div>'

data = st.session_state.get("assessment")
if data:
    score = int(data["fraud_risk_score"])
    flagged = bool(data["flagged"])
    tone = "#b42318" if flagged else "#08795a"
    score_tone = "#08795a" if score < 30 else "#a15c00" if score < 70 else "#b42318"
    status = "Review required" if flagged else "Not flagged"
    cards = [
        metric("Category", str(data["category"]).replace("_", " ").title(), "Transaction classification", '<path d="M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z"/>'),
        metric("Amount", f'{data["amount"]:,.2f} MAD', "Transaction value", '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="12" cy="12" r="3"/>'),
        metric("Flagged", "Yes" if flagged else "No", status, '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/><path d="m9 12 2 2 4-4"/>'),
        metric("Risk score", f"{score}/100", "Model risk assessment", '<path d="M4 19a9 9 0 1 1 16 0M12 13l4-4"/><circle cx="12" cy="13" r="1"/>', f'<div class="ti-track"><div class="ti-fill" style="width:{score}%;background:{score_tone}"></div></div>'),
    ]
    st.markdown('<div class="ti-section">Assessment overview</div><div class="ti-grid">' + "".join(cards) + '</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ti-report"><div class="ti-report-head"><div class="ti-report-title">Analysis &amp; reasoning</div><span class="ti-status" style="color:{tone};background:{tone}12">{status}</span></div><div class="ti-report-body">{escape(data["reasoning"])}</div><div class="ti-foot">AI-generated assessment • Synthetic customer data • Not a calibrated fraud probability or final banking decision.</div></div>', unsafe_allow_html=True)
    with st.expander("Structured output"):
        st.json(data)
else:
    st.info("Submit a transaction to view its risk assessment.")
