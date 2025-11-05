"""
Books Repository (Async)

Handles all database operations for the 'books' table.

Key Changes for Async:
- All methods are now async def
- Database operations use await with asyncio.to_thread()

Source: Extracted from db_helper.py lines 84-132 (converted to async)
"""

from typing import Optional, List, Dict
from .base import get_supabase_client
import asyncio


class BooksRepository:
    """Repository for book-related database operations (async)."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()

    async def save_book(
        self,
        user_id: str,
        title: str,
        filename: str,
        storage_path: str,
        author: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Save book metadata to database.

        Args:
            user_id: ID of user who uploaded the book
            title: Book title
            filename: Original filename
            storage_path: Path where book file is stored
            author: Book author (optional)
            metadata: Additional metadata like pages, word count (optional)

        Returns:
            Dict with book data including 'id'

        Raises:
            Exception: If database operation fails
        """
        try:
            # Create unique Pinecone namespace for this book
            pinecone_namespace = f"{user_id}-{filename.replace('.', '-').replace(' ', '-').lower()}"

            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("books").insert({
                    "user_id": user_id,
                    "title": title,
                    "filename": filename,
                    "storage_path": storage_path,
                    "author": author,
                    "metadata": metadata or {},
                    "pinecone_namespace": pinecone_namespace
                }).execute()
            )

            print(f"✅ Book saved to database: {title}")
            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in save_book: {e}")

    async def get_user_books(self, user_id: str) -> List[Dict]:
        """
        Get all books uploaded by a user.

        Args:
            user_id: ID of user

        Returns:
            List of book dicts

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run database operation in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("books").select("*").eq("user_id", user_id).execute()
            )
            return response.data
        except Exception as e:
            raise Exception(f"Error in get_user_books: {e}")
