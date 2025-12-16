import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from backend.src.services.rag_service import retrieve_context, generate_rag_response, AnswerNotFoundException, RAGServiceException

# Mocking external services
@pytest.fixture
def mock_qdrant_client():
    with patch('backend.src.services.qdrant_service.get_qdrant_client') as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_openai_client():
    with patch('backend.src.services.openai_service.get_openai_client') as mock_get_client:
        mock_client = AsyncMock()
        mock_get_client.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_get_embedding():
    with patch('backend.src.services.openai_service.get_embedding') as mock_get_embedding_func:
        mock_get_embedding_func.return_value = [0.1, 0.2, 0.3]
        yield mock_get_embedding_func

@pytest.mark.asyncio
async def test_retrieve_context_success(mock_qdrant_client, mock_get_embedding):
    mock_qdrant_client.search.return_value = [
        MagicMock(payload={"content": "Test content 1"}),
        MagicMock(payload={"content": "Test content 2"}),
    ]
    context = retrieve_context("test query")
    assert len(context) == 2
    assert "Test content 1" in context
    mock_qdrant_client.search.assert_called_once()

@pytest.mark.asyncio
async def test_retrieve_context_empty(mock_qdrant_client, mock_get_embedding):
    mock_qdrant_client.search.return_value = []
    context = retrieve_context("test query")
    assert len(context) == 0
    mock_qdrant_client.search.assert_called_once()

@pytest.mark.asyncio
async def test_generate_rag_response_success(mock_openai_client, mock_qdrant_client, mock_get_embedding):
    mock_qdrant_client.search.return_value = [
        MagicMock(payload={"content": "Relevant book content."}),
    ]
    mock_openai_client.chat.completions.create.return_value = AsyncMock(choices=[MagicMock(delta=MagicMock(content="Bot response"))])

    response_chunks = [chunk async for chunk in generate_rag_response("test query")]
    assert "Bot response" in "".join(response_chunks)
    mock_qdrant_client.search.assert_called_once()
    mock_openai_client.chat.completions.create.assert_called_once()

@pytest.mark.asyncio
async def test_generate_rag_response_answer_not_found(mock_openai_client, mock_qdrant_client, mock_get_embedding):
    mock_qdrant_client.search.return_value = []

    with pytest.raises(AnswerNotFoundException, match="No relevant information found in the book content."):
        [chunk async for chunk in generate_rag_response("test query")]
    mock_qdrant_client.search.assert_called_once()
    mock_openai_client.chat.completions.create.assert_not_called()

@pytest.mark.asyncio
async def test_generate_rag_response_rag_service_exception(mock_openai_client, mock_qdrant_client, mock_get_embedding):
    mock_qdrant_client.search.return_value = [
        MagicMock(payload={"content": "Relevant book content."}),
    ]
    mock_openai_client.chat.completions.create.side_effect = Exception("OpenAI API error")

    with pytest.raises(RAGServiceException, match="Error generating response: OpenAI API error"):
        [chunk async for chunk in generate_rag_response("test query")]
    mock_qdrant_client.search.assert_called_once()
    mock_openai_client.chat.completions.create.assert_called_once()
