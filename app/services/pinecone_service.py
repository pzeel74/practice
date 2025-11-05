"""
Pinecone Service (Async)

Handles all interactions with Pinecone vector database:
- Creating and connecting to indexes
- Storing vectors with metadata
- Searching for similar vectors
- Index management

Key Changes for Async:
- All methods are async def
- Uses asyncio.to_thread() for non-blocking I/O
- Pinecone SDK is synchronous, so we wrap calls in thread pool

Note: This service does NOT create embeddings - it receives pre-computed
embeddings from OpenAIService. This follows separation of concerns.

Source: Extracted from vector_store.py (Pinecone-specific code only, converted to async)
"""

import os
import asyncio
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
EMBEDDING_DIMENSION = 1536
INDEX_NAME = "book-chat"
BATCH_SIZE = 100  # Batch size for upsert operations


class PineconeService:
    """Service for Pinecone vector database operations (async)."""

    def __init__(self):
        """Initialize Pinecone client."""
        self.api_key = os.getenv("PINECONE_API_KEY")

        if not self.api_key or self.api_key == "your_pinecone_api_key_here":
            raise ValueError(
                "PINECONE_API_KEY not found or not set in .env file. "
                "Please add your Pinecone API key."
            )

        self.pc = Pinecone(api_key=self.api_key)
        self.index = None

    async def _ensure_index(self):
        """Ensure index is connected, connect if not."""
        if not self.index:
            await self.create_or_connect_index()

    async def create_or_connect_index(self):
        """
        Create a new Pinecone index or connect to existing one.

        Returns:
            Pinecone Index object

        Raises:
            Exception: If index creation/connection fails
        """
        try:
            # Check if index already exists (run in thread pool)
            existing_indexes = await asyncio.to_thread(
                lambda: [index.name for index in self.pc.list_indexes()]
            )

            if INDEX_NAME not in existing_indexes:
                print(f"Creating new Pinecone index: {INDEX_NAME}")
                # Create new index (run in thread pool)
                await asyncio.to_thread(
                    lambda: self.pc.create_index(
                        name=INDEX_NAME,
                        dimension=EMBEDDING_DIMENSION,
                        metric="cosine",
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                )
                print(f"Index '{INDEX_NAME}' created successfully!")
            else:
                print(f"Connecting to existing index: {INDEX_NAME}")

            # Connect to index
            self.index = self.pc.Index(INDEX_NAME)
            return self.index

        except Exception as e:
            raise Exception(f"Error creating/connecting to Pinecone index: {str(e)}")

    async def store_vectors(self, vectors: List[Dict[str, Any]]) -> int:
        """
        Store vectors with their embeddings and metadata in Pinecone.

        Args:
            vectors: List of dicts with 'id', 'values' (embedding), and 'metadata'

        Returns:
            int: Number of vectors stored

        Raises:
            Exception: If storage fails
        """
        await self._ensure_index()

        try:
            print(f"Storing {len(vectors)} vectors in Pinecone...")

            # Upsert to Pinecone in batches (run in thread pool for non-blocking I/O)
            for i in range(0, len(vectors), BATCH_SIZE):
                batch = vectors[i:i + BATCH_SIZE]
                await asyncio.to_thread(lambda b=batch: self.index.upsert(vectors=b))

            print(f"Successfully stored {len(vectors)} vectors in Pinecone!")
            return len(vectors)

        except Exception as e:
            raise Exception(f"Error storing vectors in Pinecone: {str(e)}")

    async def search_vectors(self, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
        """
        Search for most similar vectors to a query embedding.

        Args:
            query_embedding: The embedding vector to search for
            top_k: Number of top results to return (default: 3)

        Returns:
            list: List of dictionaries with 'id', 'text', and 'score' keys

        Raises:
            Exception: If search fails
        """
        await self._ensure_index()

        try:
            # Search in Pinecone (run in thread pool for non-blocking I/O)
            results = await asyncio.to_thread(
                lambda: self.index.query(
                    vector=query_embedding,
                    top_k=top_k,
                    include_metadata=True
                )
            )

            # Extract and format results
            similar_chunks = []
            for match in results.matches:
                similar_chunks.append({
                    'id': match.id,
                    'text': match.metadata['text'],
                    'score': match.score
                })

            return similar_chunks

        except Exception as e:
            raise Exception(f"Error searching similar vectors: {str(e)}")

    async def get_index_stats(self) -> Any:
        """
        Get statistics about the current index.

        Returns:
            Pinecone index statistics object

        Raises:
            Exception: If stats retrieval fails
        """
        await self._ensure_index()

        try:
            # Get stats (run in thread pool for non-blocking I/O)
            stats = await asyncio.to_thread(lambda: self.index.describe_index_stats())
            return stats
        except Exception as e:
            raise Exception(f"Error getting index stats: {str(e)}")

    async def delete_all_vectors(self):
        """
        Delete all vectors from the index (useful for resetting).

        Raises:
            Exception: If deletion fails
        """
        await self._ensure_index()

        try:
            # Delete all (run in thread pool for non-blocking I/O)
            await asyncio.to_thread(lambda: self.index.delete(delete_all=True))
            print("All vectors deleted from index.")
        except Exception as e:
            raise Exception(f"Error deleting vectors: {str(e)}")
