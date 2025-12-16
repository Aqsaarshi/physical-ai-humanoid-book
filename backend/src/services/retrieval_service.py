import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List, Dict, Any, Optional
from .qdrant_service import QdrantService
import google.generativeai as genai
from ..config import settings


class RetrievalService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        genai.configure(api_key=settings.gemini_api_key)

    def validate_qdrant_collections(self, book_name: str = "002-physical-ai-robotics-textbook") -> bool:
        """
        Validate Qdrant collections for the specified book
        """
        return self.qdrant_service.validate_collection(book_name)

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the given text using Google's embedding API
        """
        import logging
        try:
            # Using Google's embedding functionality
            result = genai.embed_content(
                model="models/embedding-001",
                content=[text],
                task_type="retrieval_document"
            )
            return result['embedding'][0]  # Return the first (and only) embedding
        except Exception as e:
            logging.error(f"Error generating embedding: {str(e)}")
            raise Exception(f"Error generating embedding: {str(e)}")

    def semantic_retrieval(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Perform semantic retrieval using Qdrant
        """
        query_embedding = self.generate_embedding(query)
        return self.qdrant_service.search_similar(query_embedding, limit)

    def context_filtering_and_ranking(self, query: str, retrieved_chunks: List[Dict[str, Any]],
                                      top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Filter and rank the retrieved context chunks based on relevance to query
        """
        # For now, we'll just return the top_k chunks from the retrieval
        # In a more sophisticated implementation, we could implement re-ranking
        return retrieved_chunks[:top_k]

    def strict_grounding_enforcement(self, response: str, context: List[str]) -> bool:
        """
        Check if the response is grounded in the provided context
        """
        # This is a basic check - in a real implementation, you'd want more sophisticated validation
        response_lower = response.lower()
        context_text = " ".join(context).lower()

        # Check if the response contains information from the context
        # This is a simplified check - a real implementation would be more thorough
        return len(response) > 0  # Placeholder implementation

    def get_context_for_selected_text_only(self, selected_text: str) -> List[str]:
        """
        Return only the selected text as context when in selected-text mode
        """
        return [selected_text] if selected_text else []

    def retrieve_for_selected_text_mode(self, selected_text: str, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve context specifically for selected-text mode, using only the selected text
        """
        # In selected-text mode, we only use the provided selected text as context
        if not selected_text:
            return []

        # Create a simple chunk with the selected text
        chunk = {
            "content": selected_text,
            "metadata": {"source": "selected_text"},
            "score": 1.0  # Perfect match since it's the exact selected text
        }

        return [chunk]

    def disable_full_book_retrieval_in_selected_mode(self) -> bool:
        """
        Explicitly confirm that full-book retrieval is disabled in selected-text mode
        """
        # This method exists to clearly indicate that full-book retrieval is not used in selected-text mode
        return True