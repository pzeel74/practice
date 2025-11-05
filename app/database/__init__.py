"""
Database Layer - Repository Pattern

This module contains all database operations using the Repository pattern.
Each repository handles operations for a single table in Supabase.

Usage:
    from app.database import UsersRepository, BooksRepository

    users_repo = UsersRepository()
    user = users_repo.get_or_create_user("test@example.com", "Test User")
"""

from .base import get_supabase_client
from .users_repo import UsersRepository
from .books_repo import BooksRepository
from .chats_repo import ChatsRepository
from .messages_repo import MessagesRepository

__all__ = [
    "get_supabase_client",
    "UsersRepository",
    "BooksRepository",
    "ChatsRepository",
    "MessagesRepository",
]
