"""
Chats Repository (Async)

Handles all database operations for the 'chats' table.

Key Changes for Async:
- All methods are now async def
- Database operations use await with asyncio.to_thread()

Source: Extracted from db_helper.py lines 139-214 and 264-285 (converted to async)
"""

from typing import Optional, List, Dict
from datetime import datetime
from .base import get_supabase_client
import asyncio


class ChatsRepository:
    """Repository for chat-related database operations (async)."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()

    async def create_chat(self, user_id: str, title: str = "New Chat") -> Dict:
        """
        Create a new chat session.

        Args:
            user_id: ID of user who owns this chat
            title: Chat title (usually first question)

        Returns:
            Dict with chat data including 'id'

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("chats").insert({
                    "user_id": user_id,
                    "title": title,
                    "messages": []
                }).execute()
            )

            print(f"✅ Chat created: {title}")
            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in create_chat: {e}")

    async def get_user_chats(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Get user's recent chats, ordered by most recent first.

        Args:
            user_id: ID of user
            limit: Maximum number of chats to return

        Returns:
            List of chat dicts

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("chats")
                    .select("*")
                    .eq("user_id", user_id)
                    .order("updated_at", desc=True)
                    .limit(limit)
                    .execute()
            )
            return response.data
        except Exception as e:
            raise Exception(f"Error in get_user_chats: {e}")

    async def get_chat_by_id(self, chat_id: str) -> Optional[Dict]:
        """
        Get a specific chat by ID.

        Args:
            chat_id: ID of the chat

        Returns:
            Chat dict if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("chats").select("*").eq("id", chat_id).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error in get_chat_by_id: {e}")

    async def update_chat_title(self, chat_id: str, title: str) -> Dict:
        """
        Update chat title (typically set from first question).

        Args:
            chat_id: ID of the chat
            title: New title

        Returns:
            Updated chat dict

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("chats").update({
                    "title": title
                }).eq("id", chat_id).execute()
            )
            return response.data[0]
        except Exception as e:
            raise Exception(f"Error in update_chat_title: {e}")

    async def save_conversation_to_jsonb(self, chat_id: str, messages: List[Dict]) -> Dict:
        """
        Save entire conversation to JSONB field in chats table.
        This provides a backup/snapshot of the conversation.

        Args:
            chat_id: ID of chat
            messages: List of message dicts with 'role' and 'content'

        Returns:
            Updated chat dict

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("chats").update({
                    "messages": messages,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("id", chat_id).execute()
            )

            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in save_conversation_to_jsonb: {e}")
