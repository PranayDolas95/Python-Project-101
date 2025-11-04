import os
import re
import numpy as np
from ingest import load_documents, split_documents
from search import create_vector_store, search
from llm_integration import generate_answer, summarize_text
from escalate import escalate


def main():
    # === Load and Prepare Data ===
    docs = load_documents()
    chunks = split_documents(docs)
    index, texts = create_vector_store(chunks)

    # Map each chunk back to its source document
    chunk_sources = [c.get("source", "Unknown Document") for c in chunks]

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tickets_path = os.path.join(project_root, "tickets", "escalations.json")
    print(f"Knowledge Assistant ready!\nTickets logged at: {tickets_path}\n")

    # === Memory for Chatbot Behavior ===
    conversation_history = []  # stores last few Q&A turns

    while True:
        query = input(">> ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Goodbye! 👋")
            break

        # === Search Relevant Chunks ===
        results, distances, indices = search(query, index, texts, return_indices=True)
        relevance = float(np.mean(distances))
        print(f"[DEBUG] Relevance distances: {distances}")

        answered_confidently = False
        final_answer = None
        source_info = None

        # === Fallback for low relevance ===
        if relevance > float(os.getenv("RELEVANCE_THRESHOLD", 1.2)):
            snippet = keyword_based_fallback(query, chunks)
            if snippet:
                final_answer = summarize_text(snippet)
                source_info = "Keyword-based snippet (low relevance)"
                answered_confidently = True
            else:
                escalate(query, "Low relevance. Insufficient knowledge.")
                print("⚠️ I couldn’t find enough information. A support ticket was created.")
        else:
            # === Use GPT-4 with document context + memory ===
            context_docs = [
                {"content": results[i], "source": chunk_sources[indices[i]]}
                for i in range(len(results))
            ]
            answer = generate_answer(query, context_docs, conversation_history)

            if "not enough context" in answer.lower():
                snippet = keyword_based_fallback(query, chunks)
                if snippet:
                    final_answer = summarize_text(snippet)
                    source_info = "Keyword fallback"
                    answered_confidently = True
                else:
                    escalate(query, "LLM uncertain.")
                    print("⚠️ I couldn’t find enough information. A support ticket was created.")
            else:
                final_answer = summarize_text(answer)

                # ✅ Collect all unique sources from matched chunks
                unique_sources = sorted(set([doc["source"] for doc in context_docs]))
                if unique_sources:
                    source_info = ", ".join(unique_sources)
                else:
                    source_info = "Unknown Document"

                answered_confidently = True

        # === Display Answer with Sources ===
        if final_answer:
            print(f"\n🧠 Answer: {final_answer}")
            print(f"📘 Sources: {source_info}\n")

            # Add this Q&A to memory for contextual continuity
            conversation_history.append({"question": query, "answer": final_answer})
            if len(conversation_history) > 10:
                conversation_history.pop(0)

        # === Auto Follow-up Section ===
        if answered_confidently and final_answer:
            followups = generate_auto_followups(query, final_answer)
            if followups:
                # Ensure there are always exactly two
                if len(followups) < 2:
                    followups += [
                        "Can you tell me more about this?",
                        "How does this connect to the previous topic?",
                    ]
                print("💬 Follow-up suggestions:")
                for i, f in enumerate(followups[:2], 1):
                    print(f"  {i}. {f}")
                print()


# === Keyword-based fallback snippet ===
def keyword_based_fallback(query, chunks):
    """Simple keyword match fallback to extract raw snippet when vector match fails."""
    text_words = lambda s: re.findall(r"\w+", s.lower())
    STOPWORDS = {
        "what", "are", "is", "the", "a", "an", "my", "of", "in", "on", "for",
        "to", "do", "does", "how", "when", "where", "who"
    }
    q_words = [w for w in text_words(query) if w not in STOPWORDS]
    if not q_words:
        return None

    for c in chunks:
        content = c.get("content", "")
        c_words = set(text_words(content))
        match_ratio = sum(1 for w in q_words if w in c_words) / len(q_words)
        if match_ratio >= 0.6:
            for w in q_words:
                idx = content.lower().find(w)
                if idx != -1:
                    start = max(0, idx - 200)
                    return content[start: idx + len(w) + 200]
    return None


# === Follow-up Generation ===
def generate_auto_followups(original_query: str, answer_text: str):
    """Generate exactly 2 short, relevant follow-up questions strictly about the same topic."""
    try:
        from llm_integration import generate_answer
        prompt = (
            f"The user asked: '{original_query}'\n"
            f"The assistant replied: '{answer_text}'\n\n"
            "Generate 2 short, relevant follow-up questions strictly about the same topic.\n"
            "Do NOT introduce new topics or unrelated ideas.\n"
            "Each question should be under 15 words.\n"
            "Return them as plain text, one per line."
        )
        raw = generate_answer(prompt, [], [])
        followups = [f.strip("-• ").strip() for f in raw.split("\n") if f.strip()]
        return followups[:2]
    except Exception:
        return []


if __name__ == "__main__":
    main()
