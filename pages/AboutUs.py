# ---------------- TOP IMPORT FIXES ----------------
from pathlib import Path
import streamlit.components.v1 as components
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ---------------------------------------------------

import streamlit as st
import qrcode
import io

from components.NavBar.navbar import navbar
from backend.api.email_api import send_contact_email


def load_about_us_page():

    st.set_page_config(page_title="StreetBase", layout="wide")

    # ---------------- CSS ----------------
    st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    body, .block-container {
        background-color: #FFFDF2;
        color: #2b2b2b;
        font-family: 'Segoe UI', sans-serif;
        max-width: 95%;
        margin: auto;
    }

    .hero-wrapper {
        margin-top: 1.5rem;
        margin-bottom: 2.5rem;
        padding: 2.5rem 2rem;
        border-radius: 24px;
        background: radial-gradient(circle at top left, #F5B895 0, #FFFDF2 45%, #EDE9D5 100%);
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid rgba(226,114,91,0.24);
    }
    .title {
        font-size: 3rem;
        font-weight: 800;
        color: #004D00;
        margin-bottom: 0.5rem;
    }
    .title span.highlight {
        color: #E2725B;
    }
    .subtitle {
        font-size: 1.15rem;
        color: #3f3f3f;
        margin-bottom: 1.25rem;
    }
    .hero-tag {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        background: #004D00;
        color: #FFFDF2;
        text-transform: uppercase;
        margin-bottom: 0.75rem;
    }
    .hero-pills {
        margin-top: 1.4rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
    }
    .pill {
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        font-size: 0.85rem;
        border: 1px solid rgba(0,0,0,0.06);
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(6px);
    }

    .metric-card {
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-top: 4px solid #E2725B;
        margin-bottom: 0.7rem;
    }
    .metric-value {
        font-size: 1.4rem;
        font-weight: 800;
        color: #004D00;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #555;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #004D00;
        margin-top: 2.5rem;
        margin-bottom: 0.75rem;
        text-align: left;
    }
    /* ✅ helper class to center specific section titles */
    .section-center {
        text-align: center;
    }

    .section-subtitle {
        font-size: 0.98rem;
        color: #555;
        margin-bottom: 1rem;
    }

    .info-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .info-card {
        flex: 1 1 260px;
        background: #FFFFFF;
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 5px solid #F5B895;
    }
    .info-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 1.05rem;
        color: #004D00;
    }
    .info-card p {
        margin: 0;
        font-size: 0.95rem;
        color: #444;
    }
    .info-badge {
        display: inline-block;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #E2725B;
        margin-bottom: 0.35rem;
        font-weight: 600;
    }

    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
        margin-top: 0.8rem;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        border: 1px solid #E2E2E2;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    }
    .feature-card h4 {
        margin: 0 0 0.35rem 0;
        font-size: 1rem;
        color: #004D00;
    }
    .feature-card p {
        margin: 0;
        font-size: 0.9rem;
        color: #444;
    }
    .feature-tag {
        font-size: 0.8rem;
        font-weight: 600;
        color: #E2725B;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
    }

    .timeline {
        border-left: 3px solid #E2725B;
        padding-left: 1rem;
        margin-top: 0.5rem;
    }
    .timeline-item {
        margin-bottom: 0.9rem;
        position: relative;
    }
    .timeline-item::before {
        content: "";
        position: absolute;
        left: -1.2rem;
        top: 0.2rem;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        border: 2px solid #E2725B;
        background: #FFFDF2;
    }
    .timeline-item-title {
        font-size: 0.98rem;
        font-weight: 600;
        color: #004D00;
    }
    .timeline-item-text {
        font-size: 0.88rem;
        color: #555;
    }

    /* contact & feedback forms */
    div[data-testid="stForm"] {
        background-color: #FFFDF2;
        padding: 35px 40px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        max-width: 800px;
        margin: auto;
        border: 1px solid #E2E2E2;
    }
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border: 2px solid #004D00 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-size: 1rem !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .stButton button {
        background-color: #F5B895 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
        border: none !important;
    }
    .stButton button:hover {
        background-color: #E2725B !important;
        transform: scale(1.05);
    }
    .contact-success {
        text-align: center;
        color: #004D00;
        font-weight: 600;
        background-color: #EAF5EA;
        border-radius: 10px;
        padding: 12px;
        margin-top: 15px;
    }

    .footer {
        text-align: center;
        color: #004D00;
        background-color: #EDE9D5;
        padding: 1.5rem 0;
        margin-top: 3rem;
        border-top: 2px solid #E2725B;
    }
    hr {
        border: none;
        height: 2px;
        background-color: #E2725B;
        margin: 3rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- NAVBAR ----------------
    navbar()

    # ---------------- HERO / INTRO ----------------
    hero_col1, hero_col2 = st.columns([2, 1], gap="large")
    with hero_col1:
        st.markdown(
            """
            <div class="hero-wrapper">
                <div class="hero-tag">About StreetBase</div>
                <div class="title">Smarter <span class="highlight">Real Estate Decisions</span> with Data & AI</div>
                <div class="subtitle">
                    StreetBase is an AI-powered real estate evaluation system that helps buyers, sellers,
                    and advisors estimate fair property values, understand market trends, and make
                    sustainable housing choices with confidence.
                </div>
                <div class="subtitle">
                    Instead of relying only on guesswork or brokers, StreetBase combines location data,
                    property attributes, and machine learning to give you transparent, explainable insights.
                </div>
                <div class="hero-pills">
                    <span class="pill">🏙 City-level & locality insights</span>
                    <span class="pill">📈 AI-driven price predictions</span>
                    <span class="pill">🌿 Sustainability-aware recommendations</span>
                    <span class="pill">🔍 Transparent & explainable outputs</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_col2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-value">₹</div>
                <div class="metric-label">Price intelligence for properties based on multiple factors like location, area, amenities, and historical trends.</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">24×7</div>
                <div class="metric-label">Digital assistant to help you explore “What-if” scenarios and compare properties.</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">Sustainable</div>
                <div class="metric-label">Designed to nudge users towards greener, energy-efficient homes and better long-term investments.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ---------------- WHY STREETBASE ----------------
    st.markdown("<h2 class='section-title'>Why StreetBase?</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>"
        "Real estate decisions in India are often influenced by hearsay, outdated listings, or biased suggestions. "
        "StreetBase aims to change that by putting data, transparency, and sustainability at the center of every decision."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-row">
            <div class="info-card">
                <div class="info-badge">The Challenge</div>
                <h4>Unclear Pricing & Market Noise</h4>
                <p>
                    Property prices can vary wildly even within the same locality. Traditional methods rarely
                    account for micro-location, connectivity, quality of construction, and future growth potential.
                </p>
            </div>
            <div class="info-card">
                <div class="info-badge">Our Approach</div>
                <h4>Data-Driven Evaluations</h4>
                <p>
                    StreetBase uses machine learning models trained on historical patterns and engineered features
                    to predict realistic price ranges and highlight the key drivers behind them.
                </p>
            </div>
            <div class="info-card">
                <div class="info-badge">The Impact</div>
                <h4>Confident, Sustainable Choices</h4>
                <p>
                    Buyers, sellers, and agents get a common reference point, reducing information asymmetry and
                    promoting decisions that are financially sound and environmentally conscious.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ---------------- HOW STREETBASE WORKS ----------------
    st.markdown("<h2 class='section-title'>How StreetBase Works</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-subtitle'>From raw property details to actionable insights, StreetBase follows a clear and explainable pipeline.</p>",
        unsafe_allow_html=True,
    )

    work_col1, work_col2 = st.columns(2, gap="large")
    with work_col1:
        st.markdown(
            """
            <div class="timeline">
                <div class="timeline-item">
                    <div class="timeline-item-title">1. Collect Property Inputs</div>
                    <div class="timeline-item-text">
                        Users provide details like location, area (sq.ft), BHK, age of building, amenities,
                        and connectivity. These become the core features for our models.
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-item-title">2. Feature Engineering</div>
                    <div class="timeline-item-text">
                        We enrich the inputs with locality scores, proximity to key landmarks, and sustainability
                        indicators such as access to public transport or green spaces.
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-item-title">3. ML-Based Price Prediction</div>
                    <div class="timeline-item-text">
                        Using trained regression models, StreetBase generates an estimated price range and
                        confidence band for the property.
                    </div>
                </div>
                <div class="timeline-item">
                    <div class="timeline-item-title">4. Insight & Recommendation Layer</div>
                    <div class="timeline-item-text">
                        The system highlights why a price is high or low and suggests actions such as negotiation
                        room, comparable localities, and more sustainable alternatives if available.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with work_col2:
        st.markdown(
            """
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-tag">Price Intelligence</div>
                    <h4>Fair Value Estimation</h4>
                    <p>
                        Predicts a realistic price range instead of a single static number, helping you see the
                        upper and lower bounds of negotiations.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-tag">Scenario Analysis</div>
                    <h4>What-If Comparisons</h4>
                    <p>
                        Compare different property configurations, locations, or budgets to understand trade-offs
                        before making a commitment.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-tag">Sustainability</div>
                    <h4>Green Home Indicators</h4>
                    <p>
                        Incorporates aspects like daylight, ventilation, and connectivity to public transport to
                        encourage more sustainable living.
                    </p>
                </div>
                <div class="feature-card">
                    <div class="feature-tag">User-Centric</div>
                    <h4>Explainable AI</h4>
                    <p>
                        Uses interpretable techniques to show which features influence the predicted price the most,
                        building trust with end users.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # ---------------- FUTURE SCOPE ----------------
    st.markdown("<h2 class='section-title'>🚀 Future Scope</h2>", unsafe_allow_html=True)
    st.markdown(
        """
        - 🌍 **Live Real Estate API Integration** – connect to real-time listings and transaction data.  
        - ☁️ **Cloud Deployment (AWS / GCP)** – scalable infrastructure for city-level evaluations.  
        - 🧠 **Explainable AI (SHAP, LIME)** – deeper interpretability for end users and partners.  
        - 📊 **Interactive Analytics Dashboard** – visualize trends across cities, localities, and property types.  
        - 🤖 **Integrated Chatbot Assistant** – guided exploration for first-time buyers and investors.  
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ---------------- CONTACT FORM ----------------
    st.markdown("<div id='contact_section'></div>", unsafe_allow_html=True)
    # ✅ centered title now
    st.markdown("<h2 class='section-title section-center'>📬 Contact Us</h2>", unsafe_allow_html=True)

    with st.form("contact_form"):
        name = st.text_input("Your Name", placeholder="Enter your full name")
        email = st.text_input("Your Email", placeholder="Enter your email address")
        message = st.text_area("Your Message", placeholder="Type your message here...")

        submitted = st.form_submit_button("Send Message")

        if submitted:
            if not name or not email or not message:
                st.error("⚠️ Please fill out all fields.")
            else:
                result = send_contact_email(name, email, message)

                if result["status"]:
                    st.markdown(
                        '<div class="contact-success">✅ Thank you! We will reach out soon.</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"❌ Email failed: {result['error']}")

    st.divider()

    # ---------------- FEEDBACK FORM (NEW) ----------------
    st.markdown("<h2 class='section-title section-center'>📝 Share Your Feedback</h2>", unsafe_allow_html=True)

    with st.form("feedback_form"):
        fb_name = st.text_input("Your Name (optional)", placeholder="Enter your name or nickname")
        fb_feedback = st.text_area(
            "Your Feedback",
            placeholder="Tell us what you liked, what felt confusing, or what you'd love to see next..."
        )

        fb_submitted = st.form_submit_button("Submit Feedback")

        if fb_submitted:
            if not fb_feedback:
                st.error("⚠️ Please add some feedback before submitting.")
            else:
                # 👉 Here you can later plug in DB / email / logging
                st.markdown(
                    '<div class="contact-success">🙏 Thanks! Your feedback has been recorded.</div>',
                    unsafe_allow_html=True
                )

    st.divider()

    # ---------------- CONNECT WITH US ----------------
    st.markdown("<h2 class='section-title'>🌐 Connect With Us</h2>", unsafe_allow_html=True)

    st.markdown(
        """
        <p class='section-subtitle'>
        Have ideas, data sources, or want to collaborate with StreetBase for your city or organization?
        Reach out and let's build smarter housing ecosystems together.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_contact, col_qr = st.columns([2, 1])
    with col_contact:
        st.write("📧 **Email:** streetbase5@gmail.com")
        st.write("🌍 **Website:** www.streetbase.ai")
        st.write("📂 **Project Repo / Demo:** Scan the QR code to explore the codebase or live demo (if hosted).")

    with col_qr:
        try:
            qr = qrcode.make("https://github.com/your-project-repo")
            buf = io.BytesIO()
            qr.save(buf, format="PNG")
            st.image(buf.getvalue(), width=130)
        except Exception:
            st.write("QR Code could not be generated")

    # ---------------- CHATBOT ----------------
    from components.chatbot_ui import chatbot_popup
    chatbot_popup()  # render the StreetBase chat

    # ---------------- FOOTER ----------------
    st.markdown("---")
    st.markdown(
        """
        <div class='footer'>
            © 2025 <b>StreetBase</b> | All Rights Reserved <br>
            Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
        </div>
    """,
        unsafe_allow_html=True,
    )


# ---- Auto-scroll if coming from Expert Review button ----
if st.session_state.get("scroll_to_contact", False):
    components.html(
        """
        <script>
        const parentDoc = window.parent ? window.parent.document : document;
        const target = parentDoc.getElementById("contact_section");
        if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
        </script>
        """,
        height=0,
    )
    st.session_state.scroll_to_contact = False
