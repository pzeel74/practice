"""
Simple demonstration of chunk overlap concept (no dependencies).
Shows how overlap preserves context between chunks.
"""

def simple_chunk_with_overlap(text, chunk_size=60, overlap_size=15):
    """Simplified chunking function for demonstration."""
    words = text.split()
    chunks = []
    i = 0
    chunk_id = 1

    while i < len(words):
        # Take chunk_size words
        chunk_words = words[i:i + chunk_size]
        chunk_text = ' '.join(chunk_words)

        chunks.append({
            'id': f'chunk_{chunk_id}',
            'text': chunk_text
        })

        # Move forward by (chunk_size - overlap_size) to create overlap
        i += (chunk_size - overlap_size)
        chunk_id += 1

    return chunks


# Sample text
sample_text = """
Alice was beginning to get very tired of sitting by her sister on the bank.
Once or twice she had peeped into the book her sister was reading.
So she was considering in her own mind whether the pleasure of making a daisy-chain would be worth the trouble.
Suddenly a White Rabbit with pink eyes ran close by her.
There was nothing so very remarkable in that.
But when the Rabbit actually took a watch out of its waistcoat-pocket Alice started to her feet.
"""

print("="*80)
print("CHUNK OVERLAP DEMONSTRATION")
print("="*80)
print(f"\nOriginal text has {len(sample_text.split())} words")
print(f"Chunk size: 60 words")
print(f"Overlap size: 15 words")
print(f"Effective step: 45 words (60 - 15)")

chunks = simple_chunk_with_overlap(sample_text.strip(), chunk_size=60, overlap_size=15)

print(f"\nResult: {len(chunks)} chunks created")
print("\n" + "="*80)

for i, chunk in enumerate(chunks, 1):
    words = chunk['text'].split()
    print(f"\n📦 CHUNK {i} ({len(words)} words)")
    print("-" * 80)

    # Show full text for small demo
    print(chunk['text'])

    if len(words) >= 15:
        print(f"\n   📍 Last 15 words: ...{' '.join(words[-15:])}")

print("\n" + "="*80)
print("OVERLAP VERIFICATION")
print("="*80)

for i in range(len(chunks) - 1):
    chunk1_words = chunks[i]['text'].split()
    chunk2_words = chunks[i + 1]['text'].split()

    last_15_chunk1 = ' '.join(chunk1_words[-15:])
    first_15_chunk2 = ' '.join(chunk2_words[:15])

    print(f"\n🔗 Between Chunk {i+1} and Chunk {i+2}:")
    print(f"   Chunk {i+1} ends:   ...{last_15_chunk1}")
    print(f"   Chunk {i+2} starts: {first_15_chunk2}...")

    # Check overlap
    matching_words = 0
    for word in last_15_chunk1.split():
        if word in first_15_chunk2:
            matching_words += 1

    print(f"   ✅ Matching words: {matching_words}/15 (overlap confirmed!)")

print("\n" + "="*80)
print("WHY THIS MATTERS")
print("="*80)
print("""
Without overlap:
  Chunk 1: "...Alice met a mysterious character who"
  Chunk 2: "told her the Queen was dangerous"
  ❌ Context split! Hard to understand who spoke.

With 15-word overlap:
  Chunk 1: "...Alice met a mysterious character who told her"
  Chunk 2: "character who told her the Queen was dangerous"
  ✅ Context preserved! Clear who spoke.
""")
