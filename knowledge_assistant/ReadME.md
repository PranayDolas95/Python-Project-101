# 🧠 Knowledge Assistant Module

This folder contains the core logic for the Knowledge Assistant — a memory-aware, document-driven conversational agent that uses vector search and LLMs to answer user questions with context and continuity.

---

## 📦 Module Overview

The `knowledge_assistant/` package is responsible for:

- Loading and chunking documents
- Creating and querying a vector store
- Generating LLM-based answers with memory context
- Handling fallback logic and escalations
- Persisting memory across sessions
- Suggesting follow-up questions

---

## 🧩 Module Components

| File                  | Responsibility                                                                 |
|-----------------------|---------------------------------------------------------------------------------|
| `main.py`             | Entry point. Manages user input, memory, search, LLM prompts, and output.       |
| `ingest.py`           | Loads documents and splits them into semantic chunks for indexing.              |
| `search.py`           | Creates a vector store and performs similarity search using embeddings.         |
| `llm_integration.py`  | Interfaces with OpenAI to generate answers and summaries.                       |
| `escalate.py`         | Logs unresolved queries to `tickets/escalations.json` for human review.         |
| `memory.json`         | Stores persistent Q&A history across sessions (auto-generated at runtime).      |

---

## 🧠 Memory-Aware Behavior

The assistant uses `memory.json` to:
- Recall the last few questions and answers
- Enrich prompts with recent context
- Handle queries like:
  - “What did I ask last time?”
  - “Why did that happen?”
  - “Can you continue our last discussion?”

---

## 🧪 Fallback Logic

If the LLM is uncertain or the vector search is weak, the assistant:
1. Performs a keyword-based fallback search
2. Expands the matched snippet using the LLM
3. Summarizes the result for the user

---

## 🔄 Follow-up Suggestions

After each confident answer, the assistant:
- Generates 1–2 short, relevant follow-up questions
- Displays them to guide the user’s next steps

---

## 🛠️ How to Run

From the project root:

```bash
python knowledge_assistant/main.py
