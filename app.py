import os

# 👉 Set these BEFORE importing anything else that might use OpenMP (torch, transformers, etc.)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import streamlit as st
# st.set_option('server.runOnSave', True)

import sys

# ✅ Ensure root paths work properly
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "components"))
sys.path.append(os.path.join(project_root, "pages"))
sys.path.append(os.path.join(project_root, "backend")) 

# ✅ Import navbar (only once)
from components.NavBar.navbar import navbar
from components.chatbot_ui import chatbot_popup  # 🟢 add this

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="StreetBase", page_icon="🏠", layout="wide")

# ---------------- RENDER NAVBAR ----------------
# Hide the default Streamlit deploy menu, header, and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

navbar()

# ---------------- LOGOUT HANDLER ----------------
# ---------------- LOGOUT HANDLER ----------------
query_params = st.query_params
if "logout" in query_params and query_params["logout"] == "true":
    st.session_state.logged_in = False
    st.session_state.username = ""
    # Clear logout param and redirect to home
    st.query_params.clear()
    st.query_params["page"] = "home"
    st.rerun()



# ---------------- PAGE ROUTING ----------------
page = st.query_params.get("page", "home")

try:
    if page == "home":
        from components.Hero import (
            custom_css_injection,
            render_brand_header,
            render_hero_section,
            render_cta_banner,
        )
        from components.simple_app import load_valuation_section
        from components.features import load_feature_section

        custom_css_injection()
        render_brand_header()
        render_hero_section()
        render_cta_banner()
        load_valuation_section()
        load_feature_section()

    elif page == "services":
        import pages.services as services
        services.load_services_page()

    elif page == "case_studies":
        import pages.case_studies as case_studies
        case_studies.load_case_studies_page()

    elif page == "news":
        from pages.news import load_articles_page
        load_articles_page()

    elif page == "AboutUs":
        import pages.AboutUs as about_us
        about_us.load_about_us_page()

    elif page == "Signin":
        import pages.Signin as signin
        signin.load_signin_page()
    elif page == "emi_calc":
        import pages.emi_calc as emi
        emi.render_emi_calculator()

    elif page == "favourites":
        import pages.favourites as fav
        fav.render_favourites_page()

    else:
        st.error("404 - Page not found 😢")

except Exception as e:
    st.error(f"Error loading page: {e}")

