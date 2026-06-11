# pages/home.py
import os
import sys
import streamlit as st
from test import render_testimonials
st.set_page_config(page_title="...", layout="wide")



# --- Add root path for imports ---
ROOT = os.path.dirname(os.path.dirname(__file__))  # Go up to project root
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# --- Import custom components ---
from components.NavBar.navbar import navbar
from components.Hero import (
    custom_css_injection,
    render_brand_header,
    render_hero_section,
    render_cta_banner
)
from components.features import load_feature_section
from components.simple_app import load_valuation_section  # ✅ NEW IMPORT

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StreetBase | Home",
    page_icon="🏠",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
    <style>
        * {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: #f7f9fb;
        }
        section {
            margin-top: 3rem;
            margin-bottom: 3rem;
        }
        h2, h3 {
            text-align: center;
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- INITIAL SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""


# ---------------- NAVBAR ----------------
navbar()  # your custom navbar (includes Login/Signup buttons)

# ---------------- HERO SECTION ----------------
custom_css_injection()
render_brand_header()
render_hero_section()
render_cta_banner()


# ---------------- VALUATION SECTION ----------------
st.markdown("<section>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#003366;'>💰 Property Valuation</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444;'>Try our AI-powered valuation engine below</p>", unsafe_allow_html=True)

load_valuation_section()  # ✅ NEW SECTION CALL


st.markdown("</section>", unsafe_allow_html=True)

# # ---------------- FOOTER ----------------
# st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- FEATURES SECTION ----------------
load_feature_section()
# render_testimonials()

# ---------------- TESTIMONIAL SLIDER ----------------

st.markdown("<br><br>", unsafe_allow_html=True)


