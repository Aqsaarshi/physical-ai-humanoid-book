import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List, Dict, Any
from .retrieval_service import RetrievalService
from .gemini_service import GeminiService
from .citation_service import CitationService
from .validation_service import ValidationService
from .prompt_service import PromptService


class RAGService:
    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.gemini_service = GeminiService()
        self.citation_service = CitationService()
        self.validation_service = ValidationService()
        self.prompt_service = PromptService()

    def retrieve_and_rerank(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant chunks for the query and rerank them
        """
        # Perform semantic retrieval
        retrieved_chunks = self.retrieval_service.semantic_retrieval(query, top_k)

        # Apply context filtering and ranking
        filtered_chunks = self.retrieval_service.context_filtering_and_ranking(
            query, retrieved_chunks, top_k
        )

        return filtered_chunks

    def generate_answer_with_context(self, query: str, mode: str = "full-book",
                                   selected_text: str = None) -> Dict[str, Any]:
        """
        Generate an answer using RAG approach
        """
        if mode == "selected-text" and selected_text:
            # Use only the selected text as context
            retrieved_chunks = self.retrieval_service.retrieve_for_selected_text_mode(selected_text, query)
        else:
            # Use full book context
            retrieved_chunks = self.retrieve_and_rerank(query)

        if not retrieved_chunks:
            return {
                "content": "I cannot answer based on the provided book content.",
                "citations": [],
                "confidence": "low"
            }

        # Extract content from chunks
        context_texts = [chunk["content"] for chunk in retrieved_chunks]

        try:
            # Generate response with context
            response_content = self.gemini_service.generate_response_with_context(query, context_texts, mode)

            # Validate the response against context
            is_valid = self.gemini_service.validate_response_against_context(response_content, context_texts)

            if not is_valid:
                response_content = "I cannot provide a reliable answer based on the provided context."

            # Create citations
            citations = self.citation_service.create_citations_from_chunks(retrieved_chunks)

        except Exception as e:
            # Fallback response when Gemini API is unavailable
            error_msg = str(e)
            if "quota" in error_msg.lower() or "429" in error_msg or "exceeded" in error_msg.lower():
                response_content = "The AI service is temporarily unavailable due to quota limits. Please try again later."
            elif "api_key" in error_msg.lower():
                response_content = "The AI service is not properly configured. Please check the API key settings."
            else:
                response_content = "I'm currently unable to process your request. The AI service may be temporarily unavailable."
            citations = []

        return {
            "content": response_content,
            "citations": citations,
            "confidence": "high" if 'citations' in locals() and citations else "low"
        }

    def validate_qdrant_collections(self, book_name: str = "002-physical-ai-robotics-textbook") -> bool:
        """
        Validate that Qdrant collections exist for the specified book
        """
        return self.retrieval_service.validate_qdrant_collections(book_name)
