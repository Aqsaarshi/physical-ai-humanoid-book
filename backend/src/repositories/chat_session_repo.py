import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from typing import Optional
from ..models.chat_session import ChatSession
from ..models.user_query import UserQuery
from ..models.ai_response import AIResponse
import uuid


class ChatSessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, user_context: str = None, current_mode: str = "full-book") -> ChatSession:
        """
        Create a new chat session
        """
        session = ChatSession(
            user_context=user_context,
            current_mode=current_mode
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session(self, session_id: uuid.UUID) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        """
        return self.db.query(ChatSession).filter(ChatSession.session_id == session_id).first()

    def update_session_mode(self, session_id: uuid.UUID, new_mode: str) -> Optional[ChatSession]:
        """
        Update the mode of a chat session
        """
        session = self.get_session(session_id)
        if session:
            session.current_mode = new_mode
            self.db.commit()
            self.db.refresh(session)
        return session

    def delete_session(self, session_id: uuid.UUID) -> bool:
        """
        Delete a chat session and all its related queries and responses
        """
        session = self.get_session(session_id)
        if session:
            # Delete all related queries and responses (due to cascade, this might be automatic)
            self.db.delete(session)
            self.db.commit()
            return True
        return False