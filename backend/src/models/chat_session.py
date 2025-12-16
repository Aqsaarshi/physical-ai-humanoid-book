import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..services.db_service import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_context = Column(String, nullable=True)
    current_mode = Column(Enum("full-book", "selected-text", name="chat_mode_enum"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    queries = relationship("UserQuery", order_by="UserQuery.timestamp", back_populates="session", cascade="all, delete-orphan")
    responses = relationship("AIResponse", back_populates="session", cascade="all, delete-orphan")