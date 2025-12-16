import unittest
from unittest.mock import Mock, patch
from src.services.retrieval_service import RetrievalService


class TestRetrievalService(unittest.TestCase):
    def setUp(self):
        self.retrieval_service = RetrievalService()

    @patch('src.services.qdrant_service.QdrantService')
    @patch('google.generativeai.embed_content')
    def test_generate_embedding(self, mock_embed_content, mock_qdrant_service):
        # Mock the embedding response
        mock_embed_content.return_value = {'embedding': [[0.1, 0.2, 0.3]]}

        result = self.retrieval_service.generate_embedding("test query")

        self.assertEqual(result, [0.1, 0.2, 0.3])
        mock_embed_content.assert_called_once()

    @patch('src.services.qdrant_service.QdrantService')
    def test_validate_qdrant_collections(self, mock_qdrant_service):
        # Mock the Qdrant service validation
        mock_qdrant_service.return_value.validate_collection.return_value = True

        result = self.retrieval_service.validate_qdrant_collections("test-book")

        self.assertTrue(result)

    def test_get_context_for_selected_text_only(self):
        selected_text = "This is the selected text."
        result = self.retrieval_service.get_context_for_selected_text_only(selected_text)

        self.assertEqual(result, [selected_text])

    def test_get_context_for_selected_text_only_empty(self):
        result = self.retrieval_service.get_context_for_selected_text_only("")

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()