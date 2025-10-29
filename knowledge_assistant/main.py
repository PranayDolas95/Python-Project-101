from ingest import load_documents, split_documents
from search import create_vector_store, search
from llm_integration import generate_answer, summarize_text
from escalate import escalate

import numpy as np
import os
import re


def main():
    docs = load_documents()
    chunks = split_documents(docs)
    index, texts = create_vector_store(chunks)

    # Tickets file path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tickets_path = os.path.join(project_root, "tickets", "escalations.json")
    print(f"Knowledge Assistant ready!\nTickets logged at: {tickets_path}\n")

    while True:
        query = input(">> ").strip()
        if query.lower() in ["exit", "quit"]:
            break

        # Perform vector search
        results, distances = search(query, index, texts)
        relevance = float(np.mean(distances))
        print(f"Relevance distances: {distances}")

        # Threshold-based logic
        if relevance > float(os.getenv("RELEVANCE_THRESHOLD", 1.2)):
            # Keyword fallback if vector match weak
            snippet = keyword_based_fallback(query, chunks)
            if snippet:
                short_summary = summarize_text(snippet)
                print(f"\nAnswer: {short_summary}\n")
            else:
                escalate(query, "Low relevance. Insufficient knowledge.")
                print("I couldn’t find enough information. A support ticket was created.")
        else:
            # Get LLM-based final answer
            answer = generate_answer(query, results)

            if "insufficient info" in answer.lower():
                snippet = keyword_based_fallback(query, chunks)
                if snippet:
                    short_summary = summarize_text(snippet)
                    print(f"\nAnswer: {short_summary}\n")
                else:
                    escalate(query, "LLM uncertain.")
                    print("I couldn’t find enough information. A support ticket was created.")
            else:
                short_final = summarize_text(answer)
                print(f"\nAnswer: {short_final}\n")


def keyword_based_fallback(query, chunks):
    """Simple keyword match fallback to extract raw snippet when vector match fails."""
    text_words = lambda s: re.findall(r"\w+", s.lower())
    STOPWORDS = {"what", "are", "is", "the", "a", "an", "my", "of", "in", "on", "for", "to", "do", "does", "how", "when", "where", "who"}
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
                    return content[start : idx + len(w) + 200]
    return None


if __name__ == "__main__":
    main()
