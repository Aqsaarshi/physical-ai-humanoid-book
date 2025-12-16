import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.user_query import UserQuery
from ..models.chat_session import ChatSession
import uuid


class UserQueryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_query(self, session_id: uuid.UUID, content: str, context_mode: str,
                     selected_text: str = None, source_metadata: dict = None) -> UserQuery:
        """
        Create a new user query
        """
        query = UserQuery(
            session_id=session_id,
            content=content,
            context_mode=context_mode,
            selected_text=selected_text,
            source_metadata=source_metadata
        )
        self.db.add(query)
        self.db.commit()
        self.db.refresh(query)
        return query

    def get_query(self, query_id: uuid.UUID) -> Optional[UserQuery]:
        """
        Get a user query by ID
        """
        return self.db.query(UserQuery).filter(UserQuery.query_id == query_id).first()

    def get_queries_by_session(self, session_id: uuid.UUID) -> List[UserQuery]:
        """
        Get all queries for a specific session
        """
        return self.db.query(UserQuery).filter(
            UserQuery.session_id == session_id
        ).order_by(UserQuery.timestamp).all()

    def get_latest_query_for_session(self, session_id: uuid.UUID) -> Optional[UserQuery]:
        """
        Get the most recent query for a session
        """
        return self.db.query(UserQuery).filter(
            UserQuery.session_id == session_id
        ).order_by(UserQuery.timestamp.desc()).first()