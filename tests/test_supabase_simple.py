"""
Simple Supabase Test - Insert Data Only
This script inserts test data into your Supabase database.
After running, go to Supabase Dashboard → Table Editor to verify the data.
"""

import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY not found in .env file")
    exit(1)

# Initialize Supabase client
print("="*60)
print("Connecting to Supabase...")
print("="*60)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Successfully connected to Supabase!")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    exit(1)

print("\n" + "="*60)
print("Inserting Test Data...")
print("="*60)

try:
    # ========================================
    # 1. Insert a test user
    # ========================================
    print("\n📝 Creating user...")

    user_data = {
        "email": "alice@example.com",
        "name": "Alice Smith"
    }

    user_response = supabase.table("users").insert(user_data).execute()
    user_id = user_response.data[0]["id"]

    print(f"✅ User created!")
    print(f"   ID: {user_id}")
    print(f"   Email: {user_data['email']}")
    print(f"   Name: {user_data['name']}")

    # ========================================
    # 2. Insert a test book
    # ========================================
    print("\n📚 Creating book...")

    book_data = {
        "user_id": user_id,
        "title": "Alice in Wonderland",
        "filename": "alice_in_wonderland.txt",
        "storage_path": "uploads/alice/alice_in_wonderland.txt",
        "author": "Lewis Carroll",
        "metadata": {"pages": 90, "word_count": 26543},
        "pinecone_namespace": f"alice-{user_id}-wonderland"
    }

    book_response = supabase.table("books").insert(book_data).execute()
    book_id = book_response.data[0]["id"]

    print(f"✅ Book created!")
    print(f"   ID: {book_id}")
    print(f"   Title: {book_data['title']}")
    print(f"   Author: {book_data['author']}")

    # ========================================
    # 3. Insert a test chat
    # ========================================
    print("\n💬 Creating chat...")

    chat_data = {
        "user_id": user_id,
        "title": "Questions about Alice in Wonderland",
        "messages": []
    }

    chat_response = supabase.table("chats").insert(chat_data).execute()
    chat_id = chat_response.data[0]["id"]

    print(f"✅ Chat created!")
    print(f"   ID: {chat_id}")
    print(f"   Title: {chat_data['title']}")

    # ========================================
    # 4. Insert test messages
    # ========================================
    print("\n📨 Creating messages...")

    messages_data = [
        {
            "chat_id": chat_id,
            "role": "user",
            "content": "Who is the main character?"
        },
        {
            "chat_id": chat_id,
            "role": "assistant",
            "content": "The main character is Alice, a young girl who falls down a rabbit hole into a fantasy world."
        },
        {
            "chat_id": chat_id,
            "role": "user",
            "content": "What happens at the tea party?"
        },
        {
            "chat_id": chat_id,
            "role": "assistant",
            "content": "At the tea party, Alice meets the Mad Hatter, March Hare, and Dormouse. They have a chaotic conversation and keep switching seats."
        }
    ]

    messages_response = supabase.table("messages").insert(messages_data).execute()

    print(f"✅ {len(messages_response.data)} messages created!")
    for i, msg in enumerate(messages_data, 1):
        print(f"   Message {i}: [{msg['role']}] {msg['content'][:40]}...")

    # ========================================
    # SUCCESS!
    # ========================================
    print("\n" + "="*60)
    print("✅✅✅ ALL DATA INSERTED SUCCESSFULLY! ✅✅✅")
    print("="*60)

    print("\n" + "="*60)
    print("🔍 HOW TO VERIFY IN SUPABASE:")
    print("="*60)
    print("1. Go to: https://kgvogczkipsznpewtlrd.supabase.co")
    print("2. Click 'Table Editor' in the left sidebar")
    print("3. Check each table:")
    print("   • users table → Look for: alice@example.com")
    print("   • books table → Look for: Alice in Wonderland")
    print("   • chats table → Look for: Questions about Alice...")
    print("   • messages table → You should see 4 messages")

    print("\n" + "="*60)
    print("💾 SAVED IDs (for reference):")
    print("="*60)
    print(f"User ID:  {user_id}")
    print(f"Book ID:  {book_id}")
    print(f"Chat ID:  {chat_id}")

    print("\n" + "="*60)
    print("🗑️  TO DELETE THIS TEST DATA LATER:")
    print("="*60)
    print("Option 1: In Supabase Table Editor")
    print("  - Go to 'users' table")
    print(f"  - Find user with email: alice@example.com")
    print("  - Click the row, then click 'Delete row'")
    print("  - All related data will be deleted automatically!")
    print("")
    print("Option 2: Run this Python command:")
    print(f"  supabase.table('users').delete().eq('id', '{user_id}').execute()")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("Script complete!")
print("="*60)
