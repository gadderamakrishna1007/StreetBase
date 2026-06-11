from components.chatbot_ui import chatbot_popup
import streamlit as st
from components.NavBar.navbar import navbar


def load_case_studies_page():
    # ---------------- PAGE CONFIG ----------------
    st.set_page_config(
        page_title="Case Studies | StreetBase AI",
        page_icon="🏙️",
        layout="wide",
    )

    # ---------------- CUSTOM STYLES ----------------
    st.markdown(
        """
        <style>
            body { background-color: #f9fafc; font-family: 'Poppins', sans-serif; }

            /* --- CASE STUDY BUTTONS --- */
            div.stButton > button {
                background-color: white;
                border: 2px solid black;
                color: #002244;
                font-weight: 600;
                border-radius: 10px;
                padding: 0.7em 1em;
                transition: all 0.3s ease;
            }
            div.stButton > button:hover {
                background-color: #FFD8B0 !important; /* light orange */
                color: #002244 !important; /* dark blue text for contrast */
                border: 2px solid #FF6600 !important;
                transform: translateY(-2px);
                box-shadow: 0 4px 10px rgba(255, 102, 0, 0.3);
            }

            .title {
                text-align: center;
                font-size: 2.6rem;
                font-weight: 700;
                color: #002244;
                margin-top: 0.3em;
                letter-spacing: 0.5px;
            }
            .subtitle {
                text-align: center;
                font-size: 1.15rem;
                color: #666;
                margin-bottom: 2.2em;
            }
            .card {
                background-color: white;
                border-radius: 18px;
                box-shadow: 0 3px 12px rgba(0,0,0,0.08);
                padding: 1.2em;
                transition: 0.3s;
                height: 100%;
                cursor: pointer;
                border-top: 4px solid #FF6600;
            }
            .card:hover {
                transform: translateY(-6px);
                box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            }
            .card img {
                border-radius: 12px;
                margin-bottom: 1em;
                width: 100%;
                height: 180px;
                object-fit: cover;
            }
            .card-title {
                color: #003366;
                font-size: 1.25rem;
                font-weight: 700;
                margin-bottom: 0.3em;
            }
            .card-location {
                color: #FF6600;
                font-weight: 600;
                font-size: 0.9rem;
                margin-bottom: 0.5em;
            }
            .card-text {
                color: #333;
                font-size: 0.9rem;
                line-height: 1.5;
            }
            .detail-box {
                background-color: #ffffff;
                border-radius: 16px;
                box-shadow: 0 4px 14px rgba(0,0,0,0.08);
                padding: 2em;
                margin-top: 1.5em;
            }
            .metric {
                background-color: #f5f8ff;
                border-left: 5px solid #4B8BFF;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 0.95rem;
                margin: 6px 0;
            }
            .impact {
                background-color: #FFF5E6;
                border-left: 5px solid #FF6600;
                padding: 12px 16px;
                border-radius: 10px;
                font-size: 0.95rem;
                margin: 6px 0;
            }
            .btn-back {
                text-align: center;
                margin-top: 1.2em;
            }
            .btn-back button {
                background-color: #003366 !important;
                color: white !important;
                border-radius: 10px;
                padding: 0.6em 1.5em;
                font-weight: 600;
            }
            .btn-back button:hover {
                background-color: #004B8D !important;
            }

            /* --- Footer (same style as About Us page) --- */
            .footer {
                text-align: center;
                color: #004D00;
                background-color: #EDE9D5;
                padding: 1.5rem 0;
                margin-top: 3rem;
                border-top: 2px solid #E2725B;
            }
            .footer a {
                color: #E2725B;
                text-decoration: none;
            }
            .footer a:hover {
                text-decoration: underline;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- NAVBAR ----------------
    navbar()

    # ---------------- HEADER ----------------
    st.markdown("<div class='title'>🏗️ Case Studies</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='subtitle'>Real-world AI Transformations in India's Real Estate Market</div>",
        unsafe_allow_html=True,
    )

    # ---------------- SESSION STATE ----------------
    if "selected_case" not in st.session_state:
        st.session_state.selected_case = None

    selected_case = st.session_state.selected_case

    # ---------------- CASE STUDY GRID ----------------
    if selected_case is None:
        st.markdown(
            """
        <div style='text-align: center; font-size: 1.3rem; font-weight: 500; color: #333; margin-bottom: 1.5em;'>
        🌍 Explore how AI is reshaping the Indian property landscape
        </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.image(
                "https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=800&q=80"
            )
            st.caption(
                "AI models bring price accuracy and speed to Mumbai’s complex housing market."
            )
            if st.button(
                "🏢 Mumbai — AI-Driven Apartment Valuation", key="case_btn_mumbai"
            ):
                st.session_state.selected_case = "mumbai"
                st.rerun()

        with col2:
            st.image(
                "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80"
            )
            st.caption(
                "Forecasting property trends and demand with deep learning time-series models."
            )
            if st.button(
                "📊 Bengaluru — Predictive Market Insights",
                key="case_btn_bengaluru",
            ):
                st.session_state.selected_case = "bengaluru"
                st.rerun()

        with col3:
            st.image(
                "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=80"
            )
            st.caption(
                "AI-powered ranking engine for better investment decisions and faster deals."
            )
            if st.button(
                "🏙️ Delhi NCR — Smart Property Comparison",
                key="case_btn_delhi",
            ):
                st.session_state.selected_case = "delhi"
                st.rerun()

    # ---------------- DETAILED VIEWS ----------------
    else:
        if selected_case == "mumbai":
            st.markdown(
                """
            <div class='detail-box'>
                <h2 style='margin-top:0;'>🏢 AI-Driven Apartment Valuation — Mumbai, India</h2>
                <p>Mumbai's real estate market is fast, fragmented, and highly price-sensitive.<br>
                SmartBricks’ <b>AI-powered valuation system</b> automated what used to take <b>weeks</b> into seconds — ensuring fair, data-backed pricing.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>📊 10,000+ apartments analyzed using Random Forest & XGBoost</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>⚙️ Achieved R² = 0.94 | MAE = ₹3.1 lakhs</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>💡 Reduced manual appraisal time by 90%</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>🏦 Adopted by 5 major property lenders for loan risk assessment</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>📈 Helped standardize price variance across suburbs</div>",
                unsafe_allow_html=True,
            )

        elif selected_case == "bengaluru":
            st.markdown(
                """
            <div class='detail-box'>
                <h2 style='margin-top:0;'>📊 Predictive Market Insights — Bengaluru, India</h2>
                <p>Bengaluru’s housing demand mirrors its booming tech industry.<br>
                Using <b>LSTM-based time series models</b>, StreetBase delivers live forecasts of housing prices and investment growth corridors.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>🧠 LSTM + Prophet ensemble model for 7 years of transaction data</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>🔍 Incorporated IT job data, metro expansions, and infra growth</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>🚀 93% forecast accuracy — helping developers plan smarter</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>💬 Realtors close deals 25% faster using AI-driven dashboards</div>",
                unsafe_allow_html=True,
            )

        elif selected_case == "delhi":
            st.markdown(
                """
            <div class='detail-box'>
                <h2 style='margin-top:0;'>🏙️ Smart Property Comparison Tool — Delhi NCR, India</h2>
                <p>Delhi NCR buyers face overwhelming property choices.<br>
                SmartBricks’ <b>AI recommendation engine</b> ranks properties based on ROI, amenities, and proximity — saving users hours of research.</p>
            </div>
            """,
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>⚖️ Ranking model powered by cosine similarity and weighted ROI</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='metric'>📉 Reduced search and decision time by 60%</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>🏘️ Integrated by 4+ real estate startups</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<div class='impact'>🧩 Increased client conversion by 35% through better matching</div>",
                unsafe_allow_html=True,
            )

        # Back button
        st.markdown("<div class='btn-back'>", unsafe_allow_html=True)
        if st.button("⬅️ Back to All Case Studies", key="case_btn_back"):
            st.session_state.selected_case = None
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CHATBOT ----------------
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
