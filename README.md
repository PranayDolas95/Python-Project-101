📘 README.md
markdown
# 🧠 Knowledge Assistant

A context-aware, memory-enabled Python assistant that answers questions using a custom document knowledge base. It supports persistent memory, intelligent fallback logic, and conversational follow-ups — making it ideal for internal knowledge retrieval, document Q&A, and smart assistants.

---

## 🚀 Features

- 🔍 Vector search over document chunks
- 🧠 LLM-powered answers with memory context
- 💾 Persistent memory across sessions
- 🧪 Intelligent fallback using keyword matching
- 🔄 Auto-generated follow-up questions
- 📚 Source attribution for each answer
- ⚠️ Escalation logging for unresolved queries

---

## 🧱 Architecture Overview

The assistant follows a modular pipeline:

User Query │ ▼ [main.py] → Entry point, memory handling, routing │ ▼ [search.py] → Vector search using embeddings │ ▼ [llm_integration.py] → OpenAI GPT-4o for answer generation and summarization │ ▼ [ingest.py] → Document loading and chunking │ ▼ [escalate.py] → Logs unresolved queries │ ▼ [memory.json] → Stores persistent Q&A history

Code

---

## 🛠️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/PranayDolas95/Python-Project-101.git
cd Python-Project-101
2. Create a Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install Dependencies
bash
pip install -r requirements.txt
4. Add Your OpenAI API Key
Create a .env file in the root directory:

Code
OPENAI_API_KEY=your-api-key-here
▶️ Running the Assistant
bash
python knowledge_assistant/main.py
You’ll see:

Relevance scores for each query

Detailed answers with source attribution

Follow-up suggestions

Memory-aware responses like:

“What did I ask last time?”

“Why did that happen?”

“Can you continue our last discussion?”

📁 File Structure
Code
Python-Project-101/
├── knowledge_assistant/
│   ├── main.py                 # Core logic and memory handling
│   ├── ingest.py               # Document loading and chunking
│   ├── search.py               # Vector search logic
│   ├── llm_integration.py      # GPT-4o answer generation
│   ├── escalate.py             # Escalation logging
│   ├── memory.json             # Persistent memory store
├── tickets/
│   └── escalations.json        # Logged unresolved queries
├── .env                        # Your OpenAI API key (not committed)
├── .env.example                # Safe placeholder for sharing
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                  # Prevents clutter from pycache, env, etc.
🧪 Sample Queries to Test Memory
text
1. What is the projection cost?
2. What did I ask last time?
3. Why did that happen?
4. Can you continue our last discussion?
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

📄 License
This project is licensed under the MIT License.

🙌 Credits
Built by Harshwardhan for Pranay Dolas Powered by OpenAI GPT-4o Maintained with ❤️ and Python

Code

---

Let me know if you want:
- A visual architecture diagram (I can generate one)
- A GitHub project banner or logo
- A demo GIF or video walkthrough

This README will make your project shine on GitHub — professional, clear, and ready for collaboration 🚀
