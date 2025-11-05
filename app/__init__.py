"""
RAG Chat Backend Application Package

This package contains the complete RAG (Retrieval-Augmented Generation) chat backend
organized into clean, layered architecture:

- database: Data access layer (Supabase repositories)
- services: Business logic layer (OpenAI, Pinecone, chat orchestration)
- routers: API endpoint layer (FastAPI routes)
- models: Data models (Pydantic schemas)
- utils: Helper utilities (logging, etc.)
"""

__version__ = "1.0.0"
__author__ = "Your Name"
