import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import List, Dict, Any
from .qdrant_service import QdrantService


class CitationService:
    def __init__(self):
        self.qdrant_service = QdrantService()

    def create_citations_from_chunks(self, retrieved_chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Create citation objects from retrieved chunks
        """
        citations = []
        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {})
            citation = {
                "chapter": metadata.get("chapter", "Unknown"),
                "section": metadata.get("section", "Unknown"),
                "score": str(chunk.get("score", 0.0))
            }
            citations.append(citation)
        return citations

    def format_citations(self, citations: List[Dict[str, str]]) -> str:
        """
        Format citations for display in the response
        """
        if not citations:
            return ""

        formatted = "Sources:\n"
        for i, citation in enumerate(citations, 1):
            formatted += f"{i}. Chapter: {citation['chapter']}, Section: {citation['section']}\n"
        return formatted

    def package_context_with_citations(self, retrieved_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Package context content with associated citations
        """
        content = [chunk["content"] for chunk in retrieved_chunks]
        citations = self.create_citations_from_chunks(retrieved_chunks)

        return {
            "content": content,
            "citations": citations
        }
