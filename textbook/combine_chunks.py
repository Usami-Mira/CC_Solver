#!/usr/bin/env python3
"""
Combine old and new textbook chunks into a single file for embedding.
"""

import json
from pathlib import Path


def main():
    base_dir = Path('/home/usamimira/PHY-LLM/CC_Solver/textbook')

    # Load old chunks (existing Chinese textbooks)
    old_chunks_file = base_dir / 'merged' / 'chunks_final.json'
    print(f"Loading old chunks from {old_chunks_file}...")
    with open(old_chunks_file, 'r', encoding='utf-8') as f:
        old_chunks = json.load(f)
    print(f"  Old chunks: {len(old_chunks)}")

    # Load new chunks (new English textbooks)
    new_chunks_file = base_dir / 'merged_new' / 'chunks_final.json'
    print(f"Loading new chunks from {new_chunks_file}...")
    with open(new_chunks_file, 'r', encoding='utf-8') as f:
        new_chunks = json.load(f)
    print(f"  New chunks: {len(new_chunks)}")

    # Combine
    all_chunks = old_chunks + new_chunks
    print(f"\nTotal chunks: {len(all_chunks)}")

    # Save combined file
    output_file = base_dir / 'merged' / 'chunks_combined.json'
    print(f"\nSaving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(all_chunks)} chunks to {output_file}")

    # Stats by book
    print("\nChunks by book:")
    book_counts = {}
    for chunk in all_chunks:
        book = chunk.get('book', 'unknown')
        book_counts[book] = book_counts.get(book, 0) + 1

    for book, count in sorted(book_counts.items()):
        print(f"  {book}: {count}")


if __name__ == '__main__':
    main()
