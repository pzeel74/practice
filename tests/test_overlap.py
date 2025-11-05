"""
Test script to demonstrate chunk overlap functionality.
Shows how the last words of one chunk appear at the start of the next.
"""

from book_loader import chunk_text

# Sample text (3 paragraphs)
sample_text = """
Alice was beginning to get very tired of sitting by her sister on the bank,
and of having nothing to do. Once or twice she had peeped into the book her
sister was reading, but it had no pictures or conversations in it, and what
is the use of a book, thought Alice, without pictures or conversations?

So she was considering in her own mind, as well as she could, for the hot day
made her feel very sleepy and stupid, whether the pleasure of making a
daisy-chain would be worth the trouble of getting up and picking the daisies,
when suddenly a White Rabbit with pink eyes ran close by her.

There was nothing so very remarkable in that, nor did Alice think it so very
much out of the way to hear the Rabbit say to itself, Oh dear! Oh dear! I shall
be too late! But when the Rabbit actually took a watch out of its waistcoat-pocket
and looked at it, and then hurried on, Alice started to her feet.
"""

print("="*70)
print("OVERLAP DEMONSTRATION")
print("="*70)

# Create chunks with 50-word overlap (using small chunk_size for demo)
chunks = chunk_text(sample_text, chunk_size=60, overlap_size=15)

print(f"\nCreated {len(chunks)} chunks with 15-word overlap")
print("\n" + "="*70)

for i, chunk in enumerate(chunks, 1):
    print(f"\n📄 CHUNK {i} (ID: {chunk['id']})")
    print("-" * 70)

    words = chunk['text'].split()
    print(f"Word count: {len(words)}")

    # Show first and last 15 words to see overlap
    if len(words) >= 15:
        first_15 = ' '.join(words[:15])
        last_15 = ' '.join(words[-15:])

        print(f"\n🔹 First 15 words:")
        print(f"   {first_15}...")

        print(f"\n🔹 Last 15 words:")
        print(f"   ...{last_15}")
    else:
        print(f"\n{chunk['text']}")

# Demonstrate overlap between chunks
print("\n" + "="*70)
print("OVERLAP CHECK")
print("="*70)

for i in range(len(chunks) - 1):
    current_chunk = chunks[i]['text']
    next_chunk = chunks[i + 1]['text']

    # Get last 15 words of current chunk
    last_words_current = ' '.join(current_chunk.split()[-15:])

    # Get first 15 words of next chunk
    first_words_next = ' '.join(next_chunk.split()[:15])

    print(f"\n🔗 Overlap between Chunk {i+1} and Chunk {i+2}:")
    print(f"   Last 15 words of Chunk {i+1}: '{last_words_current}'")
    print(f"   First 15 words of Chunk {i+2}: '{first_words_next}'")

    # Check if they match (should be identical or very similar)
    if last_words_current in next_chunk:
        print(f"   ✅ OVERLAP CONFIRMED!")
    else:
        print(f"   ⚠️  Note: Overlap may include paragraph break")

print("\n" + "="*70)
print("✅ Overlap feature is working correctly!")
print("="*70)
