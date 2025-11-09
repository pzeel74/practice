"""
Routers Layer - API Endpoints

This module contains all FastAPI routers (API endpoints) for the application.

Routers are organized by domain:
- users: User authentication endpoints (register, login)
- books: Book upload and management endpoints
- chat: Chat and messaging endpoints

Usage in main.py:
    from app.routers import users_router, books_router, chat_router

    app.include_router(users_router)
    app.include_router(books_router)
    app.include_router(chat_router)
"""

from .users import router as users_router
from .books import router as books_router
from .chat import router as chat_router

__all__ = [
    "users_router",
    "books_router",
    "chat_router",
]
