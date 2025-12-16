from sqlalchemy.orm import Session
from models.chat import ChatConversation, ChatMessage
from datetime import datetime

class ChatHistoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, title: str = None, user_id: str = None):
        conversation = ChatConversation(
            title=title,
            user_id=user_id,
            start_time=datetime.utcnow(),
            last_active_time=datetime.utcnow()
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation(self, conversation_id):
        return self.db.query(ChatConversation).filter_by(conversation_id=conversation_id).first()

    def create_message(self, conversation_id, sender, content):
        message = ChatMessage(
            conversation_id=conversation_id,
            sender=sender,
            content=content
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_for_conversation(self, conversation_id):
        return self.db.query(ChatMessage).filter_by(conversation_id=conversation_id).all()

    def get_conversations(self):
        return self.db.query(ChatConversation).all()
