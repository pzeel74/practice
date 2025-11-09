"""
Services Layer - Business Logic

This module contains all business logic services that orchestrate
between repositories and external APIs (OpenAI, Pinecone).

Services are responsible for:
- Coordinating multiple repository operations
- Calling external APIs
- Implementing core business logic (RAG pipeline)
- Data transformation and processing

Usage:
    from app.services import ChatService, OpenAIService

    chat_service = ChatService()
    answer = chat_service.process_query("What is this book about?", [])
"""

from .openai_service import OpenAIService
from .pinecone_service import PineconeService
from .book_processing_service import BookProcessingService
from .chat_service import ChatService
from .auth_service import AuthService

__all__ = [
    "OpenAIService",
    "PineconeService",
    "BookProcessingService",
    "ChatService",
    "AuthService",
]
