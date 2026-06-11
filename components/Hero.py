from components.simple_app import load_valuation_section
import streamlit.components.v1 as components  # add this at top
import streamlit as st
from streamlit_lottie import st_lottie # Keeping Lottie in case we want to use it elsewhere, though not in this specific reference image
import requests # Also keeping for Lottie if needed
import os


# --- Page Configuration ---
st.set_page_config(
    page_title="StreetBase - AI Real Estate Valuation",
    page_icon="🏠",
    layout="wide" # Use wide layout for more space
    # initial_sidebar_state="expanded" # Optional: if you had a sidebar
)

def custom_css_injection():
    custom_css = """
    <style>
        /* --- Import Google Font 'Inter' --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            color: #333333;
            background-color: #F8F9FA;
        }

        /* 🔹 Reduce default Streamlit top padding */
        .main .block-container {
            padding-top: 0.5rem !important;  /* was ~4rem by default */
        }

        /* Main container for the hero section */
        .main-hero-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 3rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
        }

        .quick-insights-box {
            background-color: #EBF2FF;
            border-radius: 12px;
            padding: 2rem;
            margin-left: 2rem;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        h1 {
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            color: #002D62 !important;
            line-height: 1.1;
            margin-bottom: 0.5rem;
        }

        h2 {
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #0047AB !important;
            margin-bottom: 1.5rem !important;
        }

        .cta-banner h2 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
            text-align: center;
            margin-bottom: 1rem !important;
        }

        p, .stMarkdown, .stText {
            font-size: 1.05rem;
            line-height: 1.6;
            color: #4A4A4A;
        }

        ul li {
            margin-bottom: 0.5rem;
            font-size: 1.05rem;
            color: #4A4A4A;
        }
        .insights-list li {
            list-style: none;
            margin-bottom: 0.7rem;
            font-size: 1.05rem;
            color: #333333;
        }
        .insights-list li::before {
            content: "✅";
            margin-right: 0.8em;
        }

        /* --- Button Styling --- */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 12px 25px !important;
            font-size: 1rem !important;
            transition: all 0.2s ease-in-out !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .stButton > button[kind="primary"] {
            background-color: #007BFF !important;
            color: white !important;
            margin-right: 15px;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #0056b3 !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            transform: translateY(-2px);
        }

        .stButton > button[kind="secondary"] {
            background-color: #28A745 !important;
            color: white !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background-color: white !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            transform: translateY(-2px);
        }

        /* --- Logo and Title at Top Left --- */
        .logo-container {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 1.5rem;
            /* 🔹 Remove big top padding here */
            padding: 0.25rem 0 1.5rem 0;  /* small top, keep some bottom */
        }

        .logo-img {
            height: 40px;
        }

        .brand-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #002D62;
            margin: 0;
        }

        /* --- Bottom CTA Banner --- */
        .cta-banner {
            background-color: #007BFF;
            color: white;
            border-radius: 12px;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-top: 3rem;
        }
        .cta-banner .emoji {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }
        .cta-banner p {
            color: #EBF2FF;
            max-width: 800px;
            margin: 0 auto;
            font-size: 1.1rem;
        }
        
                /* ACTIVE button style after click */
        .clicked-btn {
            background-color: white !important;
            color: black !important;
            border: 2px solid #007BFF !important;
        }


        /* Remove default Streamlit header/footer (no gap) */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {display: none;}  /* 🔹 use display:none instead of visibility */
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# --- Components for Member 2 ---

# Function for the logo and brand title
# Function for the logo and brand title using a local file
def render_brand_header():
    from pathlib import Path

    # Placeholder path — you can update this with your actual local logo path
    logo_path = os.path.join(os.path.dirname(__file__), "NavBar", "logo3.png") # <-- Replace with your actual file path

    st.markdown(
        """
        <div class="logo-container">
        """,
        unsafe_allow_html=True
    )

    # Display local logo
    st.image(str(logo_path), width=40)  # Width matches previous styling

    # Brand title
    st.markdown(
        """
            <span class="brand-title">StreetBase</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_hero_section():
    # Anchor that our CSS targets; the NEXT horizontal block (columns) becomes the card
    st.markdown('<div id="hero-card-anchor"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1.5], gap="large")

    with col_left:
        st.title("AI-Powered Real Estate Valuation")
        st.write("""
        Predicting house prices is complex, influenced by location, size, rooms, and economic conditions. 
        StreetBase uses *supervised machine learning* to accurately predict property values 
        based on historical data, providing valuable insights into housing price estimation.
        """)
        st.markdown("""
        <ul>
            <li>✨ <b>Real-time AI valuation</b> using regression models</li>
            <li>🚀 Built on <b>supervised ML</b> (Scikit-learn + Pandas)</li>
            <li>💡 Insights into <b>key factors</b> influencing property prices</li>
            <li>📊 Trained on comprehensive <b>Indian real estate data</b></li>
        </ul>
        """, unsafe_allow_html=True)

        st.write("")
        button_col1, button_col2, _ = st.columns([0.8, 0.8, 2])
        # with button_col1:

        #     # Create session state flags on first load
        #     if "valuation_clicked" not in st.session_state:
        #         st.session_state.valuation_clicked = False

        #     if "scroll_to_model" not in st.session_state:
        #         st.session_state.scroll_to_model = False

        #     # ---------- Dynamic CSS for button ----------
        #     button_css = f"""
        #         <style>
        #             .custom-ai-btn > button {{
        #                 border-radius: 8px !important;
        #                 font-weight: 600 !important;
        #                 padding: 12px 25px !important;
        #                 font-size: 1rem !important;
        #                 transition: all 0.2s ease-in-out !important;
        #                 border: none !important;
        #                 box-shadow: 0 4px 8px rgba(0,0,0,0.1);

        #                 /* Normal vs Clicked style */
        #                 background-color: {"white" if st.session_state.valuation_clicked else "#007BFF"} !important;
        #                 color: {"black" if st.session_state.valuation_clicked else "white"} !important;
        #             }}

        #             .custom-ai-btn > button:hover {{
        #                 transform: translateY(-2px);
        #                 box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        #                 background-color: {"#f2f2f2" if st.session_state.valuation_clicked else "#0056b3"} !important;
        #                 color: {"black" if st.session_state.valuation_clicked else "white"} !important;
        #             }}
        #         </style>
        #     """
        #     st.markdown(button_css, unsafe_allow_html=True)

        #     # ---------- Button Wrapper ----------
        #     st.markdown('<div class="custom-ai-btn">', unsafe_allow_html=True)

        #     # ---------- Actual Button ----------
        #     if st.button("Try AI Valuation", key="try_ai_btn"):
        #         st.session_state.valuation_clicked = True
        #         st.session_state.scroll_to_model = True  # trigger scroll

        #     st.markdown('</div>', unsafe_allow_html=True)


        # with button_col2:
        #     if st.button("View Insights", type="secondary"):
        #         st.success("Displaying market insights!")

    with col_right:
        st.markdown(
            """
            <div class="quick-insights-box">
                <h2>Quick Insights</h2>
                <ul class="insights-list">
                    <li>Fast & Accurate AI predictions</li>
                    <li>Beautiful UI built with Streamlit</li>
                    <li>Multiple ML algorithms evaluated</li>
                    <li>Comprehensive datasets from major Indian cities</li>
                    <li>Feature analysis for price factors</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)




def render_cta_banner():
    st.markdown(
        """
        <div class="cta-banner">
            <span class="emoji">🚀</span>
            <h2>Ready to Evaluate Your Property?</h2>
            <p>
                Get instant AI-powered property valuation based on location, size, amenities, and market trends.
                Our machine learning model analyzes multiple factors to provide accurate price estimates.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Main App Execution ---
# --- Main App Execution ---
if __name__ == "__main__":
    custom_css_injection() # Apply our custom styles first

    render_brand_header() # Logo and SmartBricks title
    render_hero_section() # Main hero content and quick insights
    # 🔽 The section we want to scroll to
    load_valuation_section()
    render_cta_banner()   # Bottom call-to-action banner
    
    # Placeholder for other members' work (will also adopt the custom styles)
    st.markdown("<br><br>", unsafe_allow_html=True) # Add some vertical space
    
    if st.session_state.get("scroll_to_model", False):
        components.html(
            """
            <script>
            // Work both when inside a component iframe or directly in the main document
            const doc = window.parent ? window.parent.document : document;
            const target = doc.getElementById("ai_model_section");
            if (target) {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
            </script>
            """,
            height=10,   
        )
        st.session_state.scroll_to_model = False
