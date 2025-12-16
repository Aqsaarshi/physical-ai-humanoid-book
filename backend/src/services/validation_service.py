import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List, Dict, Any
from .qdrant_service import QdrantService
from .retrieval_service import RetrievalService


class ValidationService:
    def __init__(self):
        self.qdrant_service = QdrantService()
        self.retrieval_service = RetrievalService()

    def validate_context_grounding(self, response: str, retrieved_context: List[Dict[str, Any]]) -> bool:
        """
        Validate that the response is grounded in the provided context
        """
        context_texts = [chunk["content"] for chunk in retrieved_context]
        return self.retrieval_service.strict_grounding_enforcement(response, context_texts)

    def validate_book_scope(self, question: str, book_content: List[Dict[str, Any]]) -> bool:
        """
        Validate that the question is within the scope of the book content
        """
        # Basic validation - check if there's relevant content in the book
        return len(book_content) > 0

    def validate_no_external_knowledge(self, response: str, context: List[str]) -> bool:
        """
        Ensure the response doesn't contain information not present in the context
        """
        # This is a basic check - a more sophisticated implementation would be needed
        # for comprehensive validation
        return True  # Placeholder for now

    def handle_out_of_scope_query(self, question: str) -> str:
        """
        Generate appropriate response for out-of-scope queries
        """
        return "I cannot answer based on the provided book content. The question appears to be outside the scope of the available information."