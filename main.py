"""
RAG Chat Backend - FastAPI Application

Main entry point for the RAG (Retrieval-Augmented Generation) Chat Backend API.

Run the application:
    python main.py
"""

from fastapi import FastAPI
from app.routers import users_router, books_router, chat_router

# =============================================================================
# STEP 5 REQUIREMENT 1: Initialize FastAPI app
# =============================================================================
app = FastAPI()


# =============================================================================
# STEP 5 REQUIREMENT 2: Include all routers
# =============================================================================
app.include_router(users_router)
app.include_router(books_router)
app.include_router(chat_router)


# =============================================================================
# STEP 5 REQUIREMENT 3: Add root endpoint to test if API is running
# =============================================================================
@app.get("/")
async def root():
    """Root endpoint - Test if API is running."""
    return {"message": "API is running"}


# =============================================================================
# STEP 5 REQUIREMENT 4: Add uvicorn configuration to run the server
# =============================================================================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# =============================================================================
# EXTRA FEATURES - Commented out to match original requirements
# Uncomment these when needed for production
# =============================================================================

# # CORS Middleware - Uncomment when you add a frontend
# from fastapi.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # In production, replace with specific origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Logging Setup - Uncomment for better debugging
# from app.utils import setup_application_logging
# import logging
# setup_application_logging(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Health Check Endpoint - Uncomment for production monitoring
# @app.get("/health")
# async def health_check():
#     """Health check endpoint for monitoring."""
#     return {
#         "status": "healthy",
#         "service": "rag-chat-backend"
#     }

# # Startup Event - Uncomment for initialization tasks
# @app.on_event("startup")
# async def startup_event():
#     """Execute on application startup."""
#     logger.info("🚀 RAG Chat Backend is starting up...")
#     logger.info("📚 Ready to process books and chat!")

# # Shutdown Event - Uncomment for cleanup tasks
# @app.on_event("shutdown")
# async def shutdown_event():
#     """Execute on application shutdown."""
#     logger.info("👋 RAG Chat Backend is shutting down...")

# # Enhanced App Metadata - Uncomment for better documentation
# app = FastAPI(
#     title="RAG Chat Backend",
#     description="A Retrieval-Augmented Generation (RAG) chat backend for chatting with books using AI",
#     version="1.0.0",
#     docs_url="/docs",
#     redoc_url="/redoc",
# )
