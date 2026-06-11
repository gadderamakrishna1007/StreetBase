import os
from openai import OpenAI
from sentence_transformers import SentenceTransformer, util
from PyPDF2 import PdfReader
import torch
import re
from dotenv import load_dotenv
load_dotenv()

# Disable parallelism warnings
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"   # 👈 add this line
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ✅ Use environment variable for API key (DON'T hardcode)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),  # set this in your system/.env
)

# Load sentence-transformer model once
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# -------- PDF Handling Utilities --------
def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract cleaned text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        t = page.extract_text()
        if t:
            # Normalize whitespace
            t = re.sub(r"\s+", " ", t)
            text += t.strip() + "\n"
    return text


def chunk_text(text: str, words_per_chunk: int = 800):
    """Split long text into word-based chunks."""
    words = text.split()
    return [
        " ".join(words[i : i + words_per_chunk])
        for i in range(0, len(words), words_per_chunk)
    ]


# -------- Bot Initialization --------
def init_bot(pdf_path: str | None = None):
    """
    Initialize the bot:
    - Locate StreetBase_KB.pdf in project root (by default)
    - Extract text
    - Create chunks + embeddings

    This should be called ONCE per session (handled in chatbot_ui).
    """

    # If no explicit path, build path to StreetBase_KB.pdf in project root
    if pdf_path is None:
        # components/StreetBase_chatbot.py -> go up one level to project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pdf_path = os.path.join(project_root, "StreetBase_KB.pdf")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

    print(f"📄 Loading PDF from: {pdf_path}")
    pdf_text = extract_text_from_pdf(pdf_path)

    if not pdf_text.strip():
        raise ValueError("PDF extraction returned empty text. Check the PDF content.")

    # Create chunks + embeddings
    chunks = chunk_text(pdf_text)
    print(f"🔧 Creating embeddings for {len(chunks)} chunks...")

    chunk_embeddings = embedder.encode(chunks, convert_to_tensor=True)

    print("🤖 StreetBase Chatbot Backend Ready!")
    return chunks, chunk_embeddings


# -------- Answering Queries --------
def answer_query(query: str, chunks, chunk_embeddings) -> str:
    """
    Given a user query + precomputed chunks & embeddings,
    find the most relevant chunk and ask the LLM to answer.
    """

    # Encode query
    query_emb = embedder.encode(query, convert_to_tensor=True)

    # Compute similarity with all chunks
    similarities = util.cos_sim(query_emb, chunk_embeddings)[0]
    best_index = torch.argmax(similarities).item()
    best_chunk = chunks[best_index]

    # Build prompt for LLM
    prompt = f"""
Use the following PDF context to answer clearly and accurately.

CONTEXT:
{best_chunk}

QUESTION:
{query}

ANSWER:
"""

    # Call LLM via OpenRouter
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": "You are an expert assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.2,
    )

    return response.choices[0].message.content
