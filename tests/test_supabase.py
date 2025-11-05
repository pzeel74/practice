"""
Test script for Supabase database connection and basic operations.
This script tests:
1. Connection to Supabase
2. Insert a test user
3. Insert a test book
4. Insert a test chat
5. Insert test messages
6. Query the data back
7. Clean up test data
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
print("Testing Supabase Connection")
print("="*60)

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Successfully connected to Supabase!")
except Exception as e:
    print(f"❌ Failed to connect to Supabase: {e}")
    exit(1)

# Test variables to store IDs
test_user_id = None
test_book_id = None
test_chat_id = None

try:
    # ========================================
    # TEST 1: Insert a test user
    # ========================================
    print("\n" + "="*60)
    print("TEST 1: Inserting a test user...")
    print("="*60)

    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }

    response = supabase.table("users").insert(user_data).execute()

    if response.data:
        test_user_id = response.data[0]["id"]
        print(f"✅ User created successfully!")
        print(f"   User ID: {test_user_id}")
        print(f"   Email: {response.data[0]['email']}")
        print(f"   Name: {response.data[0]['name']}")
    else:
        print("❌ Failed to create user")
        exit(1)

    # ========================================
    # TEST 2: Insert a test book
    # ========================================
    print("\n" + "="*60)
    print("TEST 2: Inserting a test book...")
    print("="*60)

    book_data = {
        "user_id": test_user_id,
        "title": "Alice in Wonderland",
        "filename": "alice_in_wonderland.txt",
        "storage_path": "uploads/test/alice_in_wonderland.txt",
        "author": "Lewis Carroll",
        "metadata": {"pages": 90, "word_count": 26543},
        "pinecone_namespace": f"test-{test_user_id}-alice"
    }

    response = supabase.table("books").insert(book_data).execute()

    if response.data:
        test_book_id = response.data[0]["id"]
        print(f"✅ Book created successfully!")
        print(f"   Book ID: {test_book_id}")
        print(f"   Title: {response.data[0]['title']}")
        print(f"   Author: {response.data[0]['author']}")
        print(f"   Namespace: {response.data[0]['pinecone_namespace']}")
    else:
        print("❌ Failed to create book")
        exit(1)

    # ========================================
    # TEST 3: Insert a test chat
    # ========================================
    print("\n" + "="*60)
    print("TEST 3: Inserting a test chat...")
    print("="*60)

    chat_data = {
        "user_id": test_user_id,
        "title": "Who is the main character?",
        "messages": []
    }

    response = supabase.table("chats").insert(chat_data).execute()

    if response.data:
        test_chat_id = response.data[0]["id"]
        print(f"✅ Chat created successfully!")
        print(f"   Chat ID: {test_chat_id}")
        print(f"   Title: {response.data[0]['title']}")
    else:
        print("❌ Failed to create chat")
        exit(1)

    # ========================================
    # TEST 4: Insert test messages
    # ========================================
    print("\n" + "="*60)
    print("TEST 4: Inserting test messages...")
    print("="*60)

    messages_data = [
        {
            "chat_id": test_chat_id,
            "role": "user",
            "content": "Who is the main character?"
        },
        {
            "chat_id": test_chat_id,
            "role": "assistant",
            "content": "The main character is Alice, a young girl who falls down a rabbit hole into a fantasy world."
        },
        {
            "chat_id": test_chat_id,
            "role": "user",
            "content": "What does she find at the bottom?"
        },
        {
            "chat_id": test_chat_id,
            "role": "assistant",
            "content": "At the bottom of the rabbit hole, Alice finds a long hallway with doors of various sizes and a small golden key."
        }
    ]

    response = supabase.table("messages").insert(messages_data).execute()

    if response.data:
        print(f"✅ {len(response.data)} messages created successfully!")
        for i, msg in enumerate(response.data, 1):
            print(f"   Message {i}: [{msg['role']}] {msg['content'][:50]}...")
    else:
        print("❌ Failed to create messages")
        exit(1)

    # ========================================
    # TEST 5: Query data back (JOIN)
    # ========================================
    print("\n" + "="*60)
    print("TEST 5: Querying data back...")
    print("="*60)

    # Get all messages for this chat
    response = supabase.table("messages") \
        .select("*") \
        .eq("chat_id", test_chat_id) \
        .order("created_at") \
        .execute()

    if response.data:
        print(f"✅ Retrieved {len(response.data)} messages:")
        for msg in response.data:
            print(f"   [{msg['role']}]: {msg['content']}")
    else:
        print("❌ No messages found")

    # ========================================
    # TEST 6: Get user's books
    # ========================================
    print("\n" + "="*60)
    print("TEST 6: Getting user's books...")
    print("="*60)

    response = supabase.table("books") \
        .select("*") \
        .eq("user_id", test_user_id) \
        .execute()

    if response.data:
        print(f"✅ User has {len(response.data)} book(s):")
        for book in response.data:
            print(f"   - {book['title']} by {book['author']}")
    else:
        print("❌ No books found")

    # ========================================
    # TEST 7: Get user's chats
    # ========================================
    print("\n" + "="*60)
    print("TEST 7: Getting user's chats...")
    print("="*60)

    response = supabase.table("chats") \
        .select("*") \
        .eq("user_id", test_user_id) \
        .order("updated_at", desc=True) \
        .execute()

    if response.data:
        print(f"✅ User has {len(response.data)} chat(s):")
        for chat in response.data:
            print(f"   - {chat['title']} (created: {chat['created_at']})")
    else:
        print("❌ No chats found")

    print("\n" + "="*60)
    print("✅✅✅ ALL TESTS PASSED! ✅✅✅")
    print("="*60)

except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()

finally:
    # ========================================
    # CLEANUP: Delete test data
    # ========================================
    print("\n" + "="*60)
    print("CLEANUP: Deleting test data...")
    print("="*60)

    try:
        if test_user_id:
            # Delete user (CASCADE will delete books, chats, and messages)
            supabase.table("users").delete().eq("id", test_user_id).execute()
            print("✅ Test data deleted successfully!")
            print("   (User, books, chats, and messages all removed via CASCADE)")
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

print("\n" + "="*60)
print("Test complete!")
print("="*60)
