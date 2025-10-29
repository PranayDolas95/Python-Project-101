import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError(
        "OPENAI_API_KEY is not set. Please add it to your .env file or system environment variables."
    )

# Mask part of key for logging
masked = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 12 else "(hidden)"
print(f"Using OpenAI API key: {masked}")

# Initialize client
client = OpenAI(api_key=api_key)


# ---------- Generate Answer from Context ----------
def generate_answer(query, context_chunks):
    """Answer the question using retrieved chunks only."""
    context = "\n\n".join(context_chunks)
    prompt = f"""
You are a precise knowledge assistant.
Answer the question using strictly the context below.
If answer not found, say "insufficient info".

Context:
{context}

Question: {query}
Answer:
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    try:
        return response.choices[0].message.content.strip()
    except Exception:
        return getattr(response, "text", "").strip()


# ---------- Summarize Long Text to 1–2 Lines ----------
def summarize_text(text):
    """Condense retrieved raw text or snippets into a 1–2 line human summary."""
    prompt = f"Summarize the following text in 1–2 sentences, clearly and naturally:\n\n{text[:1800]}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=60,
    )
    try:
        return response.choices[0].message.content.strip()
    except Exception:
        return getattr(response, "text", "").strip()
