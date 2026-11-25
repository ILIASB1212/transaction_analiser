
from base64 import b64encode
from html import escape
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from src.schemas.Schemas import TransactionAnalysis


# ==========================================
# GLOBAL STYLING
# ==========================================

def apply_styles():

    st.html("""
    <style>

    .stApp {
        background: #F3F6FA;
        color: #14243B;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 4rem;
        padding-bottom: 3rem;
    }

    .stApp label p {
        color: #34465F;
        font-weight: 600;
    }

    /* Transaction input */

    [data-testid="stTextArea"] textarea {
        background: #FFFFFF;
        color: #14243B;
        border: 1px solid #CBD5E1;
        border-radius: 12px;
        font-size: 16px;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #52647B;
        opacity: 1;
    }

    [data-testid="stTextArea"] textarea:focus-visible,
    .stFormSubmitButton button:focus-visible {
        outline: 2px solid #24558A;
        outline-offset: 2px;
    }

    [data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid #DCE4EE;
        border-radius: 16px;
        padding: 24px;
    }

    .stButton button,
    .stFormSubmitButton button {
        background: #163B68;
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 44px;
        transition: background 0.2s ease;
    }

    .stFormSubmitButton button:hover {
        background: #24558A;
        color: white;
    }

    /* Dashboard header */

    .dashboard-header {
        background: linear-gradient(
            120deg,
            #102740,
            #1C4169
        );
        border-radius: 20px;
        padding: 36px;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }

    .dashboard-header::after {
        content: "";
        position: absolute;
        right: -50px;
        top: -120px;
        width: 330px;
        height: 330px;
        border: 1px solid #FFFFFF22;
        border-radius: 50%;
        box-shadow:
            0 0 0 35px #FFFFFF08,
            0 0 0 70px #FFFFFF05;
        pointer-events: none;
    }

    .dashboard-header .header-title {
        color: #FFFFFF;
        font-size: 34px;
        font-weight: 750;
        letter-spacing: -1.2px;
        margin: 0 0 8px;
        padding: 0;
        position: relative;
        z-index: 1;
    }

    .header-description {
        font-size: 14px;
        color: #C0D1E3;
        position: relative;
        z-index: 1;
    }

    /* System information */

    .system-info {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        color: #64748B;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 24px;
    }

    .system-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #16A085;
    }

    /* Section headings */

    h2.section-title {
        color: #14243B;
        font-size: 20px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin: 24px 0 16px;
        padding: 0;
    }

    /* Metric cards */

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 16px;
    }

    .metric-card {
        background: #FFFFFF;
        border: 1px solid #DCE4EE;
        border-radius: 16px;
        padding: 22px;
        min-height: 170px;
        min-width: 0;
        box-sizing: border-box;
        box-shadow: 0 4px 16px rgba(20, 36, 59, 0.04);
        transition: transform 0.2s ease,
                    box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(20, 36, 59, 0.08);
    }

    .metric-heading {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
    }

    .metric-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: #EDF3FA;
        color: #285786;
        flex-shrink: 0;
    }

    .metric-value {
        margin-top: 20px;
        font-size: clamp(18px, 2.2vw, 30px);
        font-weight: 750;
        color: #14243B;
        letter-spacing: -0.8px;
        line-height: 1.2;
        overflow-wrap: anywhere;
        font-variant-numeric: tabular-nums;
    }

    .metric-description {
        margin-top: 8px;
        font-size: 11px;
        color: #64748B;
    }

    /* Risk score progress bar */

    .risk-track {
        background: #E8EEF5;
        height: 7px;
        border-radius: 20px;
        margin-top: 14px;
        overflow: hidden;
    }

    .risk-fill {
        height: 100%;
        border-radius: 20px;
        animation: reveal-risk 0.7s ease-out;
    }

    @keyframes reveal-risk {
        from {
            transform: scaleX(0);
            transform-origin: left;
        }
        to {
            transform: scaleX(1);
            transform-origin: left;
        }
    }

    /* Reasoning report */

    .reasoning-card {
        background: #FFFFFF;
        border: 1px solid #DCE4EE;
        border-radius: 18px;
        padding: 28px;
        margin-top: 20px;
        box-shadow: 0 4px 16px rgba(20, 36, 59, 0.04);
    }

    .reasoning-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        border-bottom: 1px solid #E8EDF4;
        padding-bottom: 18px;
    }

    h2.reasoning-title {
        font-size: 18px;
        font-weight: 700;
        color: #14243B;
        margin: 0;
        padding: 0;
    }

    .status-badge {
        font-size: 12px;
        font-weight: 650;
        border-radius: 30px;
        padding: 7px 14px;
    }

    .reasoning-content {
        color: #34465F;
        font-size: 15px;
        line-height: 1.9;
        margin-top: 20px;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .report-footer {
        margin-top: 24px;
        padding-top: 16px;
        border-top: 1px solid #E8EDF4;
        font-size: 11px;
        color: #64748B;
    }

    /* Responsive layout */

    @media (max-width: 850px) {

        .metric-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .dashboard-header {
            padding: 26px;
        }
    }

    @media (max-width: 480px) {

        .metric-grid {
            grid-template-columns: 1fr;
        }

        .dashboard-header .header-title {
            font-size: 26px;
        }

        .reasoning-card {
            padding: 18px;
        }

        .metric-card {
            min-height: 140px;
        }
    }

    @media (prefers-reduced-motion: reduce) {

        .metric-card,
        .risk-fill {
            animation: none;
            transition: none;
        }
    }

    </style>
    """)


# ==========================================
# SVG ICONS
# ==========================================

ICONS = {

    "category": """
        <rect x="3" y="3" width="7" height="7" rx="1"/>
        <rect x="14" y="3" width="7" height="7" rx="1"/>
        <rect x="3" y="14" width="7" height="7" rx="1"/>
        <rect x="14" y="14" width="7" height="7" rx="1"/>
    """,

    "amount": """
        <rect x="2" y="5" width="20" height="14" rx="2"/>
        <circle cx="12" cy="12" r="3"/>
        <path d="M6 12h.01M18 12h.01"/>
    """,

    "shield": """
        <path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/>
        <path d="m9 12 2 2 4-4"/>
    """,

    "alert": """
        <path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"/>
        <path d="M12 8v5"/>
        <circle cx="12" cy="16" r=".5"/>
    """,

    "score": """
        <path d="M4 19a9 9 0 1 1 16 0"/>
        <path d="m12 13 4-4"/>
        <circle cx="12" cy="13" r="1"/>
    """,
}


def get_icon(name):

    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 24 24"
         fill="none"
         stroke="#285786"
         stroke-width="1.7"
         stroke-linecap="round"
         stroke-linejoin="round">
        {ICONS[name]}
    </svg>
    """.strip()
    # Streamlit sanitizes inline SVG in st.html but accepts images.
    encoded_svg = b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{encoded_svg}" width="18" height="18" alt="">'


# ==========================================
# HEADER
# ==========================================

def render_header():

    st.html("""
    <div class="dashboard-header">

        <h1 class="header-title">
            Transaction Intelligence
        </h1>

        <div class="header-description">
            Evaluate transactions against customer behavior
            and identify unusual spending patterns.
        </div>

    </div>

    <div class="system-info">
        <span class="system-dot"></span>
        GPT-OSS-20B
        &nbsp; / &nbsp;
        SYNTHETIC BANKING DATA
        &nbsp; / &nbsp;
        MAD
    </div>
    """)


# ==========================================
# RISK CLASSIFICATION
# ==========================================

def get_risk_style(score):

    if score < 30:
        return "Low risk", "#08795A"

    elif score < 70:
        return "Moderate risk", "#945D0E"

    else:
        return "High risk", "#C53030"


# ==========================================
# REUSABLE METRIC COMPONENT
# ==========================================

def metric_card(
    label,
    value,
    description,
    icon,
    color="#14243B",
    extra=""
):

    return f"""
    <div class="metric-card">

        <div class="metric-heading">

            <div class="metric-icon">
                {get_icon(icon)}
            </div>

            {escape(str(label))}

        </div>

        <div class="metric-value" style="color:{color}">
            {escape(str(value))}
        </div>

        <div class="metric-description">
            {escape(str(description))}
        </div>

        {extra}

    </div>
    """


# ==========================================
# MAIN DASHBOARD
# ==========================================

def render_dashboard(result: "TransactionAnalysis | dict | None"):

    # Do not display anything without a result
    if result is None:
        return

    # Existing Streamlit sessions may still hold the serialized assessment.
    data = result if isinstance(result, dict) else result.model_dump(mode="json")

    category = data["category"].replace("_", " ").title()

    amount = float(data["amount"])

    score = max(
        0,
        min(100, int(data["fraud_risk_score"]))
    )

    flagged = data["flagged"]

    reasoning = data["reasoning"]

    risk_label, risk_color = get_risk_style(score)

    # Dynamic flagged status

    if flagged:

        status = "Review required"
        status_color = "#B42318"
        status_background = "#FEE4E2"
        status_icon = "alert"

    else:

        status = "Not flagged"
        status_color = "#08795A"
        status_background = "#DDF5EA"
        status_icon = "shield"

    # Progress bar

    progress_bar = f"""
    <div class="risk-track"
         role="progressbar"
         aria-label="Fraud risk score"
         aria-valuenow="{score}"
         aria-valuemin="0"
         aria-valuemax="100">

        <div class="risk-fill"
             style="width:{score}%;background:{risk_color}">
        </div>

    </div>
    """

    # Four metric cards

    cards = [

        metric_card(
            label="Category",
            value=category,
            description="Transaction classification",
            icon="category",
        ),

        metric_card(
            label="Amount",
            value=f"{amount:,.2f} MAD",
            description="Transaction value",
            icon="amount",
        ),

        metric_card(
            label="Flagged",
            value="Yes" if flagged else "No",
            description=status,
            icon=status_icon,
            color=status_color,
        ),

        metric_card(
            label="Fraud risk score",
            value=f"{score}/100",
            description=risk_label,
            icon="score",
            color=risk_color,
            extra=progress_bar,
        ),

    ]

    # Render metric cards

    dashboard_html = (
        '<h2 class="section-title">Assessment overview</h2>'
        '<div class="metric-grid">'
        + "".join(cards)
        + '</div>'
    )

    st.html(dashboard_html)

    # Render reasoning panel

    st.html(f"""
    <div class="reasoning-card">

        <div class="reasoning-header">

            <h2 class="reasoning-title">
                Analysis &amp; reasoning
            </h2>

            <span class="status-badge"
                  style="color:{status_color};
                         background:{status_background}">
                {status}
            </span>

        </div>

        <div class="reasoning-content">{escape(reasoning)}</div>

        <div class="report-footer">
            AI-generated assessment &nbsp; · &nbsp;
            Synthetic customer data &nbsp; · &nbsp;
            Not a calibrated fraud probability
        </div>

    </div>
    """)

    # Raw JSON for debugging

    with st.expander("View structured JSON output"):

        st.json(data)


# ==========================================
# EMPTY STATE
# ==========================================

def render_empty_state():

    # Intentionally hidden until a transaction is analyzed.
    return None
