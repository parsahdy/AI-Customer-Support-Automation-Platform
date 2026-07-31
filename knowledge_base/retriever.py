from pathlib import Path

import numpy as np

from .embedding_model import load_embedding_model
from .vector_store import load_index, load_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = PROJECT_ROOT / "data" / "knowledge_base" / "vector_index.faiss"
DOC_PATH = PROJECT_ROOT / "data" / "knowledge_base" / "documents.json"


class Retriever:

    def __init__(self):

        print(f"[INFO] Loading Knowledge Base...")

        self.model = load_embedding_model()
        self.index = load_index(INDEX_PATH)
        self.documents = load_documents(DOC_PATH)

        print(f"[INFO] Knowledge Base Loaded.")


    def embed_query(self, question: str) -> np.ndarray:

        return self.model.encode([question], convert_to_numpy=True).astype(np.float32)


    def retrieve(self, query_vector: np.ndarray, k):

        distances, indices = self.index.search(query_vector, k)

        return distances, indices


    def search(self, question: str, k: int = 3) -> list[dict]:

        query_vector = self.embed_query(question)

        distances, indices = self.retrieve(query_vector, k)

        results = []

        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx]

                results.append(
                    {
                        "content": doc["content"],
                        "metadata": doc["metadata"],
                        "distance": float(distance)
                    }
                )

        return results


if __name__ == "__main__":

    retriever = Retriever()

    while True:

        question = input("\nQuestion (exit to quit): ")

        if question.lower() == "exit":
            break

        results = retriever.search(question)

        print("\nTop Results")
        print("-" * 40)

        for i, doc in enumerate(results, start=1):

            print(f"\nResult {i}")

            print(doc["content"])

            print(doc["metadata"])

            print(f"Distance: {doc["distance"]:.2f}")