from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(raw_documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    documents = []

    for item in raw_documents:
        text_chunks = splitter.split_text(item["content"])
        for chunk in text_chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata=item["metadata"]
                )
            )

    return documents


