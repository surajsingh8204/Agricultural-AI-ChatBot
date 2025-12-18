from langchain_chroma import Chroma
from .embedder import get_embedding_model
from .config import VECTOR_DB_DIR

# Load embedding model once
_embedding_model = get_embedding_model()

# Load persisted Chroma DB
_vectordb = Chroma(
    persist_directory=VECTOR_DB_DIR,
    embedding_function=_embedding_model
)

def retrieve_context(query: str, domain: str, k: int = 3) -> str:
    if not domain:
        raise ValueError("Domain must be provided for retrieval")

    docs = _vectordb.similarity_search(
        query=query,
        k=k,
        filter={"domain": domain}   # 🔒 HARD FILTER
    )

    texts = []
    for doc in docs:
        texts.append(doc.page_content.strip())

    return "\n\n".join(texts)
