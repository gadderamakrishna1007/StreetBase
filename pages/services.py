from components.chatbot_ui import chatbot_popup
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from components.NavBar.navbar import navbar
import os
from backend.api.request_quote_api import send_quote_email


def load_services_page():
    # --- PAGE CONFIG ---
    st.set_page_config(page_title="Our Services | AI Real Estate", page_icon="🏠", layout="wide")

    # --- SHARED FOOTER CSS (same across app) ---
    st.markdown("""
    <style>
    .footer {
        text-align: center;
        color: #004D00;
        background-color: #EDE9D5;
        padding: 1.5rem 0;
        margin-top: 3rem;
        border-top: 2px solid #E2725B;
        font-family: 'Segoe UI', sans-serif;
    }
    .footer a {
        color: #E2725B;
        text-decoration: none;
        font-weight: 600;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- NAVBAR ---
    navbar()

    # --- LOAD LOTTIE ANIMATION FUNCTION ---
    import json

    def load_lottie_file(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)

    # --- LOAD ANIMATIONS (AI, Analytics, Market Trend) ---
    base_path = os.path.join(os.path.dirname(__file__), "..", "Assets")

    ai_data = load_lottie_file(os.path.join(base_path, "ai_data.json"))
    analytics_viz = load_lottie_file(os.path.join(base_path, "analytics_viz.json"))
    market_forecast = load_lottie_file(os.path.join(base_path, "market_forecast.json"))

    # --- CUSTOM CSS (Brand Palette: Light + Dark Ready) ---
    st.markdown("""
    <style>
    /* Base */
    body, [data-testid="stAppViewContainer"]{
      background-color:#F2F2F6;
      color:#1a1f36;
      font-family:'Inter',sans-serif;
    }

    /* Headings */
    h2, h3, h4{
      text-align:center;
      color:#0f172a;
    }
    h2{ font-weight:800; margin-bottom:.6em; }
    h3{ color:#1d4ed8; margin-bottom:1.6em; }
    h4{ color:#0f172a; }

    /* Service Card */
    .service-card{
      background:#fff;
      border-radius:16px;
      box-shadow:0 4px 20px rgba(0,0,0,.05);
      padding:30px;
      transition:all .4s ease;
      border:1px solid #cbd5e1;
    }
    .service-card:hover{
      transform:translateY(-6px) scale(1.02);
      box-shadow:0 8px 25px rgba(0,51,102,.2);
    }
    .service-card p{
      color:#334155;
    }

    /* Lottie wrapper */
    .lottie-container{ transition:transform .4s ease; }
    .lottie-container:hover{ transform:scale(1.1); }

    /* Lists */
    .benefits{
      text-align:left;
      font-size:15px;
      color:#0f172a;
    }
    .benefits li{ margin-bottom:6px; }

    /* CTA Button */
    .cta-button{
      background:#FF6600;
      color:#fff;
      border:none;
      border-radius:8px;
      padding:8px 16px;
      font-weight:600;
      text-decoration:none;
      transition:.3s ease;
    }
    .cta-button:hover{
      background:#e65c00;
      transform:scale(1.05);
    }

    /* Pricing Table */
    .pricing-table{
      width:100%;
      border-collapse:collapse;
      margin-top:40px;
      font-size:15px;
      border:1px solid #cbd5e1;
    }
    .pricing-table th, .pricing-table td{
      border:1px solid #cbd5e1;
      padding:14px;
      text-align:center;
      color:#0f172a;
    }
    .pricing-table th{
      background:#0f172a;
      color:#fff;
      font-weight:700;
    }
    .pricing-table tr:nth-child(even){ background:#eef2f7; }
    .pricing-table tr:hover{ background:#e2e8f0; }

    /* Inputs */
    input, textarea, select{
      border-radius:6px !important;
      border:1px solid #cbd5e1 !important;
      padding:6px 10px !important;
      color:#1a1f36;
    }

    a{ color:#1d4ed8; }
    a:hover{ color:#1e40af; }
    </style>
    """, unsafe_allow_html=True)

    # --- PAGE HEADER ---
    st.markdown("<h2>Our Services</h2>", unsafe_allow_html=True)
    st.markdown("<h3>Empowering Real Estate Decisions with Artificial Intelligence</h3>", unsafe_allow_html=True)
    st.write("")

    # --- SERVICE DATA ---
    services = [
        {
            "title": "AI & Data Prediction Services",
            "desc": "Get precise property valuations using AI models trained on historical market data and regional trends.",
            "benefits": [
                "Accurate and instant price estimates",
                "Data-driven decision making",
                "Localized model predictions",
                "Automated valuation insights"
            ],
            "animation": ai_data
        },
        {
            "title": "Analytics & Visualization Services",
            "desc": "Visualize property market trends through AI-powered dashboards and interactive analytics.",
            "benefits": [
                "Interactive charts & trend maps",
                "Real-time analytics dashboards",
                "Location-based market visualization",
                "Customizable reporting tools"
            ],
            "animation": analytics_viz
        },
        {
            "title": "Market Trend Forecasting",
            "desc": "Leverage machine learning to forecast future property price movements and demand fluctuations.",
            "benefits": [
                "AI-driven trend forecasting",
                "Region-wise growth prediction",
                "Investment timing recommendations",
                "Dynamic data visualization"
            ],
            "animation": market_forecast
        },
    ]

    # --- DISPLAY SERVICE CARDS ---
    for service in services:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            st.markdown(f"""
            <div class="service-card">
                <h4>{service['title']}</h4>
                <p style='color:#555; font-size:16px;'>{service['desc']}</p>
                <ul class="benefits">
                    {''.join(f"<li> {b}</li>" for b in service['benefits'])}
                </ul>
                <br>
                <a class="cta-button" href="#quote-form">Get Quote</a>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            with st.container():
                st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
                if service["animation"]:
                    st_lottie(service["animation"], height=260, key=service["title"])
                else:
                    st.info("Animation could not load.")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    # (Pricing + Quote form commented out for now in your original code)

    chatbot_popup()  # 👈 StreetBase chat

    # --- FOOTER ---
    st.markdown("""
        <div class='footer'>
            © 2025 <b>StreetBase</b> | All Rights Reserved <br>
            Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
        </div>
    """, unsafe_allow_html=True)
