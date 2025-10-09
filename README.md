# OpenAI Chat Application

A simple command-line chat application that uses OpenAI's GPT-3.5-turbo model to provide conversational AI interactions. The application maintains conversation history and provides a clean terminal-based interface.

## Features

- Interactive command-line chat interface
- Conversation history maintenance
- Error handling for API issues
- Environment variable configuration for API key security
- Graceful exit options

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pzeel74/practice.git
   cd practice
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   To get an OpenAI API key:
   - Visit [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in to your account
   - Go to API Keys section
   - Create a new secret key

## Usage

1. **Activate your virtual environment** (if not already activated):
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Run the application:**
   ```bash
   python chat.py
   ```

3. **Start chatting:**
   - Type your message and press Enter
   - The AI will respond with contextual awareness of the conversation
   - Type `quit` to exit the application
   - Press `Ctrl+C` for immediate exit

## Example

```
OpenAI Chat (type 'quit' to exit)
----------------------------------------

You: Hello! How are you today?

Assistant: Hello! I'm doing well, thank you for asking. I'm here and ready to help you with any questions or tasks you might have. How are you doing today?

You: Can you help me with Python programming?

Assistant: Absolutely! I'd be happy to help you with Python programming. Whether you need help with:

- Basic syntax and concepts
- Debugging code
- Best practices
- Specific libraries or frameworks
- Project architecture
- Or any other Python-related questions

Just let me know what you're working on or what you'd like to learn!

You: quit
Goodbye!
```

## Error Handling

The application handles various error scenarios:

- **Missing API Key**: Checks for the presence of the OpenAI API key in environment variables
- **Authentication Errors**: Validates API key authenticity
- **Rate Limiting**: Handles API rate limit exceeded errors
- **Network Issues**: Manages general API connectivity problems
- **Keyboard Interrupts**: Graceful handling of Ctrl+C

## Project Structure

```
practice/
├── chat.py           # Main application file
├── requirements.txt  # Python dependencies
├── .env             # Environment variables (create this)
├── .gitignore       # Git ignore patterns
└── README.md        # Project documentation
```

## Dependencies

- `openai`: Official OpenAI Python client library
- `python-dotenv`: Loads environment variables from .env files

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
