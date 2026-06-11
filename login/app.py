import streamlit as st
import pyrebase
import datetime
import requests
import os
import json
from urllib.parse import urlencode

# ----------------------------
# Config / Secrets
# ----------------------------
def get_secret(key, default=None):
    if key in st.secrets:
        return st.secrets[key]
    return os.environ.get(key, default)

GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = get_secret("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = get_secret("REDIRECT_URI", "http://localhost:8501")
FIREBASE_API_KEY = get_secret("FIREBASE_API_KEY")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Firebase Auth App", page_icon="🔥", layout="centered")

# ------------------------------
# Theme Toggle
# ------------------------------
# Note: The default theme is "Light". 
# You can set the default in session state.
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Dark" 

# This radio button doesn't actually change the theme, 
# as Streamlit's theme is set in the main config or settings.
# Keeping it as it was in your original code
# ------------------------------
# Firebase config
# ------------------------------
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

try:
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
except Exception as e:
    st.error(f"Failed to initialize Firebase: {e}")
    st.stop()

# ------------------------------
# Session State
# ------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "saved_token" not in st.session_state:
    st.session_state.saved_token = None

def save_token_to_cookie(token):
    # Streamlit doesn't have persistent cookies. 
    # This just saves to session state.
    st.session_state["saved_token"] = token

def load_token_from_cookie():
    # This just loads from session state.
    return st.session_state.get("saved_token", None)

# ------------------------------
# Auto-login using token
# ------------------------------
saved = load_token_from_cookie()
if saved:
    try:
        # Check if token is still valid
        data = auth.get_account_info(saved)
        u = data["users"][0]
        st.session_state.logged_in = True
        st.session_state.user = {"uid": u["localId"], "email": u["email"]}
    except Exception as e:
        # Token is invalid or expired
        st.session_state.saved_token = None
        st.session_state.logged_in = False
        st.session_state.user = None


# ------------------------------
# DB Helpers
# ------------------------------
def add_user_to_db(uid, email):
    try:
        db.child("users").child(uid).set({
            "email": email,
            "created_at": datetime.datetime.now().isoformat()
        })
    except Exception as e:
        st.error(f"Database Error: {e}")

def get_user_profile(uid):
    try:
        data = db.child("users").child(uid).get()
        return data.val() or {}
    except Exception as e:
        st.error(f"Database Error: {e}")
        return {}

# ------------------------------
# Google OAuth Endpoints
# ------------------------------
GOOGLE_AUTH_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
FIREBASE_IDP_ENDPOINT = (
    f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_API_KEY}"
)

def build_google_url():
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "consent"
    }
    return GOOGLE_AUTH_ENDPOINT + "?" + urlencode(params)

# Google OAuth handler
# Replace your existing handle_google_callback function with this one
# to see the specific error message from Google.

def handle_google_callback():
    params = st.query_params
    if "code" not in params:
        return
    
    code = params["code"] # In newer Streamlit, this is usually a string, not a list

    try:
        # STEP 1 → Exchange code for Google tokens
        data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code"
        }
        
        # Debug: Check if secrets are actually loaded
        if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
            st.error("Error: Google Client ID or Secret is missing. Check .streamlit/secrets.toml")
            st.stop()

        token_resp = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
        
        # --- NEW DEBUGGING SECTION ---
        if not token_resp.ok:
            # This will show you EXACTLY what is wrong (e.g., "redirect_uri_mismatch")
            st.error(f"Google API Error: {token_resp.text}")
            st.stop()
        # -----------------------------

        token_resp.raise_for_status()
        token_json = token_resp.json()
        id_token = token_json.get("id_token")

        if not id_token:
            st.error("Failed to get ID token from Google.")
            return

        # STEP 2 → Convert Google token → Firebase token
        payload = {
            "postBody": f"id_token={id_token}&providerId=google.com",
            "requestUri": REDIRECT_URI,
            "returnSecureToken": True
        }
        fb_resp = requests.post(FIREBASE_IDP_ENDPOINT, json=payload)
        fb_resp.raise_for_status()
        fb = fb_resp.json()

        st.session_state.logged_in = True
        st.session_state.user = {"uid": fb["localId"], "email": fb["email"]}
        save_token_to_cookie(fb["idToken"])
        
        # Add user to DB if they are new
        profile = get_user_profile(fb["localId"])
        if not profile:
            add_user_to_db(fb["localId"], fb["email"])

        # Clear query params and rerun to remove the 'code' from URL
        st.query_params.clear()
        st.rerun()

    except Exception as e:
        st.error(f"Google Sign-In Error: {e}")

# Check for callback *before* rendering login page
handle_google_callback()

# ------------------------------
# LOGIN PAGE
# ------------------------------
def login():
    st.subheader("Login to Your Account")
    
    email = st.text_input("📧 Email ID", key="email_login")
    password = st.text_input("🔒 Password", key="password_login", type="password")
    
    remember = st.checkbox("Remember me", key="remember_login")
    
    if st.button("Login", key="login_btn", type="primary"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.user = {"uid": user["localId"], "email": email}
            if remember:
                save_token_to_cookie(user["idToken"])
            st.rerun()
        except Exception as e:
            st.error("Invalid credentials. Please check your email and password.")

    st.divider()
    
    # Build Google URL and create link button
    try:
        google_url = build_google_url()
        st.link_button("Continue with Google", google_url)
    except Exception as e:
        st.error(f"Google Auth not configured: {e}")


# ------------------------------
# SIGNUP PAGE
# ------------------------------
def signup():
    st.subheader("Create a New Account")

    email = st.text_input("📧 Email ID", key="email_signup")
    password = st.text_input("🔒 Create Password", key="password_signup", type="password")
    confirm = st.text_input("🔒 Confirm Password", key="confirm_signup", type="password")

    if st.button("Create Account", key="create_btn", type="primary"):
        if password != confirm:
            st.error("Passwords do not match")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters long")
        else:
            try:
                user = auth.create_user_with_email_and_password(email, password)
                # Add user to our realtime database
                add_user_to_db(user["localId"], email)
                st.success("Account created successfully! Please login.")
            except Exception as e:
                # Handle known Firebase errors
                if "EMAIL_EXISTS" in str(e):
                    st.error("This email address is already in use.")
                else:
                    st.error(f"An error occurred: {e}")

# ------------------------------
# PROFILE PAGE
# ------------------------------
def profile_page():
    st.subheader(f"Welcome, {st.session_state.user['email']}!")
    
    st.markdown("---")
    
    try:
        data = get_user_profile(st.session_state.user["uid"])
        st.write(f"**Email:** {st.session_state.user['email']}")
        
        created_at_str = data.get("created_at", "Unknown")
        if created_at_str != "Unknown":
            try:
                # Parse ISO format and make it friendly
                created_at_dt = datetime.datetime.fromisoformat(created_at_str)
                created_at_friendly = created_at_dt.strftime("%B %d, %Y")
                st.write(f"**Joined:** {created_at_friendly}")
            except ValueError:
                st.write(f"**Joined:** {created_at_str}") # Fallback
        else:
            st.write(f"**Joined:** {created_at_str}")

    except Exception as e:
        st.error(f"Could not load profile: {e}")

    st.markdown("---")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.saved_token = None
        st.rerun()

# ------------------------------
# MAIN UI
# ------------------------------

if st.session_state.logged_in:
    # If logged in, show profile in sidebar and main page
    st.sidebar.title("User Profile")
    with st.sidebar:
        profile_page()
    
    # You can put your main app content here
    st.title("Main Application")
    st.write("You are logged in! This is your main app area.")
    
else:
    # If not logged in, show Login/Signup in sidebar
    st.sidebar.title("Welcome")
    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        login()
    else:
        signup()