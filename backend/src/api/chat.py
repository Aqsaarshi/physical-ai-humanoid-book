from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ..services.rag_service import RAGService
from ..services.db_service import db_service
from ..services.retrieval_service import RetrievalService
from ..repositories.chat_session_repo import ChatSessionRepository
from ..repositories.user_query_repo import UserQueryRepository
from ..repositories.ai_response_repo import AIResponseRepository

router = APIRouter()

class ChatQueryRequest(BaseModel):
    session_id: Optional[str] = None
    query: str
    context_mode: str = "full-book"  # "full-book" or "selected-text"
    selected_text: Optional[Dict[str, Any]] = None  # Contains 'text' and 'source_metadata'

class ChatQueryResponse(BaseModel):
    response_id: str
    content: str
    citations: List[Dict[str, str]]

def get_db():
    db_gen = db_service.get_db()
    db = next(db_gen)
    try:
        yield db
    finally:
        db.close()

@router.post("/query")
def chat_query(request: ChatQueryRequest, db: Session = Depends(get_db)):
    rag_service = RAGService()
    session_repo = ChatSessionRepository(db)
    query_repo = UserQueryRepository(db)
    response_repo = AIResponseRepository(db)

    # Get or create session
    if request.session_id:
        try:
            session_uuid = uuid.UUID(request.session_id)
        except ValueError:
            session = session_repo.create_session(current_mode=request.context_mode)
        else:
            session = session_repo.get_session(session_uuid)
            if not session:
                session = session_repo.create_session(current_mode=request.context_mode)
    else:
        session = session_repo.create_session(current_mode=request.context_mode)

    # Safely get selected text and source metadata
    selected_text_content = None
    source_metadata = {}
    if request.selected_text:
        selected_text_content = request.selected_text.get("text", "")
        source_metadata = request.selected_text.get("source_metadata", {})

    # Create user query
    user_query = query_repo.create_query(
        session_id=session.session_id,
        content=request.query,
        context_mode=request.context_mode,
        selected_text=selected_text_content,
        source_metadata=source_metadata
    )

    # Generate response
    try:
        if request.context_mode == "selected-text" and selected_text_content:
            # Use the selected text directly as context (no paragraph retrieval available)
            # The rag_service will handle the selected-text mode
            response_data = rag_service.generate_answer_with_context(
                request.query,
                mode="selected-text",
                selected_text=selected_text_content
            )
        else:
            # Full-book context
            try:
                response_data = rag_service.generate_answer_with_context(
                    request.query,
                    mode="full-book"
                )
            except Exception as e:
                # Fallback to selected-text if full-book fails
                if selected_text_content:
                    response_data = rag_service.generate_answer_with_context(
                        request.query,
                        mode="selected-text",
                        selected_text=selected_text_content
                    )
                else:
                    # Check for specific error types
                    error_msg = str(e)
                    if "quota" in error_msg.lower() or "429" in error_msg or "exceeded" in error_msg.lower():
                        response_data = {
                            "content": "The AI service is temporarily unavailable due to quota limits. Please try again later.",
                            "citations": [],
                            "confidence": "low"
                        }
                    elif "api_key" in error_msg.lower():
                        response_data = {
                            "content": "The AI service is not properly configured. Please check the API key settings.",
                            "citations": [],
                            "confidence": "low"
                        }
                    else:
                        response_data = {
                            "content": f"I encountered an issue processing your request. Error: {str(e)}",
                            "citations": [],
                            "confidence": "low"
                        }
    except Exception as e:
        # Check for specific error types
        error_msg = str(e)
        if "quota" in error_msg.lower() or "429" in error_msg:
            response_data = {
                "content": "The AI service is temporarily unavailable due to quota limits. Please try again later.",
                "citations": [],
                "confidence": "low"
            }
        elif "api_key" in error_msg.lower():
            response_data = {
                "content": "The AI service is not properly configured. Please check the API key settings.",
                "citations": [],
                "confidence": "low"
            }
        else:
            response_data = {
                "content": f"Sorry, I encountered an error: {str(e)}",
                "citations": [],
                "confidence": "low"
            }

    # Store AI response
    ai_response = response_repo.create_response(
        session_id=session.session_id,
        query_id=user_query.query_id,
        content=response_data["content"],
        citations=response_data.get("citations", [])
    )

    return ChatQueryResponse(
        response_id=str(uuid.uuid4()),
        content=response_data["content"],
        citations=response_data.get("citations", [])
    )

@router.get("/history/{session_id}")
def get_chat_history(session_id: str, db: Session = Depends(get_db)):
    session_repo = ChatSessionRepository(db)
    query_repo = UserQueryRepository(db)
    response_repo = AIResponseRepository(db)

    session_uuid = uuid.UUID(session_id)
    session = session_repo.get_session(session_uuid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all queries and responses
    queries = query_repo.get_queries_by_session(session_uuid)
    responses = response_repo.get_responses_by_session(session_uuid)

    messages = []
    for query in queries:
        messages.append({
            "message_id": str(query.query_id),
            "content": query.content,
            "sender": "user",
            "timestamp": query.timestamp.isoformat(),
            "citations": []
        })

    for response in responses:
        messages.append({
            "message_id": str(response.response_id),
            "content": response.content,
            "sender": "bot",
            "timestamp": response.timestamp.isoformat(),
            "citations": response.citations or []
        })

    messages.sort(key=lambda x: x["timestamp"])
    return messages
