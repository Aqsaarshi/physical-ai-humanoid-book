import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qdrant_client import QdrantClient
from qdrant_client.http import models
from typing import List, Dict, Any, Optional
from ..config import settings


class QdrantService:
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            prefer_grpc=True
        )
        self.collection_name = "book_content"

    def validate_collection(self, book_name: str = "002-physical-ai-robotics-textbook") -> bool:
        """
        Validate that the Qdrant collection exists for the specified book
        """
        try:
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)
            return collection_exists
        except Exception as e:
            raise Exception(f"Error validating Qdrant collection: {str(e)}")

    def search_similar(self, query_vector: List[float], limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar content in the Qdrant collection
        """
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit
            )

            return [
                {
                    "content": point.payload.get("content", ""),
                    "metadata": point.payload.get("metadata", {}),
                    "score": point.score
                }
                for point in results
            ]
        except Exception as e:
            raise Exception(f"Error searching in Qdrant: {str(e)}")

    def upsert_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None) -> bool:
        """
        Upsert a document into the Qdrant collection
        """
        try:
            from .retrieval_service import RetrievalService
            # Generate embedding for the content
            retrieval_service = RetrievalService()
            embedding = retrieval_service.generate_embedding(content)

            # Prepare the payload
            payload = {
                "content": content,
                "metadata": metadata or {}
            }

            # Upsert the document
            self.client.upsert(
                collection_name=self.collection_name,
                points=[models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload=payload
                )]
            )
            return True
        except Exception as e:
            raise Exception(f"Error upserting document to Qdrant: {str(e)}")

    def get_all_books(self) -> List[str]:
        """
        Get list of all books available in the Qdrant collection
        """
        try:
            # This would depend on how books are indexed in your collection
            # For now, returning a placeholder list
            return ["002-physical-ai-robotics-textbook"]
        except Exception as e:
            raise Exception(f"Error getting books from Qdrant: {str(e)}")
