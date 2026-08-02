from pathlib import Path

import faiss
import numpy as np
import json

from .embedding_model import load_embedding_model


def build_vector_store(docs: list[dict]) -> tuple[faiss.Index, np.ndarray]:

    if not docs:
        raise ValueError("No documents provided.")

    texts = [doc["content"] for doc in docs]

    model = load_embedding_model()
    
    embeddings = model.encode(texts, convert_to_numpy=True).astype(np.float32)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index, embeddings


def save_index(index: faiss.Index, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(file_path))


def load_index(file_path: str) -> faiss.Index:
    return faiss.read_index(str(file_path))


def save_documents(documents: list[dict], file_path: Path) -> None:

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=4)


def load_documents(file_path: Path) -> list[dict]:
    
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)