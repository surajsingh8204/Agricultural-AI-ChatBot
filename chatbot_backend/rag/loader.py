import json
from pathlib import Path
from typing import List, Dict


def flatten_json(data: Dict) -> str:
    """
    Convert structured JSON data into clean natural language text
    for high-quality embeddings.
    """
    parts = []

    for key, value in data.items():
        if isinstance(value, str):
            parts.append(value)

        elif isinstance(value, list):
            parts.extend([str(v) for v in value])

        elif isinstance(value, dict):
            parts.extend([str(v) for v in value.values()])

    return " ".join(parts)


def load_rag_documents(relative_data_path: str) -> List[Dict]:
    documents = []

    # Resolve project root safely
    project_root = Path(__file__).resolve().parents[2]
    base_path = project_root / relative_data_path

    if not base_path.exists():
        raise FileNotFoundError(f"RAG data path not found: {base_path}")

    for domain_dir in base_path.iterdir():
        if not domain_dir.is_dir():
            continue

        domain = domain_dir.name

        for file in domain_dir.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                data_list = json.load(f)

                if not isinstance(data_list, list):
                    raise ValueError(f"{file} must contain a JSON list")

                for data in data_list:
                    text = flatten_json(data)

                    documents.append({
                        "content": text,
                        "metadata": {
                            "domain": domain,
                            "id": data.get("id", ""),
                            "crop": data.get("crop", "all"),
                            "region": data.get("region", "India")
                        }
                    })

    return documents


