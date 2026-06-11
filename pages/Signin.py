# Signin.py
import streamlit as st
import pyrebase
import datetime
import requests
from urllib.parse import urlencode
import time
import re

def is_valid_email(email):
    """Validate email using regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


# ----------------------------
# Config / Secrets
# ----------------------------
def get_secret(key, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return default

GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_secret("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = get_secret("REDIRECT_URI", "http://localhost:8501")
FIREBASE_API_KEY = get_secret("FIREBASE_API_KEY")

firebaseConfig = {
    "apiKey": FIREBASE_API_KEY,
    "authDomain": "login-10cee.firebaseapp.com",
    "databaseURL": "https://login-10cee-default-rtdb.firebaseio.com",
    "projectId": "login-10cee",
    "storageBucket": "login-10cee.appspot.com",
    "messagingSenderId": "332483422044",
    "appId": "1:332483422044:web:22ecce612880ab53a54399",
    "measurementId": "G-044W8QJB1Q"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# ----------------------------
# Session State Initialization
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "saved_token" not in st.session_state:
    st.session_state.saved_token = None

# ----------------------------
# Helper Functions
# ----------------------------
def save_token(token):
    st.session_state.saved_token = token

def load_token():
    return st.session_state.get("saved_token", None)

def get_token():
    return st.session_state.get("saved_token", None)


def add_user_to_db(uid, email):
    try:
        db.child("users").child(uid).set({
            "email": email,
            "created_at": datetime.datetime.now().isoformat()
        })
    except:
        pass

def get_user_profile(uid):
    try:
        data = db.child("users").child(uid).get()
        return data.val() or {}
    except:
        return {}

def build_google_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "consent"
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

def handle_google_callback():
    params = st.query_params
    if "code" not in params:
        return
    code_param = params["code"]
    code = code_param[0] if isinstance(code_param, list) else code_param
    try:
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        token_resp = requests.post("https://oauth2.googleapis.com/token", data=data)
        token_resp.raise_for_status()
        id_token = token_resp.json().get("id_token")
        payload = {
            "postBody": f"id_token={id_token}&providerId=google.com",
            "requestUri": REDIRECT_URI,
            "returnSecureToken": True
        }
        fb_resp = requests.post(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}",
            json=payload
        )
        fb_resp.raise_for_status()
        fb = fb_resp.json()
        st.session_state.logged_in = True
        st.session_state.user = {"uid": fb["localId"], "email": fb["email"]}
        save_token(fb["idToken"])
        if not get_user_profile(fb["localId"]):
            add_user_to_db(fb["localId"], fb["email"])
        st.query_params.clear()
        st.rerun()
    except Exception as e:
        st.error(f"Google Sign-In failed: {e}")
        st.query_params.clear()

# ----------------------------
# Error Mapping for Firebase
# ----------------------------
FIREBASE_ERRORS = {
    "EMAIL_EXISTS": "This email is already registered.",
    "OPERATION_NOT_ALLOWED": "Password sign-in is disabled.",
    "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Try again later.",
    "EMAIL_NOT_FOUND": "Email not found. Please sign up.",
    "INVALID_PASSWORD": "Incorrect password. Try again.",
    "USER_DISABLED": "This account has been disabled by an administrator."
}

def map_firebase_error(error_str):
    for code, msg in FIREBASE_ERRORS.items():
        if code in error_str:
            return msg
    return "An unexpected error occurred. Please try again."

# ----------------------------
# Main Page Function
# ----------------------------
def load_signin_page():
    st.set_page_config(page_title="Login | Firebase Auth", layout="centered")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user" not in st.session_state:
        st.session_state.user = None

    handle_google_callback()  # Check for Google OAuth callback

    # ---------- CSS ----------
    st.markdown("""
        <style>
            header, footer {visibility: hidden;}
            div.block-container {padding-top: 2rem;}
            .login-title {text-align:center;color:#FF6600;font-size:1.6rem;font-weight:bold;margin-bottom:1rem;}
            .stButton>button {background-color:#FF6600;color:white;border-radius:10px;font-weight:600;width:100%;height:2.5rem;}
        </style>
    """, unsafe_allow_html=True)

    # ---------- LOGIN / REGISTER ----------
    if not st.session_state.logged_in:
        tabs = st.tabs(["🔐 Login", "🆕 Register"])

        # -------- LOGIN TAB --------
        with tabs[0]:
            st.markdown("<div class='login-title'>User Login</div>", unsafe_allow_html=True)
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")

            if st.button("Login"):
                if not email or not password:
                    st.warning("Please enter both email and password.")
                else:
                    try:
                        user = auth.sign_in_with_email_and_password(email, password)
                        st.session_state.logged_in = True
                        st.session_state.user = {"uid": user["localId"], "email": email}
                        save_token(user["idToken"])
                        st.success(f"✅ Logged in successfully! Welcome {email}")
                        st.rerun()
                    except Exception as e:
                        st.error(map_firebase_error(str(e)))

            st.markdown("### 🔐 Or login with Google")
            st.link_button("Continue with Google", build_google_url())

        # -------- REGISTER TAB --------
        with tabs[1]:
            st.markdown("<div class='login-title'>Create Account</div>", unsafe_allow_html=True)
            new_email = st.text_input("Email", key="reg_email")
            new_pass = st.text_input("Password", type="password", key="reg_pass")
            confirm_pass = st.text_input("Confirm Password", type="password", key="reg_confirm")

            if st.button("Register"):
                if not new_email or not new_pass or not confirm_pass:
                    st.warning("All fields are required.")
                elif not is_valid_email(new_email):
                    st.error("❌ Please enter a valid email address.")
                elif new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        user = auth.create_user_with_email_and_password(new_email, new_pass)
                        add_user_to_db(user["localId"], new_email)
                        st.success("✅ Account created successfully! You can now log in.")
                    except Exception as e:
                        st.error(map_firebase_error(str(e)))

    # ---------- DASHBOARD / LOGOUT ----------
    else:
        st.success(f"✅ Logged in as: {st.session_state.user['email']}")
        st.write("Welcome to your **Dashboard!** Here you can view personalized content.")
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.saved_token = None
            st.success("You have been logged out.")
            st.rerun()

# ----------------------------
# Run directly
# ----------------------------
if __name__ == "__main__":
    load_signin_page()
