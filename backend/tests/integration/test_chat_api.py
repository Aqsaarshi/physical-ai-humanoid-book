import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.main import app  # Assuming your FastAPI app is in main.py
from src.services.rag_service import RAGService


@pytest.fixture
def client():
    return TestClient(app)


@patch('src.services.rag_service.RAGService')
def test_chat_query_endpoint_success(mock_rag_service, client):
    # Mock the RAG service response
    mock_rag_service.return_value.generate_answer_with_context.return_value = {
        "content": "This is a test response",
        "citations": [{"chapter": "Chapter 1", "section": "Section 1.1"}],
        "confidence": "high"
    }

    response = client.post(
        "/chat/query",
        json={
            "query": "Test question",
            "context_mode": "full-book"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "response_id" in data
    assert data["content"] == "This is a test response"
    assert len(data["citations"]) == 1


@patch('src.services.rag_service.RAGService')
def test_chat_query_endpoint_with_selected_text(mock_rag_service, client):
    # Mock the RAG service response
    mock_rag_service.return_value.generate_answer_with_context.return_value = {
        "content": "Response based on selected text",
        "citations": [{"chapter": "Selected Text", "section": "User Selection"}],
        "confidence": "high"
    }

    response = client.post(
        "/chat/query",
        json={
            "query": "Test question about selection",
            "context_mode": "selected-text",
            "selected_text": {
                "text": "This is the selected text",
                "source_metadata": {"chapter": "Chapter 2", "section": "Section 2.1"}
            }
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "response_id" in data
    assert data["content"] == "Response based on selected text"


def test_chat_history_endpoint(client):
    # Test with a non-existent session ID
    response = client.get("/chat/history/non-existent-session-id")

    assert response.status_code == 422  # Validation error for invalid UUID