"""
Chat Router - Chat and Messaging Endpoints

FastAPI endpoints for chat operations:
- Send messages and get AI responses
- Get chat history

These are NEW endpoints that convert the CLI functionality to a web API.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services import ChatService
from app.database import ChatsRepository, MessagesRepository

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"]
)

# Initialize services and repositories
chat_service = ChatService()
chats_repo = ChatsRepository()
messages_repo = MessagesRepository()

# Note: user_id is passed in requests but users are managed manually in Supabase
# (Step 6: Temporary solution - no user authentication yet)


# Request/Response Models
class ChatRequest(BaseModel):
    """Request model for sending a chat message."""
    user_id: str
    message: str
    chat_id: Optional[str] = None
    chat_title: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat message."""
    message: str
    chat_id: str
    role: str = "assistant"


@router.post("/message")
async def send_message(request: ChatRequest) -> ChatResponse:
    """
    Send a message and get AI response using RAG.

    This endpoint:
    1. Creates a new chat session if chat_id is not provided
    2. Saves the user message
    3. Queries the book using RAG pipeline
    4. Saves the assistant response
    5. Returns the AI's answer

    Args:
        request: ChatRequest with user_id, message, optional chat_id and chat_title

    Returns:
        ChatResponse with AI's answer and chat_id
    """
    try:
        # Create or use existing chat session
        if not request.chat_id:
            # Create new chat session (async)
            chat_title = request.chat_title or request.message[:50]
            chat = await chats_repo.create_chat(
                user_id=request.user_id,
                title=chat_title
            )
            chat_id = chat['id']
        else:
            chat_id = request.chat_id

        # Save user message (async)
        await chat_service.save_chat_message(
            chat_id=chat_id,
            role="user",
            content=request.message
        )

        # Get conversation history (for context) (async)
        messages = await messages_repo.get_chat_messages(chat_id)
        conversation_history = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]

        # Query the book using RAG (async)
        answer = await chat_service.process_query(
            question=request.message,
            conversation_history=conversation_history
        )

        # Save assistant response (async)
        await chat_service.save_chat_message(
            chat_id=chat_id,
            role="assistant",
            content=answer
        )

        return ChatResponse(
            message=answer,
            chat_id=chat_id,
            role="assistant"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{chat_id}")
async def get_chat_history(chat_id: str) -> List[Dict]:
    """
    Get all messages in a specific chat session.

    Args:
        chat_id: ID of the chat session

    Returns:
        List of message dictionaries with role, content, and timestamp
    """
    try:
        # Get messages (async)
        messages = await messages_repo.get_chat_messages(chat_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# EXTRA ENDPOINTS - Commented out to match original requirements
# Uncomment these when needed for additional functionality
# =============================================================================

# @router.get("/chats/{user_id}")
# async def get_user_chats(user_id: str, limit: int = 10) -> List[Dict]:
#     """
#     Get all chat sessions for a specific user.
#
#     Args:
#         user_id: ID of the user
#         limit: Maximum number of chats to return (default: 10)
#
#     Returns:
#         List of chat dictionaries with metadata
#     """
#     try:
#         # Get chats (async)
#         chats = await chats_repo.get_user_chats(user_id, limit=limit)
#         return chats
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/chat/{chat_id}")
# async def get_chat_by_id(chat_id: str) -> Dict:
#     """
#     Get details of a specific chat session.
#
#     Args:
#         chat_id: ID of the chat
#
#     Returns:
#         Chat dictionary with metadata
#     """
#     try:
#         # Get chat (async)
#         chat = await chats_repo.get_chat_by_id(chat_id)
#         if not chat:
#             raise HTTPException(status_code=404, detail="Chat not found")
#         return chat
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/chat/create")
# async def create_chat(user_id: str, title: str = "New Chat") -> Dict:
#     """
#     Create a new chat session.
#
#     Args:
#         user_id: ID of the user
#         title: Title for the chat session
#
#     Returns:
#         Created chat dictionary
#     """
#     try:
#         # Create chat (async)
#         chat = await chats_repo.create_chat(user_id=user_id, title=title)
#         return chat
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
