"""
Book Processing Service (Async)

Handles all book file processing operations:
- Detecting file types (.txt, .pdf)
- Reading text and PDF files
- Chunking text with overlap for RAG

Key Changes for Async:
- File I/O operations use asyncio.to_thread() for non-blocking
- Text processing remains synchronous (CPU-bound, not I/O-bound)

Source: Extracted from book_loader.py (entire file, converted to async)
"""

import os
import re
import asyncio
from typing import List, Dict
from PyPDF2 import PdfReader


class BookProcessingService:
    """Service for processing book files and chunking text (async)."""

    async def detect_file_type(self, file_path: str) -> str:
        """
        Detect if the file is a text file or PDF.

        Args:
            file_path: Path to the book file

        Returns:
            str: 'txt' or 'pdf'

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file type is not supported
        """
        # File system check (run in thread pool for non-blocking I/O)
        exists = await asyncio.to_thread(os.path.exists, file_path)
        if not exists:
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = os.path.splitext(file_path)[1].lower()

        if extension == '.txt':
            return 'txt'
        elif extension == '.pdf':
            return 'pdf'
        else:
            raise ValueError(
                f"Unsupported file type: {extension}. Only .txt and .pdf are supported."
            )

    async def read_text_file(self, file_path: str) -> str:
        """
        Read content from a text file.

        Args:
            file_path: Path to the text file

        Returns:
            str: Content of the file

        Raises:
            Exception: If file reading fails
        """
        def _read_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            except UnicodeDecodeError:
                # Try with different encoding if UTF-8 fails
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()

        # Run file I/O in thread pool for non-blocking
        return await asyncio.to_thread(_read_file)

    async def read_pdf_file(self, file_path: str) -> str:
        """
        Extract text content from a PDF file.

        Args:
            file_path: Path to the PDF file

        Returns:
            str: Extracted text content

        Raises:
            Exception: If PDF reading fails
        """
        def _read_pdf():
            try:
                reader = PdfReader(file_path)
                text = ""

                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

                return text
            except Exception as e:
                raise Exception(f"Error reading PDF: {str(e)}")

        # Run PDF reading in thread pool for non-blocking
        return await asyncio.to_thread(_read_pdf)

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 500,
        overlap_size: int = 50
    ) -> List[Dict]:
        """
        Split text into chunks based on word count with overlap between chunks.
        Tries to split at paragraph boundaries when possible.

        Args:
            text: The book content to split
            chunk_size: Target number of words per chunk (default: 500)
            overlap_size: Number of words to overlap between chunks (default: 50)

        Returns:
            list: List of dictionaries with 'id' and 'text' keys
        """
        # Clean up the text - remove extra whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)  # Replace multiple newlines with double newlines
        text = re.sub(r' +', ' ', text)  # Replace multiple spaces with single space

        # Split into paragraphs
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

        chunks = []
        current_chunk = ""
        chunk_id = 1

        for paragraph in paragraphs:
            # Count words in current chunk and paragraph
            current_word_count = len(current_chunk.split())
            paragraph_word_count = len(paragraph.split())

            # If adding this paragraph would exceed chunk_size, save current chunk
            if current_chunk and (current_word_count + paragraph_word_count > chunk_size):
                chunks.append({
                    'id': f'chunk_{chunk_id}',
                    'text': current_chunk.strip()
                })
                chunk_id += 1

                # Extract overlap from the end of the previous chunk
                words = current_chunk.split()
                overlap_text = ' '.join(words[-overlap_size:]) if len(words) >= overlap_size else current_chunk

                # Start new chunk with overlap + new paragraph
                current_chunk = overlap_text + "\n\n" + paragraph
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph

        # Add the last chunk
        if current_chunk:
            chunks.append({
                'id': f'chunk_{chunk_id}',
                'text': current_chunk.strip()
            })

        print(f"Split book into {len(chunks)} chunks (with {overlap_size}-word overlap)")
        return chunks

    async def process_book(
        self,
        file_path: str,
        chunk_size: int = 500,
        overlap_size: int = 50
    ) -> List[Dict]:
        """
        Complete pipeline: Load book and split into chunks with overlap.

        Args:
            file_path: Path to the book file (.txt or .pdf)
            chunk_size: Target number of words per chunk (default: 500)
            overlap_size: Number of words to overlap between chunks (default: 50)

        Returns:
            list: List of chunks with id and text

        Raises:
            Exception: If processing fails at any stage
        """
        # Detect file type (async)
        file_type = await self.detect_file_type(file_path)
        print(f"Loading {file_type.upper()} file: {file_path}")

        # Load content based on file type (async file I/O)
        if file_type == 'txt':
            content = await self.read_text_file(file_path)
        else:  # pdf
            content = await self.read_pdf_file(file_path)

        print(f"Successfully loaded book ({len(content)} characters)")

        # Split into chunks with overlap (CPU-bound, stays sync)
        chunks = self.chunk_text(content, chunk_size, overlap_size)

        return chunks
