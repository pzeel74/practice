"""
Models Layer - Data Models

This module contains Pydantic models for request/response validation and data schemas.

Pydantic models provide:
- Automatic validation of incoming data
- Type checking
- Serialization/deserialization
- API documentation (via FastAPI)

Usage:
    from app.models import UserCreate, ChatRequest

    user = UserCreate(email="test@example.com", name="Test User")
    chat = ChatRequest(user_id="123", message="Hello!")
"""

from .schemas import (
    UserCreate,
    UserResponse,
    BookUpload,
    BookResponse,
    ChatRequest,
    ChatResponse,
    MessageResponse,
)

__all__ = [
    "UserCreate",
    "UserResponse",
    "BookUpload",
    "BookResponse",
    "ChatRequest",
    "ChatResponse",
    "MessageResponse",
]
