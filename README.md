# OpenAI Chat Application with RAG

A Python command-line chat application with two modes:
1. **Normal Chat** - Traditional AI conversation with persistent memory
2. **Book Chat (RAG)** - Ask questions about any book using vector search and AI

## What is This Project?

This project demonstrates three progressive AI implementation tasks:

- **Task 1**: Basic OpenAI chat integration
- **Task 2**: Persistent conversation history (saved to JSON)
- **Task 3**: RAG (Retrieval-Augmented Generation) - chat with books using Pinecone vector database

The Book Chat mode prevents AI hallucination by only answering based on actual book content, using semantic search to find relevant passages.

## Features

### Normal Chat
- Real-time conversation with GPT-3.5-turbo
- Conversation history persists across sessions
- Context-aware responses

### Book Chat (RAG)
- Upload text or PDF books
- Intelligent text chunking (~500 words)
- Vector embeddings via OpenAI
- Semantic search with Pinecone
- Answers based ONLY on book content

## Quick Start

### 1. Prerequisites
- Python 3.7+
- OpenAI API key
- Pinecone API key (for Book Chat mode)

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/pzeel74/practice.git
cd practice

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up API keys
cp .env.example .env
# Edit .env and add your API keys
```

### 3. Get API Keys

**OpenAI API Key:**
- Visit [OpenAI Platform](https://platform.openai.com/)
- Create an account and generate an API key
- Add to `.env` file

**Pinecone API Key (for Book Chat):**
- Visit [Pinecone](https://www.pinecone.io/)
- Create a free account
- Create an index: name=`book-chat`, dimensions=`1536`, metric=`cosine`
- Add API key to `.env` file

### 4. Run the Application

```bash
source .venv/bin/activate
python chat.py
```

**On Apple Silicon Macs (if you get architecture errors):**
```bash
./run_chat.sh
```

## Usage

When you start the app, choose a mode:

```
1. Normal Chat - Regular conversation with AI
2. Book Chat - Ask questions about a book (RAG)
```

### Normal Chat
- Type your messages and press Enter
- Conversation history is automatically saved
- Type `quit` to exit

### Book Chat
- First time: Enter path to your book file (`.txt` or `.pdf`)
- Example: `sample_book.txt`
- Wait for processing (done once per book)
- Ask questions about the book
- Get answers based only on book content

## Project Structure

```
├── chat.py                    # Main application
├── book_loader.py             # Text/PDF processing & chunking
├── vector_store.py            # Pinecone & OpenAI embeddings
├── test_rag.py               # Test script for RAG
├── sample_book.txt           # Sample book for testing
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── run_chat.sh              # ARM64 compatibility script
```

## How Book Chat (RAG) Works

```
1. Upload Book → Split into chunks → Generate embeddings → Store in Pinecone

2. Ask Question → Search similar chunks → Send to GPT → Get answer based on book
```

**Why RAG?**
- Prevents AI hallucination
- Answers based on actual document content
- Works with any book/document
- Provides source citations

## Testing

Try the included sample book:

```bash
source .venv/bin/activate
python chat.py
# Choose option 2 (Book Chat)
# Enter: sample_book.txt
# Ask: "Who is Luna?"
```

## Troubleshooting

**Architecture errors on Mac?**
```bash
./run_chat.sh
```

**API authentication error?**
- Check `.env` file has correct API keys
- Verify OpenAI account has credits

**Module not found?**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

**Pinecone index not found?**
- Create index named `book-chat`
- Dimensions: `1536`, Metric: `cosine`

## Technologies Used

- **OpenAI GPT-3.5-turbo** - Conversation AI
- **OpenAI text-embedding-ada-002** - Vector embeddings
- **Pinecone** - Vector database
- **PyPDF2** - PDF text extraction
- **python-dotenv** - Environment management

## License

This is a learning project for educational purposes.
