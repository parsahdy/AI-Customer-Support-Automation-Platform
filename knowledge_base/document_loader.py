import pandas as pd


def row_to_document(row: pd.Series) -> dict:

    question = row["question"]
    answer = row["answer"]
    document_id = row["document_id"]

    return {
        "content": f"Question:\n{question}\n\nAnswer:\n{answer}",
        "metadata": {
            "document_id": document_id,
            "source": "faq",
        }
    }