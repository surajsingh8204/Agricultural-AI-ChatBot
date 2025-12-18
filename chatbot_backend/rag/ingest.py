from .loader import load_rag_documents
from .chunker import chunk_documents
from .embedder import get_embedding_model
from .vectorstore import create_vectorstore

print("🔹 Loading RAG data...")
docs = load_rag_documents("data/rag_data")

print(f"🔹 Loaded {len(docs)} documents")

print("🔹 Chunking...")
chunks = chunk_documents(docs)

print(f"🔹 Created {len(chunks)} chunks")

print("🔹 Creating embeddings & vector store...")
embedding = get_embedding_model()
create_vectorstore(chunks, embedding)

print("✅ RAG ingestion complete")
