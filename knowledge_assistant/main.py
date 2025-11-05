from ingest import load_documents, split_documents
from search import create_vector_store, search
from llm_integration import generate_answer, summarize_text
from escalate import escalate

import numpy as np
import os
import re
import json


def main():
    # 🚀 Load and prepare knowledge base
    docs = load_documents()
    chunks = split_documents(docs)
    index, texts = create_vector_store(chunks)

    # 🧠 Load persistent memory
    memory_file = "memory.json"
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            conversation_history = json.load(f)
    else:
        conversation_history = []

    # 📂 Tickets file path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tickets_path = os.path.join(project_root, "tickets", "escalations.json")
    print(f"🤖 Knowledge Assistant ready!\n📍 Tickets logged at: {tickets_path}\n")

    while True:
        query = input("💡 Ask me something (or type 'exit' to quit): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        # 🧠 Handle memory-based queries
        q_lower = query.lower().strip("?")

        if q_lower in [
            "what did i ask last time",
            "what did i ask previously",
            "what was my previous question"
        ]:
            if conversation_history:
                last_q = conversation_history[-1][0]
                print(f"🧠 Last question you asked was: {last_q}\n")
            else:
                print("🧠 I don't have any previous questions stored yet.\n")
            continue

        if q_lower in [
            "why did that happen",
            "why was that the case",
            "why did you say that"
        ]:
            if conversation_history:
                last_q, last_a = conversation_history[-1]
                if len(last_a.strip()) > 30:
                    followup_prompt = (
                        f"The user previously asked: '{last_q}'\n"
                        f"The assistant answered: '{last_a}'\n\n"
                        "Now the user asked: 'Why did that happen?'\n"
                        "Explain the reason behind the previous answer."
                    )
                    explanation = generate_answer(followup_prompt, [])
                    print(f"\n🧠 Explanation: {explanation}\n")
                else:
                    print("🧠 I don't have enough detail in the last answer to explain it.\n")
            else:
                print("🧠 I don't have enough context to explain that yet.\n")
            continue

        if q_lower in [
            "can you continue our last discussion",
            "continue our last discussion",
            "continue the previous topic",
            "continue from last time"
        ]:
            if conversation_history:
                last_q, last_a = conversation_history[-1]
                followup_prompt = (
                    f"The user previously asked: '{last_q}'\n"
                    f"The assistant answered: '{last_a}'\n\n"
                    "Now the user asked to continue the discussion. Respond with a relevant continuation."
                )
                continuation = generate_answer(followup_prompt, [])
                print(f"\n🧠 Continuing: {continuation}\n")
            else:
                print("🧠 I don't have a previous discussion to continue yet.\n")
            continue

        # 🔍 Perform vector search
        results, distances = search(query, index, texts)
        relevance = float(np.mean(distances))
        print(f"📊 Relevance distances: {distances}")

        answered_confidently = False
        final_answer = None
        source_filename = None

        # 🧠 Get LLM-based final answer with memory and multi-chunk context
        context = "\n".join(f"Q: {q}\nA: {a}" for q, a in conversation_history[-3:])
        combined_context = "\n\n".join(results)
        prompt = (
            f"{context}\n\nUse the following information to answer the new question:\n"
            f"{combined_context}\n\nQ: {query}\nA:"
        )
        answer = generate_answer(prompt, results)

        if "insufficient info" in answer.lower() or len(answer.strip()) < 20:
            # 🧪 Fallback if LLM is uncertain or answer is too short
            snippet, source_filename = keyword_based_fallback(query, chunks, return_source=True)
            if snippet:
                enriched = generate_answer(f"Expand and explain this:\n{snippet}", [])
                final_answer = summarize_text(enriched)
                print(f"\n✅ Answer: {final_answer}")
                if source_filename:
                    print(f"📚 Source: {source_filename}\n")
                answered_confidently = True
            else:
                escalate(query, "LLM uncertain and fallback failed.")
                print("⚠️ I couldn’t find enough information. A support ticket was created.")
        else:
            final_answer = summarize_text(answer)
            source_filename = find_source(results[0], chunks) if results else None
            print(f"\n✅ Answer: {final_answer}")
            if source_filename:
                print(f"📚 Source: {source_filename}\n")
            answered_confidently = True

        # 💬 Auto Follow-up Suggestions + Save to memory
        if answered_confidently and final_answer:
            conversation_history.append((query, final_answer))
            with open(memory_file, "w") as f:
                json.dump(conversation_history, f, indent=2)

            followups = generate_auto_followups(query, final_answer)
            if followups:
                print("🔄 Related Follow-up Questions:")
                for i, f in enumerate(followups, 1):
                    print(f"  {i}. {f}")
                print()  # spacing


def keyword_based_fallback(query, chunks, return_source=False):
    """🧪 Simple keyword match fallback to extract raw snippet when vector match fails."""
    text_words = lambda s: re.findall(r"\w+", s.lower())
    STOPWORDS = {
        "what", "are", "is", "the", "a", "an", "my", "of", "in", "on", "for",
        "to", "do", "does", "how", "when", "where", "who"
    }
    q_words = [w for w in text_words(query) if w not in STOPWORDS]
    if not q_words:
        return (None, None) if return_source else None

    for c in chunks:
        content = c.get("content", "")
        c_words = set(text_words(content))
        match_ratio = sum(1 for w in q_words if w in c_words) / len(q_words)
        if match_ratio >= 0.6:
            for w in q_words:
                idx = content.lower().find(w)
                if idx != -1:
                    start = max(0, idx - 200)
                    snippet = content[start: idx + len(w) + 200]
                    source = c.get("source")
                    return (snippet, source) if return_source else snippet
    return (None, None) if return_source else None


def find_source(matched_text, chunks):
    """🔍 Find the source filename for a given matched text snippet."""
    for c in chunks:
        if c.get("content") == matched_text:
            return c.get("source")
    return None


def generate_auto_followups(original_query: str, answer_text: str):
    """
    🧠 Generate 1–2 short follow-up questions strictly related
    to the original query and its answer.
    """
    try:
        prompt = (
            f"The user asked: '{original_query}'\n"
            f"The assistant replied: '{answer_text}'\n\n"
            "Now generate 2 short, relevant follow-up questions strictly about the same topic.\n"
            "Do NOT introduce new topics or unrelated ideas.\n"
            "Keep each question under 15 words.\n"
            "Return them as plain text, one per line."
        )
        raw = generate_answer(prompt, [])
        followups = [f.strip("-• ").strip() for f in raw.split("\n") if f.strip()]
        return followups[:2]
    except Exception:
        return []


if __name__ == "__main__":
    main()
