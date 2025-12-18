from langchain_chroma import Chroma
from .config import VECTOR_DB_DIR
import os

def create_vectorstore(documents, embedding_model):
    # Ensure the directory exists
    os.makedirs(VECTOR_DB_DIR, exist_ok=True)
    
    # Use from_documents to create and persist the vectorstore
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=VECTOR_DB_DIR
    )
    
    print(f"✅ Stored {len(documents)} documents in ChromaDB at {VECTOR_DB_DIR}")
    
    return vectordb


