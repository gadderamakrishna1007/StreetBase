import streamlit as st
import base64
import os

def _embed_logo_base64(logo_path: str) -> str:
    """Convert logo to Base64 for inline embedding"""
    if not os.path.exists(logo_path):
        return ""
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def navbar():
    logo_path = os.path.join(os.path.dirname(__file__), "logo3.png")
    logo_b64 = _embed_logo_base64(logo_path)

    if logo_b64:
        logo_html = f"<img src='data:image/png;base64,{logo_b64}' class='logo' />"
    else:
        logo_html = "<div style='width:60px;height:60px;background:#fff;'></div>"

    # ---------- AUTH / LOGIN BUTTON ----------
    if st.session_state.get("logged_in", False):
        username = st.session_state.get("username", "")
        auth_html = f"""
        <div class='profile-wrap' id='profileWrap'>
            <button class='profile-btn' id='profileBtn'>👤 {username}</button>
            <div class='dropdown-content' id='dropdownMenu'>
                <a href='?page=Signin&logout=true' id='logoutBtn' target='_self'>Sign Out</a>
            </div>
        </div>
        """.strip()
    else:
        auth_html = "<a href='?page=Signin' class='login-btn' target='_self'>Login / Sign Up</a>"

    # ---------- NAVBAR HTML ----------
    html = f"""
    <style>
        /* NAVBAR STYLING */
        .smartbricks-nav {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background: #003366;
            color: #fff;
            z-index: 9999;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        .smartbricks-nav .container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
        }}
        .nav-left {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .logo {{
            width: 60px;
            height: 60px;
            border-radius: 7px;
        }}
        .brand {{
            font-size: 1.6rem;
            font-weight: 700;
            color: #FF6600;
        }}
        .nav-options {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        .nav-options a {{
            color: #fff;
            text-decoration: none;
            font-weight: 600;
        }}
        .nav-options a:hover {{
            color: #FF6600;
        }}
        .login-btn {{
            background: #FF6600;
            color: #fff;
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: 600;
            text-decoration: none;
        }}
        .login-btn:hover {{
            background: #fff;
            color: #FF6600;
        }}
        .profile-wrap {{
            position: relative;
        }}
        .profile-btn {{
            background: #fff;
            border: 2px solid #FF6600;
            color: #FF6600;
            cursor: pointer;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .profile-btn:hover {{
            background: #FF6600;
            color: #fff;
        }}
        .dropdown-content {{
            display: none;
            position: absolute;
            right: 0;
            top: 46px;
            background: #fff;
            color: #003366;
            min-width: 150px;
            border-radius: 6px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        }}
        .dropdown-content a {{
            display: block;
            padding: 8px 12px;
            color: #003366;
            text-decoration: none;
            font-weight: 600;
        }}
        .dropdown-content a:hover {{
            background: #F8F8F8;
        }}
        .profile-wrap.show .dropdown-content {{
            display: block;
        }}

        /* Push main content down so it isn't hidden behind fixed navbar */
        .block-container {{
            padding-top: 100px !important;
        }}
    </style>

    <div class="smartbricks-nav">
      <div class="container">
        <div class="nav-left">
          {logo_html}
          <div class="brand">StreetBase</div>
        </div>
        <div class="nav-options">
            <a href="?page=home" target="_self">Home</a>
            <a href="?page=services" target="_self">Services</a>
            <a href="?page=case_studies" target="_self">Case Studies</a>
            <a href="?page=favourites" target="_self">Favourites</a>
            <a href="?page=emi_calc" target="_self">EMI_Calc</a>
            <a href="?page=news" target="_self">News</a>
            <a href="?page=AboutUs" target="_self">About Us</a>
            {auth_html}
        </div>
      </div>
    </div>

    <script>
        const profileBtn = document.getElementById('profileBtn');
        const profileWrap = document.getElementById('profileWrap');
        if (profileBtn) {{
            profileBtn.addEventListener('click', (e) => {{
                e.stopPropagation();
                profileWrap.classList.toggle('show');
            }});
        }}
        document.addEventListener('click', (e) => {{
            if (profileWrap && !profileWrap.contains(e.target)) {{
                profileWrap.classList.remove('show');
            }}
        }});
    </script>
    """

    st.markdown(html, unsafe_allow_html=True)
