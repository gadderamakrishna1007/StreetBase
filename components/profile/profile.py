import streamlit as st

st.set_page_config(page_title="Profile", layout="wide")

# ---------- SAMPLE SAFEGUARD ----------
# If user not in session_state, you can handle gracefully
if "user" not in st.session_state:
    st.session_state.user = {
        "name": "Guest User",
        "email": "guest@example.com",
        "bio": "Welcome to StreetBase! Update your profile to personalize your experience.",
        "interests": ["Real Estate", "Data Science", "Sustainability"],
        "stats": {
            "valuations": 0,
            "saved_properties": 0,
            "recommendations": 0,
        },
        "preferences": {
            "city": "N/A",
            "budget": "N/A",
            "property_type": "N/A",
        },
    }

user = st.session_state.user

# ---------- CSS (aligned with About Us styling) ----------
st.markdown(
    """
    <style>
    #MainMenu, header {visibility: hidden;}

    body, .block-container {
        background-color: #FFFDF2;
        color: #2b2b2b;
        font-family: 'Segoe UI', sans-serif;
        max-width: 95%;
        margin: auto;
    }

    .profile-hero {
        margin-top: 1.5rem;
        margin-bottom: 2.0rem;
        padding: 1.8rem 1.8rem;
        border-radius: 24px;
        background: radial-gradient(circle at top left, #F5B895 0, #FFFDF2 45%, #EDE9D5 100%);
        box-shadow: 0 10px 28px rgba(0,0,0,0.08);
        border: 1px solid rgba(226,114,91,0.24);
        display: flex;
        gap: 1.8rem;
        align-items: center;
    }

    .profile-avatar {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        overflow: hidden;
        border: 3px solid #004D00;
        background: #FFF;
        flex-shrink: 0;
    }

    .profile-main {
        flex: 1;
    }

    .profile-name {
        font-size: 1.8rem;
        font-weight: 800;
        color: #004D00;
        margin-bottom: 0.25rem;
    }

    .profile-email {
        font-size: 0.95rem;
        color: #555;
        margin-bottom: 0.6rem;
    }

    .profile-bio {
        font-size: 0.95rem;
        color: #333;
        margin-bottom: 0.8rem;
    }

    .interest-pill {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        border: 1px solid rgba(0,0,0,0.06);
        background: rgba(255,255,255,0.9);
        margin: 0.15rem 0.3rem 0.15rem 0;
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #004D00;
        margin-top: 1.5rem;
        margin-bottom: 0.4rem;
    }

    .section-subtitle {
        font-size: 0.92rem;
        color: #555;
        margin-bottom: 0.8rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        padding: 1.0rem 1.1rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-top: 4px solid #E2725B;
        margin-bottom: 0.7rem;
    }
    .metric-value {
        font-size: 1.35rem;
        font-weight: 800;
        color: #004D00;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #555;
    }

    .info-card {
        background: #FFFFFF;
        border-radius: 18px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
        border-left: 5px solid #F5B895;
        margin-bottom: 1rem;
    }
    .info-card h4 {
        margin: 0 0 0.4rem 0;
        font-size: 1.05rem;
        color: #004D00;
    }
    .info-card p {
        margin: 0.1rem 0;
        font-size: 0.92rem;
        color: #444;
    }

    /* Edit form styling */
    div[data-testid="stForm"] {
        background-color: #FFFDF2;
        padding: 24px 26px;
        border-radius: 18px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        max-width: 800px;
        margin: 0 auto 1.5rem auto;
        border: 1px solid #E2E2E2;
    }
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border: 2px solid #004D00 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-size: 0.95rem !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .stButton button {
        background-color: #F5B895 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 8px 20px !important;
        border: none !important;
    }
    .stButton button:hover {
        background-color: #E2725B !important;
        transform: scale(1.03);
    }

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

# ---------- HERO SECTION ----------
hero_col1, hero_col2 = st.columns([1.4, 2.6])
with hero_col1:
    st.markdown(
        """
        <div class="profile-hero">
            <div class="profile-avatar">
                <img src="https://i.imgur.com/6VBx3io.png" style="width:100%; height:100%; object-fit:cover;" />
            </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with hero_col2:
    st.markdown(
        f"""
        <div class="profile-hero">
            <div class="profile-main">
                <div class="profile-name">{user["name"]}</div>
                <div class="profile-email">{user["email"]}</div>
                <div class="profile-bio">{user["bio"]}</div>
                <div>
        """,
        unsafe_allow_html=True,
    )

    # interest pills inside hero card
    if user.get("interests"):
        pills_html = "".join(
            f"<span class='interest-pill'>{i}</span>" for i in user["interests"]
        )
        st.markdown(pills_html, unsafe_allow_html=True)

    st.markdown("</div></div></div>", unsafe_allow_html=True)

st.divider()

# ---------- INSIGHTS + PREFERENCES SECTIONS ----------
left_col, right_col = st.columns([1.6, 1.4], gap="large")

with left_col:
    st.markdown("<div class='section-title'>📊 Activity Snapshot</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>A quick overview of how you use StreetBase.</div>",
        unsafe_allow_html=True,
    )

    mcol1, mcol2, mcol3 = st.columns(3)
    stats = user.get("stats", {})

    with mcol1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get("valuations", 0)}</div>
                <div class="metric-label">Valuations</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mcol2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get("saved_properties", 0)}</div>
                <div class="metric-label">Saved Properties</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with mcol3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{stats.get("recommendations", 0)}</div>
                <div class="metric-label">Recommendations Viewed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-title'>🎯 Interests</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>What you care about helps us personalize your experience.</div>",
        unsafe_allow_html=True,
    )
    if user.get("interests"):
        pills_html_block = "".join(
            f"<span class='interest-pill'>{i}</span>" for i in user["interests"]
        )
        st.markdown(pills_html_block, unsafe_allow_html=True)
    else:
        st.info("Add a few interests below to see them here.")

with right_col:
    st.markdown("<div class='section-title'>🏡 Preferences</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='section-subtitle'>Your default search and evaluation context.</div>",
        unsafe_allow_html=True,
    )
    prefs = user.get("preferences", {})

    st.markdown(
        f"""
        <div class="info-card">
            <h4>Property Preferences</h4>
            <p><b>Preferred City:</b> {prefs.get('city', 'N/A')}</p>
            <p><b>Budget:</b> {prefs.get('budget', 'N/A')}</p>
            <p><b>Property Type:</b> {prefs.get('property_type', 'N/A')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# ---------- EDIT PROFILE FORM ----------
st.markdown("<div class='section-title'>✏️ Edit Profile</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='section-subtitle'>Update your basic details and what you’re interested in.</div>",
    unsafe_allow_html=True,
)

with st.form("edit_profile_form"):
    name = st.text_input("Name", user["name"])
    bio = st.text_area("Bio", user["bio"])
    interests_str = ", ".join(user["interests"]) if user.get("interests") else ""
    interests_input = st.text_area(
        "Interests (comma separated)",
        interests_str,
        placeholder="Example: Real estate, Data science, Sustainability",
    )

    submitted = st.form_submit_button("Save Changes")

    if submitted:
        st.session_state.user["name"] = name
        st.session_state.user["bio"] = bio
        st.session_state.user["interests"] = [
            x.strip() for x in interests_input.split(",") if x.strip()
        ]
        st.success("✅ Profile updated successfully!")

# ---------- FOOTER ----------
st.markdown(
    """
    <div class='footer'>
        © 2025 <b>StreetBase</b> | All Rights Reserved <br>
        Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
    </div>
    """,
    unsafe_allow_html=True,
)
