knowledge_assistant/README.md
# 🧠 Knowledge Assistant — Submodule Overview

This folder implements the **core Knowledge Assistant system**, which allows users to ask questions from a knowledge base, search semantically relevant documents, and receive summarized, LLM-based answers.  
It also supports **automatic escalation** when information is missing, and can now generate **contextual follow-up questions** for deeper engagement.

---

## ⚙️ Architecture Overview

The Knowledge Assistant is composed of five main components:



main.py ───────► ingest.py ───► search.py ───► llm_integration.py ───► escalate.py
│
└────► Handles user interaction loop (queries, fallback, and follow-ups)


---

## 🧩 Module Breakdown

### 1. **`main.py` — Entry Point**
- Runs the main CLI loop (`while True`) to accept user queries.
- Loads and splits documents using `ingest.py`.
- Builds a vector index using `search.py`.
- For each query:
  - Performs semantic search to find relevant text.
  - Uses a relevance threshold to decide whether to:
    - Generate an answer using the LLM (`llm_integration.py`), or
    - Escalate to support (`escalate.py`).
- Implements a **keyword-based fallback** if semantic relevance is weak.
- Automatically generates **relevant follow-up questions** after providing a correct answer.

### 2. **`ingest.py` — Document Loader**
- Reads PDF, TXT, DOCX, or other supported files.
- Cleans and converts them into a standardized format.
- Splits documents into manageable **text chunks** (e.g., 500–1000 tokens each).
- Returns a list of structured chunks (for vector embedding and search).

### 3. **`search.py` — Vector Search Engine**
- Converts document chunks into vector embeddings.
- Stores them in an in-memory or on-disk vector store (e.g., FAISS, numpy).
- Provides a function to perform **semantic similarity search** against user queries.
- Returns the top matching chunks and similarity distances.

### 4. **`llm_integration.py` — Language Model Interface**
- Integrates with a Large Language Model (LLM) API (like OpenAI, local LLM, or Ollama).
- Functions include:
  - `generate_answer(query, retrieved_docs)` — produces an AI-generated answer.
  - `summarize_text(text)` — generates a concise version of a long answer.
  - `generate_follow_up_question(query, answer)` — creates a natural follow-up question related to the user’s last query.
- Ensures responses are **context-aware**, **fact-based**, and **concise**.

### 5. **`escalate.py` — Ticket Creation System**
- Creates a **support escalation ticket** when:
  - Relevance is too low,
  - The LLM reports “insufficient information”, or
  - No matching snippet is found.
- Saves escalations into `tickets/escalations.json` with metadata like:
  - Question, timestamp, reason, and unique reference ID.

---

## 🔁 Query Flow

1. **User asks a question**


What are the benefits of using data encryption?


2. **System retrieves relevant chunks**
- Uses semantic search on indexed documents.
- Computes similarity distances.

3. **Decision based on relevance**
- If high → answer with LLM.
- If low → fallback to keyword snippet or escalate.

4. **LLM generates final answer**


Answer: Data encryption protects sensitive information from unauthorized access...


5. **Follow-up Question Generated**


Follow-up: Would you like to learn about symmetric vs asymmetric encryption?


---

## 🧠 Logic for Follow-Up Generation

Follow-up questions are created **only when a confident answer is provided**.

The logic is:
1. After generating a valid answer → call `generate_follow_up_question()`.
2. The model crafts a **relevant** and **contextually linked** follow-up.
3. The user is prompted automatically to continue the discussion.

---

## 🧰 Configuration

- **Relevance Threshold:** Controlled via environment variable `RELEVANCE_THRESHOLD` (default: `1.2`).
- **Ticket Storage:** JSON file under `tickets/escalations.json`.
- **Embeddings & Search:** Uses vector embeddings from local or API model.

---

## 🧪 Example Run



Knowledge Assistant ready!
Tickets logged at: /path/to/tickets/escalations.json

What is data masking?
Relevance distances: [0.89, 0.92, 1.01]
Answer: Data masking hides sensitive data by replacing it with realistic but fictitious values.

Follow-up: Would you like me to explain how dynamic data masking works?


---

## 🧾 Future Enhancements

- Add **document ingestion from URLs or APIs**
- Add **RAG (Retrieval-Augmented Generation)** pipeline integration
- Enhance **ticket analytics dashboard**
- Introduce **user authentication and feedback tracking**

---

## 📂 File Summary

| File | Description |
|------|--------------|
| `main.py` | Core logic and user interaction |
| `ingest.py` | Document loading and chunking |
| `search.py` | Vector embeddings and similarity search |
| `llm_integration.py` | LLM calls and summarization |
| `escalate.py` | Support ticket creation and logging |
| `tickets/escalations.json` | Auto-generated ticket log file |

---

### 🧑‍💻 Author
Developed by **Pranay Dolas**  
Part of the **Python Project 101** repository.
