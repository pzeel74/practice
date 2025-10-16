"""
Quick test script for the RAG Book Chat system.
This will load the sample book, create embeddings, and test queries.
"""

import os
import sys
import time

# Force reload of .env file
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']
if 'PINECONE_API_KEY' in os.environ:
    del os.environ['PINECONE_API_KEY']

from dotenv import load_dotenv
load_dotenv(override=True)

from book_loader import process_book
from vector_store import VectorStore

def test_rag_system():
    print("="*60)
    print("Testing RAG Book Chat System")
    print("="*60)

    # Step 1: Initialize Vector Store
    print("\n[1/4] Initializing Pinecone connection...")
    try:
        vector_store = VectorStore()
        vector_store.create_or_connect_index()
        print("✓ Connected to Pinecone successfully!")
    except Exception as e:
        print(f"✗ Error connecting to Pinecone: {e}")
        return

    # Step 2: Load and chunk the book
    print("\n[2/4] Loading and chunking sample book...")
    try:
        chunks = process_book("sample_book.txt", chunk_size=500)
        print(f"✓ Loaded book with {len(chunks)} chunks")
        print(f"  First chunk preview: {chunks[0]['text'][:100]}...")
    except Exception as e:
        print(f"✗ Error loading book: {e}")
        return

    # Step 3: Store embeddings in Pinecone
    print("\n[3/4] Creating embeddings and storing in Pinecone...")
    try:
        num_stored = vector_store.store_chunks(chunks)
        print(f"✓ Stored {num_stored} chunks with embeddings")
    except Exception as e:
        print(f"✗ Error storing embeddings: {e}")
        return

    # Wait for Pinecone to index the vectors
    print("\n⏳ Waiting 5 seconds for Pinecone to index vectors...")
    time.sleep(5)

    # Step 4: Test retrieval with sample queries
    print("\n[4/4] Testing retrieval with sample queries...")

    test_queries = [
        "Who is Luna?",
        "What happened with the mysterious signal?",
        "Where does Luna live?"
    ]

    for query in test_queries:
        print(f"\n  Query: '{query}'")
        try:
            results = vector_store.search_similar_chunks(query, top_k=2)
            print(f"  ✓ Found {len(results)} relevant chunks")
            for i, result in enumerate(results):
                print(f"    [{i+1}] Score: {result['score']:.4f}")
                print(f"        Preview: {result['text'][:80]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Get index stats
    print("\n" + "="*60)
    print("Final Index Statistics:")
    try:
        stats = vector_store.get_index_stats()
        print(f"  Total vectors: {stats.total_vector_count if hasattr(stats, 'total_vector_count') else 'N/A'}")
        print(f"  Index: {stats}")
    except Exception as e:
        print(f"  Error getting stats: {e}")

    print("\n" + "="*60)
    print("✓ RAG System Test Complete!")
    print("="*60)
    print("\nYou can now run: python chat.py")
    print("Choose option 2 for Book Chat mode")

if __name__ == "__main__":
    test_rag_system()
