"""
Messages Repository (Async)

Handles all database operations for the 'messages' table.

Key Changes for Async:
- All methods are now async def
- Database operations use await with asyncio.to_thread()

Source: Extracted from db_helper.py lines 221-261 (converted to async)
"""

from typing import List, Dict
from .base import get_supabase_client
import asyncio


class MessagesRepository:
    """Repository for message-related database operations (async)."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()

    async def save_message(self, chat_id: str, role: str, content: str) -> Dict:
        """
        Save a single message to the database.

        Args:
            chat_id: ID of chat this message belongs to
            role: Either 'user', 'assistant', or 'system'
            content: Message content

        Returns:
            Dict with message data including 'id'

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("messages").insert({
                    "chat_id": chat_id,
                    "role": role,
                    "content": content
                }).execute()
            )

            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in save_message: {e}")

    async def get_chat_messages(self, chat_id: str) -> List[Dict]:
        """
        Get all messages in a chat, ordered chronologically.

        Args:
            chat_id: ID of the chat

        Returns:
            List of message dicts with 'role', 'content', 'created_at'

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("messages")
                    .select("*")
                    .eq("chat_id", chat_id)
                    .order("created_at")
                    .execute()
            )
            return response.data
        except Exception as e:
            raise Exception(f"Error in get_chat_messages: {e}")
