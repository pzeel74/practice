"""
Books Router - Book Management Endpoints

FastAPI endpoints for book operations:
- Upload and process books

These are NEW endpoints that convert the CLI functionality to a web API.
"""

import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Dict
from app.services import ChatService
from app.database import BooksRepository

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/v1/books",
    tags=["books"]
)

# Initialize services and repositories
chat_service = ChatService()
books_repo = BooksRepository()

# Note: user_id is passed in requests but users are managed manually in Supabase
# (Step 6: Temporary solution - no user authentication yet)


@router.post("/upload")
async def upload_book(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    title: str = Form(None),
    author: str = Form(None),
    chunk_size: int = Form(500),
    overlap_size: int = Form(50)
) -> Dict:
    """
    Upload and process a book file (.txt or .pdf).

    This endpoint:
    1. Saves the uploaded file to temp/ directory
    2. Processes the book into chunks
    3. Creates embeddings
    4. Stores vectors in Pinecone
    5. Saves book metadata to Supabase

    Args:
        file: Book file (.txt or .pdf)
        user_id: ID of the user uploading the book
        title: Book title (optional, uses filename if not provided)
        author: Book author (optional)
        chunk_size: Number of words per chunk (default: 500)
        overlap_size: Overlap between chunks (default: 50)

    Returns:
        Dict with book metadata and processing results
    """
    try:
        # Validate file type
        if not file.filename.endswith(('.txt', '.pdf')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only .txt and .pdf files are supported."
            )

        # Create temp directory if it doesn't exist
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)

        # Save uploaded file
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process and store book (async)
        num_chunks = await chat_service.load_and_store_book(
            book_path=file_path,
            chunk_size=chunk_size,
            overlap_size=overlap_size
        )

        # Save book metadata to database (async)
        book_title = title or file.filename
        book_data = await books_repo.save_book(
            user_id=user_id,
            title=book_title,
            filename=file.filename,
            storage_path=file_path,
            author=author,
            metadata={
                "chunks_count": num_chunks,
                "chunk_size": chunk_size,
                "overlap_size": overlap_size
            }
        )

        return {
            "success": True,
            "message": f"Book processed successfully! {num_chunks} chunks stored.",
            "book": book_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# EXTRA ENDPOINTS - Commented out to match original requirements
# Uncomment these when needed for additional functionality
# =============================================================================

# @router.get("/{user_id}")
# async def get_user_books(user_id: str) -> List[Dict]:
#     """
#     Get all books uploaded by a specific user.
#
#     Args:
#         user_id: ID of the user
#
#     Returns:
#         List of book dictionaries with metadata
#     """
#     try:
#         # Get user books (async)
#         books = await books_repo.get_user_books(user_id)
#         return books
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/stats/index")
# async def get_index_stats() -> Dict:
#     """
#     Get statistics about the Pinecone vector index.
#
#     Returns:
#         Dict with index statistics (vector count, dimensions, etc.)
#     """
#     try:
#         # Get stats (async)
#         stats = await chat_service.get_index_stats()
#         return {
#             "total_vectors": stats.total_vector_count if hasattr(stats, 'total_vector_count') else 0,
#             "dimensions": stats.dimension if hasattr(stats, 'dimension') else 1536,
#             "index_fullness": stats.index_fullness if hasattr(stats, 'index_fullness') else 0
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.delete("/clear")
# async def clear_vector_database() -> Dict:
#     """
#     Delete all vectors from the Pinecone index.
#     Use this to reset the database before uploading a new book.
#
#     Returns:
#         Dict with success message
#     """
#     try:
#         # Clear database (async)
#         await chat_service.clear_vector_database()
#         return {
#             "success": True,
#             "message": "All vectors deleted from index."
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
