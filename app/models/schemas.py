"""
Pydantic Schemas - Data Models

Defines all Pydantic models for request/response validation across the API.

Pydantic provides:
- Automatic validation of data types
- Serialization/deserialization
- Clear API documentation
- Type hints and IDE autocomplete

These are NEW models created for the FastAPI web API.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========================================
# USER MODELS
# ========================================

class UserCreate(BaseModel):
    """Model for creating a new user."""
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's name")


class UserResponse(BaseModel):
    """Model for user response."""
    id: str
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# BOOK MODELS
# ========================================

class BookUpload(BaseModel):
    """Model for book upload request."""
    title: Optional[str] = Field(None, description="Book title (optional, uses filename if not provided)")
    author: Optional[str] = Field(None, description="Book author (optional)")
    chunk_size: int = Field(500, ge=100, le=2000, description="Words per chunk")
    overlap_size: int = Field(50, ge=0, le=500, description="Overlap between chunks")


class BookResponse(BaseModel):
    """Model for book response."""
    id: str
    user_id: str
    title: str
    filename: str
    author: Optional[str]
    storage_path: str
    pinecone_namespace: str
    metadata: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# CHAT MODELS
# ========================================

class ChatRequest(BaseModel):
    """Model for sending a chat message."""
    user_id: str = Field(..., description="ID of the user sending the message")
    message: str = Field(..., min_length=1, max_length=5000, description="User's message/question")
    chat_id: Optional[str] = Field(None, description="Existing chat session ID (optional)")
    chat_title: Optional[str] = Field(None, description="Title for new chat (optional)")


class ChatResponse(BaseModel):
    """Model for chat message response."""
    message: str = Field(..., description="AI's response message")
    chat_id: str = Field(..., description="Chat session ID")
    role: str = Field(default="assistant", description="Message role (user/assistant)")


class ChatCreate(BaseModel):
    """Model for creating a new chat session."""
    user_id: str = Field(..., description="ID of the user")
    title: str = Field(default="New Chat", description="Chat title")


class ChatSessionResponse(BaseModel):
    """Model for chat session response."""
    id: str
    user_id: str
    title: str
    messages: List[Dict[str, str]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ========================================
# MESSAGE MODELS
# ========================================

class MessageResponse(BaseModel):
    """Model for individual message response."""
    id: str
    chat_id: str
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ========================================
# UTILITY MODELS
# ========================================

class SuccessResponse(BaseModel):
    """Generic success response model."""
    success: bool = True
    message: str
    data: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Generic error response model."""
    success: bool = False
    error: str
    detail: Optional[str] = None


class IndexStats(BaseModel):
    """Model for Pinecone index statistics."""
    total_vectors: int = Field(..., description="Total number of vectors in index")
    dimensions: int = Field(..., description="Vector dimensionality")
    index_fullness: float = Field(..., description="Index fullness (0.0 to 1.0)")
