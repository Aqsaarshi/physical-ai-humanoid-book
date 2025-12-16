from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from ..services.db_service import Base

class ChatConversation(Base):
    __tablename__ = "chat_conversations"
    conversation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)
    title = Column(String)
    start_time = Column(DateTime)
    last_active_time = Column(DateTime)
    messages = relationship("ChatMessage", back_populates="conversation")

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    message_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("chat_conversations.conversation_id"))
    sender = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime)
    conversation = relationship("ChatConversation", back_populates="messages")
