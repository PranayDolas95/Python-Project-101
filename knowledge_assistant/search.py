import os
import faiss
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize embeddings with explicit API key
embeddings = OpenAIEmbeddings(openai_api_key=api_key)

def create_vector_store(chunks):
    texts = [c["content"] for c in chunks]
    vectors = np.array(embeddings.embed_documents(texts)).astype("float32")
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, texts

def search(query, index, texts, k=3):
    query_vector = np.array([embeddings.embed_query(query)]).astype("float32")
    distances, indices = index.search(query_vector, k)
    results = [texts[i] for i in indices[0]]
    return results, distances[0]

