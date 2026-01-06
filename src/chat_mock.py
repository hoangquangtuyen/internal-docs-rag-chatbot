"""
Mock LLM / RAG layer
Used for cloud deployment to avoid API cost.

This module simulates:
- document retrieval
- answer generation
"""

from typing import Dict, List


def fake_retrieve(query: str) -> List[str]:
    """
    Simulate document retrieval (FAKE).
    """
    if "quy trình" in query.lower():
        return ["internal_process.md"]
    if "chính sách" in query.lower():
        return ["company_policy.pdf"]
    return ["general_docs.txt"]


def generate_answer(query: str, docs: List[str]) -> str:
    """
    Simulate LLM generation (FAKE).
    """
    return (
        "Dựa trên tài liệu nội bộ, tôi tìm thấy thông tin liên quan "
        f"đến câu hỏi: '{query}'.\n"
        f"Tài liệu tham khảo: {', '.join(docs)}."
    )


def get_chat_response(query: str) -> Dict:
    """
    Main entry used by FastAPI.
    """
    if not query:
        return {
            "answer": "Vui lòng nhập câu hỏi.",
            "sources": [],
            "confidence": 0.0,
            "mode": "mock"
        }

    docs = fake_retrieve(query)
    answer = generate_answer(query, docs)

    return {
        "answer": answer,
        "sources": docs,
        "confidence": 0.75,
        "mode": "mock"
    }
