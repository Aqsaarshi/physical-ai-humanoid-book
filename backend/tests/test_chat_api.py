import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.main import app
from backend.src.services.db_service import get_db
from backend.src.models.chat import Base, ChatConversation, ChatMessage
from datetime import datetime

# Setup for in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_rag_service():
    with patch('backend.src.services.rag_service.generate_rag_response') as mock_generate:
        async def async_generator(response_text):
            yield response_text
        mock_generate.return_value = async_generator("Mocked RAG response")
        yield mock_generate

@pytest.fixture
def mock_citation_service():
    with patch('backend.src.services.citation_service.extract_citations') as mock_extract:
        mock_extract.return_value = [{"chapter": "Test Chapter", "section": "Test Section"}]
        yield mock_extract

@pytest.fixture
def mock_openai_embedding():
    with patch('backend.src.services.openai_service.get_embedding') as mock_get_embedding_func:
        mock_get_embedding_func.return_value = [0.1, 0.2, 0.3]
        yield mock_get_embedding_func

@pytest.fixture
def mock_qdrant_client_search():
    with patch('backend.src.services.qdrant_service.QdrantClient.search') as mock_search:
        mock_search.return_value = [MagicMock(payload={"content": "Mocked Qdrant content"})]
        yield mock_search


def test_ask_chatbot_new_conversation(client, mock_rag_service, mock_citation_service, mock_openai_embedding, mock_qdrant_client_search):
    response = client.post(
        "/api/chat/ask",
        json={
            "user_question": "What is FastAPI?"
        }
    )
    assert response.status_code == 200
    data = response.text  # Streaming response, get text
    assert "Mocked RAG response" in data
    assert "Test Chapter" in data

    # Verify conversation and messages are saved
    conversations_response = client.get("/api/chat/conversations")
    assert conversations_response.status_code == 200
    conversations = conversations_response.json()["conversations"]
    assert len(conversations) == 1
    conversation_id = conversations[0]["id"]

    history_response = client.get(f"/api/chat/history/{conversation_id}")
    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history["messages"]) == 2 # user and bot message


def test_ask_chatbot_existing_conversation(client, session, mock_rag_service, mock_citation_service, mock_openai_embedding, mock_qdrant_client_search):
    # Create an initial conversation
    conversation = ChatConversation(title="Existing Chat", created_at=datetime.now())
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    existing_conversation_id = conversation.id

    response = client.post(
        "/api/chat/ask",
        json={
            "user_question": "How does it work?",
            "conversation_id": existing_conversation_id
        }
    )
    assert response.status_code == 200
    data = response.text
    assert "Mocked RAG response" in data

    # Verify messages are added to existing conversation
    history_response = client.get(f"/api/chat/history/{existing_conversation_id}")
    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history["messages"]) == 2 # 2 new messages (user + bot)


def test_get_chat_history(client, session):
    conversation = ChatConversation(title="History Test", created_at=datetime.now())
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    conversation_id = conversation.id

    client.post(
        "/api/chat/ask",
        json={
            "user_question": "Test history question",
            "conversation_id": conversation_id
        }
    )

    response = client.get(f"/api/chat/history/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["conversation"]["id"] == conversation_id
    assert len(data["messages"]) == 2
    assert data["messages"][0]["sender"] == "user"
    assert data["messages"][1]["sender"] == "bot"


def test_get_all_conversations(client, session):
    conv1 = ChatConversation(title="Chat One", created_at=datetime.now())
    conv2 = ChatConversation(title="Chat Two", created_at=datetime.now())
    session.add_all([conv1, conv2])
    session.commit()

    response = client.get("/api/chat/conversations")
    assert response.status_code == 200
    data = response.json()
    assert len(data["conversations"]) == 2
    assert data["conversations"][0]["title"] == "Chat Two" # Ordered by created_at desc
    assert data["conversations"][1]["title"] == "Chat One"

def test_ask_chatbot_answer_not_found(client, mock_rag_service, mock_citation_service, mock_openai_embedding, mock_qdrant_client_search):
    mock_rag_service.return_value = AsyncMock(side_effect=AnswerNotFoundException("No info"))
    response = client.post(
        "/api/chat/ask",
        json={
            "user_question": "Irrelevant question"
        }
    )
    assert response.status_code == 404
    assert "No answer found for your question" in response.json()["message"]

def test_ask_chatbot_rag_service_exception(client, mock_rag_service, mock_citation_service, mock_openai_embedding, mock_qdrant_client_search):
    mock_rag_service.return_value = AsyncMock(side_effect=RAGServiceException("Internal RAG error"))
    response = client.post(
        "/api/chat/ask",
        json={
            "user_question": "Any question"
        }
    )
    assert response.status_code == 500
    assert "An internal error occurred in the RAG service." in response.json()["message"]
