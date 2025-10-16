import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
EMBEDDING_MODEL = "text-embedding-ada-002"
EMBEDDING_DIMENSION = 1536
INDEX_NAME = "book-chat"


class VectorStore:
    """
    Handles all vector database operations using Pinecone and OpenAI embeddings.
    """

    def __init__(self):
        """Initialize Pinecone and OpenAI clients."""
        # Get API keys
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.pinecone_api_key or self.pinecone_api_key == "your_pinecone_api_key_here":
            raise ValueError(
                "PINECONE_API_KEY not found or not set in .env file. "
                "Please add your Pinecone API key."
            )

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file.")

        # Initialize clients
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        self.openai_client = OpenAI(api_key=self.openai_api_key)
        self.index = None

    def create_or_connect_index(self):
        """
        Create a new Pinecone index or connect to existing one.

        Returns:
            Pinecone Index object
        """
        try:
            # Check if index already exists
            existing_indexes = [index.name for index in self.pc.list_indexes()]

            if INDEX_NAME not in existing_indexes:
                print(f"Creating new Pinecone index: {INDEX_NAME}")
                # Create new index
                self.pc.create_index(
                    name=INDEX_NAME,
                    dimension=EMBEDDING_DIMENSION,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
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

    def create_embedding(self, text):
        """
        Create embedding for a single text using OpenAI.

        Args:
            text: Text to embed

        Returns:
            list: Embedding vector (1536 dimensions)
        """
        try:
            response = self.openai_client.embeddings.create(
                model=EMBEDDING_MODEL,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error creating embedding: {str(e)}")

    def create_embeddings_batch(self, texts):
        """
        Create embeddings for multiple texts (batch processing).

        Args:
            texts: List of texts to embed

        Returns:
            list: List of embedding vectors
        """
        try:
            embeddings = []
            # Process in batches to avoid rate limits
            batch_size = 100

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                response = self.openai_client.embeddings.create(
                    model=EMBEDDING_MODEL,
                    input=batch
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)

            return embeddings
        except Exception as e:
            raise Exception(f"Error creating batch embeddings: {str(e)}")

    def store_chunks(self, chunks):
        """
        Store book chunks with their embeddings in Pinecone.

        Args:
            chunks: List of chunks with 'id' and 'text' keys

        Returns:
            int: Number of chunks stored
        """
        if not self.index:
            self.create_or_connect_index()

        try:
            print(f"Creating embeddings for {len(chunks)} chunks...")

            # Extract texts for batch embedding
            texts = [chunk['text'] for chunk in chunks]

            # Create embeddings
            embeddings = self.create_embeddings_batch(texts)

            print("Storing embeddings in Pinecone...")

            # Prepare vectors for upsert
            vectors = []
            for i, chunk in enumerate(chunks):
                vectors.append({
                    'id': chunk['id'],
                    'values': embeddings[i],
                    'metadata': {
                        'text': chunk['text']
                    }
                })

            # Upsert to Pinecone in batches
            batch_size = 100
            for i in range(0, len(vectors), batch_size):
                batch = vectors[i:i + batch_size]
                self.index.upsert(vectors=batch)

            print(f"Successfully stored {len(chunks)} chunks in Pinecone!")
            return len(chunks)

        except Exception as e:
            raise Exception(f"Error storing chunks in Pinecone: {str(e)}")

    def search_similar_chunks(self, query, top_k=3):
        """
        Search for most similar chunks to a query.

        Args:
            query: User's question
            top_k: Number of top results to return (default: 3)

        Returns:
            list: List of dictionaries with 'id', 'text', and 'score' keys
        """
        if not self.index:
            self.create_or_connect_index()

        try:
            # Create embedding for the query
            query_embedding = self.create_embedding(query)

            # Search in Pinecone
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
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
            raise Exception(f"Error searching similar chunks: {str(e)}")

    def get_index_stats(self):
        """
        Get statistics about the current index.

        Returns:
            dict: Index statistics
        """
        if not self.index:
            self.create_or_connect_index()

        try:
            stats = self.index.describe_index_stats()
            return stats
        except Exception as e:
            raise Exception(f"Error getting index stats: {str(e)}")

    def delete_all_vectors(self):
        """
        Delete all vectors from the index (useful for resetting).
        """
        if not self.index:
            self.create_or_connect_index()

        try:
            self.index.delete(delete_all=True)
            print("All vectors deleted from index.")
        except Exception as e:
            raise Exception(f"Error deleting vectors: {str(e)}")
