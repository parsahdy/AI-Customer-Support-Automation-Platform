from pathlib import Path

import pandas as pd
import time

from document_loader import row_to_document
from vector_store import build_vector_store, save_index, save_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FAQ_PATH = PROJECT_ROOT / "data" / "cleaned" / "faq_clean.csv"
KB_DIR = PROJECT_ROOT / "data" / "knowledge_base"
INDEX_PATH = KB_DIR / "vector_index.faiss"
DOCS_PATH = KB_DIR / "documents.json"


def knowledge_base_pipeline():

    start = time.perf_counter()

    faq_df = pd.read_csv(FAQ_PATH)

    documents = [row_to_document(row) for row in faq_df.to_dict(orient="records")]

    index, embeddings = build_vector_store(documents)

    save_index(index, INDEX_PATH)
    save_documents(documents, DOCS_PATH)

    end = time.perf_counter()
    elapsed_time = end - start

    return {
        "index": index,
        "embeddings": embeddings,
        "documents": documents,
        "build_time": elapsed_time,
    }


def generate_statistics(result: dict) -> dict:

    documents = result["documents"]
    embeddings = result["embeddings"]

    return {
        "num_documents": len(documents),
        "average_document_lenght": round(sum(len(doc["content"]) for doc in documents) / len(documents) if documents else 0, 2),
        "embedding_dimension": embeddings.shape[1] if embeddings is not None else 0,
        "Index_type": "FAISS IndexFlatL2",
        "build_time": round(result["build_time"], 2),
    }


def print_statistics(stats: dict):

    print("\nKnowledge Base Summary")
    print("-" * 30)   

    for key, value in stats.items():
        print(f"{key}: {value}") 
    

if __name__ == "__main__":
    result = knowledge_base_pipeline()
    stats = generate_statistics(result)
    print_statistics(stats)