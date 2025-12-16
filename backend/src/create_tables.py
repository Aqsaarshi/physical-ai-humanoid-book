import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.db_service import Base, db_service
from models.chat_session import ChatSession
from models.user_query import UserQuery
from models.ai_response import AIResponse
from models.chat import ChatConversation, ChatMessage

# Get the engine from the database service instance
engine = db_service.get_engine()

# Create tables
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
