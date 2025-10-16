import os
import re
from PyPDF2 import PdfReader


def detect_file_type(file_path):
    """
    Detect if the file is a text file or PDF.

    Args:
        file_path: Path to the book file

    Returns:
        str: 'txt' or 'pdf'

    Raises:
        ValueError: If file type is not supported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.txt':
        return 'txt'
    elif extension == '.pdf':
        return 'pdf'
    else:
        raise ValueError(f"Unsupported file type: {extension}. Only .txt and .pdf are supported.")


def read_text_file(file_path):
    """
    Read content from a text file.

    Args:
        file_path: Path to the text file

    Returns:
        str: Content of the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(file_path, 'r', encoding='latin-1') as file:
            return file.read()


def read_pdf_file(file_path):
    """
    Extract text content from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        str: Extracted text content
    """
    try:
        reader = PdfReader(file_path)
        text = ""

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")


def load_book(file_path):
    """
    Load a book from either text or PDF file.

    Args:
        file_path: Path to the book file

    Returns:
        str: Content of the book
    """
    file_type = detect_file_type(file_path)

    print(f"Loading {file_type.upper()} file: {file_path}")

    if file_type == 'txt':
        content = read_text_file(file_path)
    else:  # pdf
        content = read_pdf_file(file_path)

    print(f"Successfully loaded book ({len(content)} characters)")
    return content


def chunk_text(text, chunk_size=500):
    """
    Split text into chunks based on word count.
    Tries to split at paragraph boundaries when possible.

    Args:
        text: The book content to split
        chunk_size: Target number of words per chunk (default: 500)

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
            current_chunk = paragraph
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

    print(f"Split book into {len(chunks)} chunks")
    return chunks


def process_book(file_path, chunk_size=500):
    """
    Complete pipeline: Load book and split into chunks.

    Args:
        file_path: Path to the book file
        chunk_size: Target number of words per chunk

    Returns:
        list: List of chunks with id and text
    """
    # Load the book
    content = load_book(file_path)

    # Split into chunks
    chunks = chunk_text(content, chunk_size)

    return chunks
