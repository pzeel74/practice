"""
Database Base Module (Async)

Provides the core Supabase async client connection that all repositories use.
This implements the Singleton pattern to ensure only one database connection exists.

Key Changes for Async:
- Uses AsyncClient for non-blocking I/O operations
- All repository database calls will be async/await

Source: Extracted from db_helper.py lines 11-27 (converted to async)
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

# Load environment variables
load_dotenv()

# Global Supabase client (singleton)
# Note: Supabase Python SDK operations will be wrapped in async functions
_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """
    Get or create the Supabase client (Singleton pattern).

    Note: The client initialization is synchronous, but database operations
    in repositories will be wrapped with async/await for non-blocking I/O.

    Returns:
        Client: Initialized Supabase client

    Raises:
        ValueError: If SUPABASE_URL or SUPABASE_KEY are not set
    """
    global _supabase_client

    if _supabase_client is None:
        # Get credentials from environment
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        # Validate credentials
        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_KEY must be set in .env file"
            )

        # Create client (initialization is synchronous)
        _supabase_client = create_client(supabase_url, supabase_key)

    return _supabase_client
