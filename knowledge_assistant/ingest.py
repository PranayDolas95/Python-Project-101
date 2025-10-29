import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_documents(data_dir=r"C:\Users\Harshwardhan\mini-genai-assistant\data"):
    docs = []
    for file in os.listdir(data_dir):
        path = os.path.join(data_dir, file)
        try:
            if file.lower().endswith(".pdf"):
                print(f"Loading PDF: {file}")
                loader = PyPDFLoader(path)
                pages = loader.load()
                for page in pages:
                    docs.append({"source": file, "content": page.page_content})
            elif file.lower().endswith((".pptx", ".ppt")):
                print(f"Loading PowerPoint: {file}")
                loader = UnstructuredPowerPointLoader(path)
                document = loader.load()
                for page in document:
                    docs.append({"source": file, "content": page.page_content})
        except Exception as e:
            print(f"Error loading {file}: {str(e)}")
            continue
    return docs

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    all_chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["content"]):
            all_chunks.append({"source": doc["source"], "content": chunk})
    return all_chunks

