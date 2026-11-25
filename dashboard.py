import streamlit as st
import asyncio
from main import transaction_agent, records
async def analise_transaction(query: str):
    result = await transaction_agent.run(
        query,
        deps=records,
    )
    return result.output

st.title("Transaction Analysis System")

query = st.text_area("Enter a transaction description (include customer_id):")

if st.button("Analyze Transaction"):
    if query.strip():
        with st.spinner("Analyzing transaction..."):
            result = asyncio.run(analise_transaction(query))
            data = result.model_dump()

        st.markdown("""
        <style>
        .metric-box {
            border: 4px solid black;
            height: 120px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-bottom: 10px;
            background-color: white;
        }

        .metric-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
            text-transform: uppercase;
        }

        .metric-value {
            font-size: 22px;
            font-weight: 600;
        }

        .reason-box {
            border: 4px solid black;
            min-height: 180px;
            padding: 18px;
            background-color: white;
            margin-top: 20px;
        }

        .reason-title {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 12px;
            text-transform: uppercase;
        }

        .reason-text {
            font-size: 17px;
            line-height: 1.6;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Category</div>
                <div class="metric-value">{data["category"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Amount</div>
                <div class="metric-value">{data["amount"]} MAD</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            flagged_text = "YES" if data["flagged"] else "NO"
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Flagged</div>
                <div class="metric-value">{flagged_text}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-title">Score</div>
                <div class="metric-value">{data["fraud_risk_score"]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="reason-box">
            <div class="reason-title">Reasoning</div>
            <div class="reason-text">{data["reasoning"]}</div>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Please enter a transaction.")