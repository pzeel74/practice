import os
import sys
from openai import OpenAI, AuthenticationError, RateLimitError, APIError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    print("Please create a .env file with your API key.")
    sys.exit(1)

try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    sys.exit(1)

def chat():
    print("OpenAI Chat (type 'quit' to exit)")
    print("-" * 40)

    while True:
        # Read user input
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Send to OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": user_input}
                ]
            )

            # Print response
            assistant_message = response.choices[0].message.content
            print(f"\nAssistant: {assistant_message}")

        except AuthenticationError:
            print("\nError: Invalid API key. Please check your OPENAI_API_KEY.")
            break
        except RateLimitError:
            print("\nError: Rate limit exceeded. Please wait and try again.")
        except APIError as e:
            print(f"\nError: OpenAI API error - {e}")
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    chat()
