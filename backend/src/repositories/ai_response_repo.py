import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.ai_response import AIResponse
from ..models.user_query import UserQuery
import uuid


class AIResponseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_response(self, session_id: uuid.UUID, query_id: uuid.UUID, content: str,
                        citations: list = None, confidence_level: str = None) -> AIResponse:
        """
        Create a new AI response
        """
        response = AIResponse(
            session_id=session_id,
            query_id=query_id,
            content=content,
            citations=citations,
            confidence_level=confidence_level
        )
        self.db.add(response)
        self.db.commit()
        self.db.refresh(response)
        return response

    def get_response(self, response_id: uuid.UUID) -> Optional[AIResponse]:
        """
        Get an AI response by ID
        """
        return self.db.query(AIResponse).filter(AIResponse.response_id == response_id).first()

    def get_responses_by_session(self, session_id: uuid.UUID) -> List[AIResponse]:
        """
        Get all responses for a specific session
        """
        return self.db.query(AIResponse).filter(
            AIResponse.session_id == session_id
        ).order_by(AIResponse.timestamp).all()

    def get_responses_by_query(self, query_id: uuid.UUID) -> List[AIResponse]:
        """
        Get all responses for a specific query
        """
        return self.db.query(AIResponse).filter(
            AIResponse.query_id == query_id
        ).order_by(AIResponse.timestamp).all()

    def get_latest_response_for_session(self, session_id: uuid.UUID) -> Optional[AIResponse]:
        """
        Get the most recent response for a session
        """
        return self.db.query(AIResponse).filter(
            AIResponse.session_id == session_id
        ).order_by(AIResponse.timestamp.desc()).first()