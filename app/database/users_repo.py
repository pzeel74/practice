"""
Users Repository (Async)

Handles all database operations for the 'users' table.

Key Changes for Async:
- All methods are now async def
- Database operations use await
- Non-blocking I/O for better performance

Source: Extracted from db_helper.py lines 34-78 (converted to async)
"""

from typing import Optional, Dict
from .base import get_supabase_client
import asyncio


class UsersRepository:
    """Repository for user-related database operations (async)."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()

    async def get_or_create_user(self, email: str, name: str) -> Dict:
        """
        Get existing user by email, or create new one if doesn't exist.

        Args:
            email: User's email address
            name: User's name

        Returns:
            Dict with user data including 'id', 'email', 'name', 'created_at'

        Raises:
            Exception: If database operation fails
        """
        try:
            # Try to find existing user (run in thread pool for non-blocking)
            response = await asyncio.to_thread(
                lambda: self.supabase.table("users").select("*").eq("email", email).execute()
            )

            if response.data and len(response.data) > 0:
                print(f"✅ Found existing user: {email}")
                return response.data[0]

            # User doesn't exist, create new one (run in thread pool for non-blocking)
            response = await asyncio.to_thread(
                lambda: self.supabase.table("users").insert({
                    "email": email,
                    "name": name
                }).execute()
            )

            print(f"✅ Created new user: {email}")
            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in get_or_create_user: {e}")

    async def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            User dict if found, None otherwise

        Raises:
            Exception: If database operation fails
        """
        try:
            # Run in thread pool for non-blocking I/O
            response = await asyncio.to_thread(
                lambda: self.supabase.table("users").select("*").eq("email", email).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            raise Exception(f"Error in get_user_by_email: {e}")

    async def create_user(self, email: str, name: str, hashed_password: str) -> Dict:
        """
        Create a new user with hashed password.

        Args:
            email: User's email address
            name: User's name
            hashed_password: Bcrypt hashed password

        Returns:
            Dict with created user data including 'id', 'email', 'name', 'created_at'

        Raises:
            Exception: If database operation fails or email already exists
        """
        try:
            # Check if user already exists
            existing_user = await self.get_user_by_email(email)
            if existing_user:
                raise Exception(f"User with email {email} already exists")

            # Create new user
            response = await asyncio.to_thread(
                lambda: self.supabase.table("users").insert({
                    "email": email,
                    "name": name,
                    "password": hashed_password
                }).execute()
            )

            print(f"✅ Created new user: {email}")
            return response.data[0]

        except Exception as e:
            raise Exception(f"Error in create_user: {e}")
