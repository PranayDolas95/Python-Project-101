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
    """Create FAISS vector store from document chunks."""
    texts = [c["content"] for c in chunks]
    vectors = np.array(embeddings.embed_documents(texts)).astype("float32")

    # Initialize FAISS index (L2 distance metric)
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    return index, texts


def search(query, index, texts, k=3, return_indices=False):
    """
    Perform semantic search using FAISS index.

    Args:
        query (str): User query
        index (faiss.Index): FAISS index containing embedded chunks
        texts (list): List of chunk texts
        k (int): Number of top matches to retrieve
        return_indices (bool): Whether to also return FAISS indices

    Returns:
        tuple: (results, distances[, indices])
    """
    # Embed query
    query_vector = np.array([embeddings.embed_query(query)]).astype("float32")

    # Search top-k similar chunks
    distances, indices = index.search(query_vector, k)

    # Retrieve text results
    results = [texts[i] for i in indices[0]]

    if return_indices:
        return results, distances[0], indices[0]
    else:
        return results, distances[0]
