# main_app.py  (replace your current main file with this)
from components.chatbot_ui import chatbot_popup
import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd
from datetime import datetime, timedelta, timezone
from components.NavBar.navbar import navbar  # pyright: ignore[reportMissingImports]
import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os
from urllib.parse import urlparse

# Auto-refresh
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(page_title="News & Articles", layout="wide")

# Show navbar if you have it
navbar()

# ---------- Shared footer CSS ----------
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

# --- Configuration ---
API_KEY = "d4d290fde3d8464b8d689e5726ebfd45"
BASE_URL = "https://newsapi.org/v2/everything"
DEFAULT_QUERY = "real estate india"
MODEL_PATH = "news_classifier_model.joblib"

# Define the set of all possible categories
ALL_CATEGORIES = [
    "Apartments",
    "Villas",
    "Market Trends",
    "Investment Tips",
    "Regulations",
    "Industry News"  # Default/Catch-all
]
REAL_ESTATE_KEYWORDS = [
    "real estate", "property", "housing", "apartment", "apartments",
    "rental", "rent", "construction", "infrastructure",
    "home", "homes", "flat", "flats", "land", "plot", "plots",
    "builder", "builders", "realty", "estate", "market",
    "prices", "mortgage", "loan", "housing loan", "emi"
]

INDIA_KEYWORDS = [
    "india", "indian", "delhi", "mumbai",
    "bangalore", "hyderabad", "pune", "chennai",
]


def is_indian(text):
    t = text.lower()
    return any(k in t for k in INDIA_KEYWORDS)


def is_real_estate(text):
    t = text.lower()
    return any(k in t for k in REAL_ESTATE_KEYWORDS)


def is_relevant_article(article):
    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "")
    ).lower()

    return is_indian(text) and is_real_estate(text)


# --- ML Model Setup (Mock Training) ---
def train_and_save_model():
    """Trains a simple Naive Bayes classifier and saves it."""
    X_train = [
        "New high-rise apartment project launched in Mumbai", "flat for sale in Delhi", "condo prices rising",
        "Luxury villa sales hit record high in Goa", "independent house for rent", "mansion tax implications",
        "Indian real estate market poised for growth", "economic forecast for housing sector", "property price trend",
        "Top investment tips for first-time homebuyers", "maximizing ROI on rental property", "equity investment strategy",
        "RERA regulation changes announced", "new tax policy for property transactions", "land law updates",
        "General news about the real estate industry", "developer announces new project", "construction update"
    ]
    y_train = [
        "Apartments", "Apartments", "Apartments",
        "Villas", "Villas", "Villas",
        "Market Trends", "Market Trends", "Market Trends",
        "Investment Tips", "Investment Tips", "Investment Tips",
        "Regulations", "Regulations", "Regulations",
        "Industry News", "Industry News", "Industry News"
    ]

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    return model


# Load or train the model
if os.path.exists(MODEL_PATH):
    try:
        classifier = joblib.load(MODEL_PATH)
    except Exception:
        classifier = train_and_save_model()
else:
    classifier = train_and_save_model()


def ml_categorize_article(article_text):
    """Uses the trained ML model to predict the primary category."""
    predicted_category = classifier.predict([article_text])[0]
    return [predicted_category]


# -----------------------
# Helper utilities added
# -----------------------
def get_domain(url):
    try:
        net = urlparse(url).netloc.replace("www.", "")
        return net or "Unknown"
    except Exception:
        return "Unknown"


def human_time_from_iso(iso_string):
    """Convert ISO-8601 datetime to human-friendly relative time."""
    try:
        dt = None
        try:
            dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        except Exception:
            dt = datetime.strptime(iso_string[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

        now = datetime.now(tz=timezone.utc)
        diff = now - dt.astimezone(timezone.utc)
        s = diff.total_seconds()

        if s < 60:
            return "Just now"
        if s < 3600:
            return f"{int(s // 60)} minutes ago"
        if s < 86400:
            return f"{int(s // 3600)} hours ago"
        if s < 172800:
            return "Yesterday"
        return f"{int(s // 86400)} days ago"
    except Exception:
        return iso_string


def extract_tags(article):
    """Return small set of emoji-prefixed tags based on title/description."""
    text = ((article.get("title") or "") + " " + (article.get("description") or "")).lower()
    tags = []
    if any(k in text for k in ["price", "market", "prices", "trend"]):
        tags.append("📈 Market")
    if any(k in text for k in ["construction", "infrastructure", "build", "project"]):
        tags.append("🏗️ Construction")
    if any(k in text for k in ["rent", "rental", "lease", "tenant"]):
        tags.append("💸 Rental")
    if any(k in text for k in ["housing", "apartment", "flat", "homes"]):
        tags.append("🏙️ Housing")
    if any(k in text for k in ["loan", "emi", "mortgage", "tax", "finance", "investment", "roi"]):
        tags.append("💰 Finance")

    if not tags:
        tags.append("📰 News")
    return tags


# --- Data Fetching ---
def get_news_data(query: str, page_size: int = 50):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": page_size
    }

    articles_data = []

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        news = response.json().get("articles", [])

        for i, item in enumerate(news):
            published_at = item.get("publishedAt") or datetime.now(timezone.utc).isoformat()
            content_for_categorization = f"{item.get('title', '')} {item.get('description', '')}"

            articles_data.append({
                "id": i + 1,
                "title": item.get("title", "No Title"),
                "description": item.get("description", "No Description Available"),
                "publishedAt": published_at,
                "date": None,
                "author": item.get("author", "Unknown"),
                "image_url": item.get("urlToImage") or "https://via.placeholder.com/500x300.png?text=Real+Estate+News",
                "url": item.get("url", "#"),
                "content_text": content_for_categorization,
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "popularity_score": i + 1
            })

    except Exception as e:
        st.error(f"⚠️ Failed to fetch real-time articles: {e}. Showing demo content instead.")
        articles_data = [
            # fallback data...
        ]

    articles_data = [
        a for a in articles_data
        if is_relevant_article(a)
    ]

    return articles_data


def categorize_articles(articles):
    """Assigns articles to categories using the ML model and popularity."""
    categorized_news = {
        "Trending": [],
        "Most Read": [],
    }
    for cat in ALL_CATEGORIES:
        categorized_news[cat] = []

    for article in articles:
        ml_categories = ml_categorize_article(article["content_text"])
        article["categories"] = ml_categories

        if article.get("popularity_score", 9999) <= 10:
            categorized_news["Trending"].append(article)
        if article.get("popularity_score", 9999) <= 5:
            categorized_news["Most Read"].append(article)

        for cat in ml_categories:
            if cat in categorized_news:
                categorized_news[cat].append(article)
            else:
                categorized_news.setdefault(cat, []).append(article)

    for category in list(categorized_news.keys()):
        unique_articles = {a['id']: a for a in categorized_news[category]}.values()
        categorized_news[category] = list(unique_articles)

    categorized_news = {k: v for k, v in categorized_news.items() if v}
    return categorized_news


def render_article_card(article, is_featured=False):
    """Renders a single article card as pure HTML so background wraps everything."""
    card_class = "featured-article" if is_featured else "article-card"
    title_class = "featured-title" if is_featured else "article-title"

    st.markdown("""
        <style>
        .article-card, .featured-article {
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 20px;
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
        }
        .article-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .featured-article {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }

        .card-inner {
            display: flex;
            gap: 20px;
            align-items: flex-start;
        }

        .card-image {
            width: 32%;
            min-width: 220px;
        }
        .card-image img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 14px;
            object-fit: cover;
        }

        .card-content {
            flex: 1;
        }

        .article-title, .featured-title {
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .article-title {
            font-size: 18px;
        }
        .featured-title {
            font-size: 26px;
        }
        .article-title a,
        .featured-title a {
            color: inherit;
            text-decoration: none;
        }
        .article-title a:hover,
        .featured-title a:hover {
            text-decoration: underline;
        }

        .article-description-text {
            color: rgba(255, 255, 255, 0.94);
            font-size: 14px;
            line-height: 1.7;
            margin-bottom: 10px;
        }

        .article-meta {
            color: rgba(255,255,255,0.92);
            font-size: 13px;
        }

        .meta-tag-box {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 6px 10px;
            background: rgba(0, 0, 0, 0.16);
            border-radius: 999px;
            padding: 6px 14px;
            margin-bottom: 10px;
        }
        .meta-left {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 4px;
        }
        .meta-tags {
            display: flex;
            flex-wrap: wrap;
            margin-left: auto;
        }

        .tag-chip {
            display:inline-block;
            background: rgba(255,255,255,0.18);
            color: #ffffff;
            padding: 4px 10px;
            border-radius: 999px;
            margin-right:6px;
            font-size:11px;
            white-space: nowrap;
        }

        .read-link {
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            text-decoration: none;
        }
        .read-link:hover {
            text-decoration: underline;
        }
        </style>
    """, unsafe_allow_html=True)

    domain = get_domain(article.get("url", "#"))
    human_published = human_time_from_iso(
        article.get("publishedAt", datetime.now(timezone.utc).isoformat())
    )
    tags = extract_tags(article)
    author = article.get("author", "Unknown")
    image_url = (
        article.get("image_url")
        or article.get("urlToImage")
        or "https://via.placeholder.com/500x300.png?text=News"
    )

    desc = article.get("description", "") or ""
    if len(desc) > 220:
        desc = desc[:220].rstrip() + "…"

    meta_text = f"{domain} • {human_published} • By <strong>{author}</strong>"
    tag_html = "".join([f'<span class="tag-chip">{t}</span>' for t in tags])

    card_html = f"""
    <div class="{card_class}">
        <div class="card-inner">
            <div class="card-image">
                <img src="{image_url}" alt="article image" />
            </div>
            <div class="card-content">
                <div class="{title_class}">
                    <a href="{article.get("url", "#")}" target="_blank">
                        {article.get("title", "No Title")}
                    </a>
                </div>
                <div class="meta-tag-box">
                    <div class="meta-left">
                        <span class="article-meta">{meta_text}</span>
                    </div>
                    <div class="meta-tags">
                        {tag_html}
                    </div>
                </div>
                <div class="article-description-text">
                    {desc}
                </div>
                <a class="read-link" href="{article.get("url", "#")}" target="_blank">
                    🔗 Read full article →
                </a>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


# --- Page ----
def load_articles_page():
    """Load and display the articles page"""

    st_autorefresh(interval=60000, limit=None, key="real_estate_refresh")

    st.title("📰 Real Estate News & Articles")
    st.markdown("Stay updated with the latest trends, insights, and news in the real estate industry.")

    search_query = st.text_input(
        "Search all news articles...",
        placeholder="e.g., 'new apartment regulations' or 'villa investment'",
        key="main_search_box"
    )
    st.markdown("---")

    fetch_query = search_query.strip() if search_query.strip() else DEFAULT_QUERY

    articles_data = get_news_data(query=fetch_query, page_size=50)

    if search_query.strip():
        q = search_query.lower()
        filtered_local = [
            a for a in articles_data
            if q in (a.get("title") or "").lower() or q in (a.get("description") or "").lower()
        ]
        if filtered_local:
            articles_data = filtered_local

    categorized_news = categorize_articles(articles_data)

    if articles_data:
        featured = articles_data[0]
        st.subheader("🔥 Featured Article")
        render_article_card(featured, is_featured=True)

    for category, articles in categorized_news.items():
        if articles:
            st.header(f"🗞️ {category} ({len(articles)})")

            with st.expander(
                f"View {len(articles)} articles in {category}",
                expanded=category in ["Trending", "Most Read"]
            ):
                cols_per_row = 2
                for i in range(0, len(articles), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(articles):
                            article = articles[i + j]
                            with col:
                                render_article_card(article, is_featured=False)
            st.markdown("---")

    if not articles_data:
        st.info("📭 No articles found. Please try a different search query.")

    st.subheader("📧 Subscribe to Our Newsletter")
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input("Enter your email to get weekly real estate news", key="newsletter_email")
    with col2:
        if st.button("Subscribe", key="newsletter_subscribe"):
            if email:
                st.success(f"✅ Subscribed! You'll receive updates at {email}")
            else:
                st.error("Please enter a valid email address")


# Run the page function
if __name__ == "__main__":
    load_articles_page()

    chatbot_popup()  # 👈 this will render the StreetBase chat section here

    st.markdown("""
        <div class='footer'>
            © 2025 <b>StreetBase</b> | All Rights Reserved <br>
            Built with ❤️ using <a href='https://streamlit.io/' target='_blank'>Streamlit</a> and AI
        </div>
    """, unsafe_allow_html=True)
