"""
Chat Service - RAG Orchestrator (Async)

This is the core business logic service that orchestrates the entire RAG
(Retrieval-Augmented Generation) pipeline:

1. Process books → chunks
2. Create embeddings → OpenAI
3. Store vectors → Pinecone
4. Search similar chunks → Pinecone
5. Generate responses → OpenAI
6. Save chat history → Supabase

Key Changes for Async:
- All methods are async def
- Awaits all async service and repository calls
- True non-blocking RAG pipeline!

This service coordinates between all other services and repositories.

Source: Extracted from chat.py query_book() function and orchestration logic (converted to async)
"""

from typing import List, Dict, Optional
from .openai_service import OpenAIService
from .pinecone_service import PineconeService
from .book_processing_service import BookProcessingService
from app.database import MessagesRepository, ChatsRepository


class ChatService:
    """Main RAG orchestration service (async)."""

    def __init__(self):
        """Initialize all required services and repositories."""
        self.openai_service = OpenAIService()
        self.pinecone_service = PineconeService()
        self.book_service = BookProcessingService()
        self.messages_repo = MessagesRepository()
        self.chats_repo = ChatsRepository()

    async def process_query(
        self,
        question: str,
        conversation_history: List[Dict],
        top_k: int = 3
    ) -> str:
        """
        Answer a question using RAG (Retrieval-Augmented Generation).

        This is the core RAG pipeline:
        1. Create embedding for the question
        2. Search for similar chunks in Pinecone
        3. Build context from retrieved chunks
        4. Generate answer using OpenAI with context

        Args:
            question: User's question
            conversation_history: List of conversation messages
            top_k: Number of similar chunks to retrieve (default: 3)

        Returns:
            str: AI's answer based on book content

        Raises:
            Exception: If any step of the pipeline fails
        """
        try:
            # Step 1: Create embedding for the question (async)
            query_embedding = await self.openai_service.create_embedding(question)

            # Step 2: Search for similar chunks in Pinecone (async)
            similar_chunks = await self.pinecone_service.search_vectors(
                query_embedding=query_embedding,
                top_k=top_k
            )

            if not similar_chunks:
                return "I couldn't find relevant information in the book to answer your question."

            # Step 3: Build context from retrieved chunks
            context = "\n\n".join([
                f"[Source {i+1}]:\n{chunk['text']}"
                for i, chunk in enumerate(similar_chunks)
            ])

            # Step 4: Create system message with context
            system_message = {
                "role": "system",
                "content": f"""You are a helpful assistant that answers questions based ONLY on the provided book content.

Book Context:
{context}

Instructions:
- Answer the question using ONLY the information from the context above
- If the context doesn't contain enough information to answer, say so
- Be specific and cite which source you're using when possible
- Do not make up information not present in the context"""
            }

            # Create messages list with system message first
            messages = [system_message] + conversation_history

            # Step 5: Generate response using OpenAI (async)
            answer = await self.openai_service.generate_chat_response(messages)

            return answer

        except Exception as e:
            return f"Error querying book: {e}"

    async def load_and_store_book(
        self,
        book_path: str,
        chunk_size: int = 500,
        overlap_size: int = 50
    ) -> int:
        """
        Complete pipeline to load a book and store it in the vector database.

        Args:
            book_path: Path to the book file (.txt or .pdf)
            chunk_size: Target number of words per chunk (default: 500)
            overlap_size: Number of words to overlap between chunks (default: 50)

        Returns:
            int: Number of chunks stored

        Raises:
            Exception: If processing or storage fails
        """
        try:
            # Step 1: Process book into chunks (async file I/O)
            print("\n" + "="*50)
            print("Processing Book")
            print("="*50)

            chunks = await self.book_service.process_book(
                file_path=book_path,
                chunk_size=chunk_size,
                overlap_size=overlap_size
            )

            # Step 2: Create embeddings for all chunks (async)
            print(f"Creating embeddings for {len(chunks)} chunks...")
            texts = [chunk['text'] for chunk in chunks]
            embeddings = await self.openai_service.create_embeddings_batch(texts)

            # Step 3: Prepare vectors for Pinecone
            vectors = []
            for i, chunk in enumerate(chunks):
                vectors.append({
                    'id': chunk['id'],
                    'values': embeddings[i],
                    'metadata': {
                        'text': chunk['text']
                    }
                })

            # Step 4: Store in Pinecone (async)
            num_stored = await self.pinecone_service.store_vectors(vectors)

            print("="*50)
            print(f"Book processed successfully! {num_stored} chunks stored.")
            print("="*50 + "\n")

            return num_stored

        except Exception as e:
            raise Exception(f"Error loading and storing book: {e}")

    async def save_chat_message(
        self,
        chat_id: str,
        role: str,
        content: str
    ) -> Optional[Dict]:
        """
        Save a message to the database.

        Args:
            chat_id: ID of the current chat session
            role: Either 'user' or 'assistant'
            content: The message content

        Returns:
            Dict with message data, or None if save fails
        """
        try:
            # Save message to database (async)
            return await self.messages_repo.save_message(chat_id, role, content)
        except Exception as e:
            # Don't break the conversation if database save fails
            print(f"⚠️ Warning: Could not save message to database: {e}")
            return None

    async def get_index_stats(self) -> Dict:
        """
        Get statistics about the vector index.

        Returns:
            Dict with index statistics including vector count
        """
        # Get index stats (async)
        return await self.pinecone_service.get_index_stats()

    async def clear_vector_database(self):
        """
        Delete all vectors from the Pinecone index.
        Useful for resetting or loading a new book.
        """
        # Delete all vectors (async)
        await self.pinecone_service.delete_all_vectors()
