# 🧠 Knowledge Assistant CLI

A modular **Retrieval-Augmented Generation (RAG)** based command-line Knowledge Assistant that answers user queries from your custom documents.  
If the assistant cannot find a confident answer, it **creates an escalation ticket**, and for each correct answer, it automatically **suggests a relevant follow-up question**.

---

## 🚀 Features

✅ **Document Ingestion** – Load and split large documents into searchable chunks  
✅ **Semantic Search** – Retrieve the most relevant chunks using vector similarity  
✅ **LLM-Powered Answers** – Generate concise, context-aware answers using an LLM  
✅ **Automatic Follow-up Questions** – Suggest a contextually relevant follow-up after each successful answer  
✅ **Escalation System** – Log unanswered or low-confidence queries into a ticket file for review  
✅ **Configurable Threshold** – Adjust the relevance score cutoff for fallback/escalation behavior  

---

## 🏗️ Project Structure

knowledge-assistant/
│
├── ingest.py # Document loader and splitter
├── search.py # Vector store creation and semantic search
├── llm_integration.py # LLM answer generation, summarization, and follow-up
├── escalate.py # Escalation ticket handler
├── main.py # CLI controller and logic orchestrator
│
├── data/ # Folder containing knowledge base documents
├── tickets/
│ └── escalations.json # Logged escalation tickets
│
├── requirements.txt # Dependencies list
└── README.md # Project documentation

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/knowledge-assistant.git
cd knowledge-assistant
2. Create a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Set Environment Variables
Create a .env file or export variables manually:

bash
Copy code
RELEVANCE_THRESHOLD=1.2
OPENAI_API_KEY=your_api_key_here
5. Add Documents
Place your knowledge base files (PDFs, text, etc.) inside the data/ directory.

🧩 How It Works
Document Ingestion

ingest.py loads all documents and splits them into small text chunks for efficient retrieval.

Vector Search

search.py embeds each chunk and builds a vector index.

When you ask a question, it finds the most similar chunks by semantic meaning.

Answer Generation

llm_integration.py combines the retrieved context with your question.

It uses an LLM to form a contextually aware answer.

Then, it summarizes the answer for clarity.

Follow-up Generation

After a correct answer, a relevant follow-up question is automatically generated to deepen user understanding.

Escalation

If the assistant cannot find enough relevant information (low relevance or weak LLM confidence),
a ticket is created inside tickets/escalations.json with the question and timestamp.

🧠 Example Usage
bash
Copy code
$ python main.py
Knowledge Assistant ready!
Tickets logged at: /path/to/tickets/escalations.json

>> What is data encryption?
Relevance distances: [0.45, 0.52, 0.60]

Answer:
Data encryption is the process of converting readable data into coded form to prevent unauthorized access.

Follow-up:
Would you like to learn about the different types of encryption methods?
If relevance is too low:

bash
Copy code
>> What is alien signal detection?
Relevance distances: [1.78, 1.94]
I couldn’t find enough information. A support ticket was created.
🧱 Architecture Overview
🔹 Modules and Responsibilities
Module	Responsibility
ingest.py	Load and split documents into chunks
search.py	Create embeddings and perform semantic search
llm_integration.py	Generate, summarize, and produce follow-up questions
escalate.py	Create structured JSON tickets for unresolved queries
main.py	User interaction loop, orchestration logic, and decision control

🧩 Logic Flow
text
Copy code
User Query
   ↓
Vector Search (semantic)
   ↓
If Relevance < Threshold → Keyword Fallback → Escalate (ticket)
   ↓
If Relevance ≥ Threshold → LLM Answer → Summarize → Generate Follow-up
   ↓
Display Answer + Follow-up
📁 Escalation Ticket Format
Example escalations.json entry:

json
Copy code
{
  "reference_id": "b7e2a3f0-92b1-45d8-9f63-d7a2a81a1a2f",
  "timestamp": "2025-10-27T14:21:36Z",
  "question": "What is quantum cloud networking?",
  "reason": "Low relevance. Insufficient knowledge."
}
🧩 Customization
Feature	Description	How to Modify
Relevance Threshold	Controls when fallback or escalation triggers	Change RELEVANCE_THRESHOLD in .env
Embedding Model	Change text vectorization model	Modify create_vector_store() in search.py
LLM Provider	Use OpenAI, Anthropic, or Local LLMs	Update generate_answer() in llm_integration.py
Ticket Storage	Change log location or format	Edit escalate.py

🧪 Future Enhancements
🌐 Web-based dashboard for reviewing escalations

💾 Persistent vector store (FAISS, Qdrant, or ChromaDB)

🔁 Auto-learning: add resolved tickets back to the knowledge base

🗣️ Multi-turn conversation context memory

🧑‍💻 Author
Himanshu Sapkale
💼 DevSecOps Engineer | Cloud Security Enthusiast
📧 [youremail@example.com]
🌐 [LinkedIn Profile or Portfolio link]

🪪 License
This project is licensed under the MIT License – feel free to use, modify, and distribute with attribution.

🏁 Summary
The Knowledge Assistant bridges the gap between automated document intelligence and human escalation, enabling:

Faster knowledge retrieval

Transparent fallback mechanisms

Smart contextual conversations

It’s a lightweight, extensible, and intelligent foundation for internal enterprise knowledge management systems.

pgsql
Copy code

---

Would you like me to make this README **automatically generate and update version info (e.g., build date, version number)** in the header each time you run the app?  
That can make it look like a professional maintained project.
