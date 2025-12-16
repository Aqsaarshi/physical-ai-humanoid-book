import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..services.db_service import Base


class AIResponse(Base):
    __tablename__ = "ai_responses"

    response_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.session_id"), nullable=False)
    query_id = Column(UUID(as_uuid=True), ForeignKey("user_queries.query_id"), nullable=False)  # Link to the query that generated this response
    content = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True)  # List of citation objects
    confidence_level = Column(String, nullable=True)  # "high", "medium", "low"
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    session = relationship("ChatSession", back_populates="responses")
    query = relationship("UserQuery")  # The query that this response answers