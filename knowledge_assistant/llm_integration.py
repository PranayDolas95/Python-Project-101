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
def generate_answer(query, context_chunks, conversation_history=None):
    """
    Answer the question using retrieved chunks and optional conversation history.
    """
    # Combine all chunks into a rich context
    context = "\n\n".join(
        f"Source: {c.get('source', 'Unknown')}\n{c['content']}"
        if isinstance(c, dict) else str(c)
        for c in context_chunks
    )

    # Include recent conversation history
    history_text = ""
    if conversation_history:
        history_text = "\n\n".join(
            f"Q: {h['question']}\nA: {h['answer']}" for h in conversation_history[-5:]
        )

    # Prompt for detailed answer
    prompt = f"""
You are a precise and helpful knowledge assistant.
Use only the provided context and conversation history to answer the question in detail.
If the answer is not found, say "insufficient info".

Conversation history:
{history_text or '(none)'}

Context:
{context}

Question: {query}

Answer (in 3–5 sentences):
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    try:
        return response.choices[0].message.content.strip()
    except Exception:
        return getattr(response, "text", "").strip()


# ---------- Summarize Long Text to 1–2 Sentences ----------
def summarize_text(text):
    """Condense retrieved raw text or snippets into a brief, natural summary."""
    prompt = f"Summarize the following text in 2–3 clear, informative sentences:\n\n{text[:1800]}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100,
    )
    try:
        return response.choices[0].message.content.strip()
    except Exception:
        return getattr(response, "text", "").strip()
