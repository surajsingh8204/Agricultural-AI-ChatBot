
import os
from pathlib import Path

EMBEDDING_MODEL =  "sentence-transformers/all-MiniLM-L6-v2"

# Get absolute path for vector_db relative to project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTOR_DB_DIR = str(PROJECT_ROOT / "vector_db")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
