"""
OpenAI Service (Async)

Handles all interactions with OpenAI API:
- Creating embeddings for text
- Generating chat completions

Key Changes for Async:
- Uses AsyncOpenAI for native async support
- All methods are async def with await
- Non-blocking API calls for better performance

Source: Extracted from vector_store.py lines 80-123 and chat.py lines 103-106 (converted to async)
"""

import os
from typing import List, Dict
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
EMBEDDING_MODEL = "text-embedding-ada-002"
BATCH_SIZE = 100  # Batch size for API requests to avoid rate limits


class OpenAIService:
    """Service for OpenAI API operations (async)."""

    def __init__(self):
        """Initialize async OpenAI client."""
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file.")

        # Use AsyncOpenAI for native async support
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def create_embedding(self, text: str) -> List[float]:
        """
        Create embedding for a single text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            list: Embedding vector (1536 dimensions)

        Raises:
            Exception: If embedding creation fails
        """
        try:
            # Async API call - non-blocking
            response = await self.client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error creating embedding: {str(e)}")

    async def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for multiple texts (batch processing).

        Args:
            texts: List of texts to embed

        Returns:
            list: List of embedding vectors

        Raises:
            Exception: If batch embedding creation fails
        """
        try:
            embeddings = []

            # Process batches sequentially with async calls
            for i in range(0, len(texts), BATCH_SIZE):
                batch = texts[i:i + BATCH_SIZE]
                # Async API call - non-blocking
                response = await self.client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)

            return embeddings
        except Exception as e:
            raise Exception(f"Error creating batch embeddings: {str(e)}")

    async def generate_chat_response(self, messages: List[Dict], model: str = "gpt-3.5-turbo") -> str:
        """
        Generate a chat completion response using OpenAI.

        Args:
            messages: List of message dicts with 'role' and 'content' keys
            model: OpenAI model to use (default: gpt-3.5-turbo)

        Returns:
            str: Generated response content

        Raises:
            Exception: If chat completion fails
        """
        try:
            # Async API call - non-blocking
            response = await self.client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating chat response: {str(e)}")
