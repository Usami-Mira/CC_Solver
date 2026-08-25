#!/usr/bin/env python3
"""
Process new textbooks: extract pure content, split by sections, smart chunk.
For: ahlfors, cft, special_functions
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any


def estimate_tokens(text: str) -> int:
    """Estimate token count (roughly 1.5 chars per token for mixed content)."""
    return int(len(text) / 1.5)


def find_paragraph_break(text: str, target_pos: int, window: int = 300) -> int:
    """Find the nearest paragraph break to target_pos."""
    start = max(0, target_pos - window)
    end = min(len(text), target_pos + window)
    search_region = text[start:end]

    # Look for double newlines first (strongest break)
    double_newline = search_region.rfind('\n\n', 0, target_pos - start)
    if double_newline != -1 and abs(start + double_newline - target_pos) < window:
        return start + double_newline + 2

    # Look for single newline after sentence ending
    for i in range(target_pos - start, -1, -1):
        if i < len(search_region) and search_region[i] == '\n':
            if i > 0 and search_region[i-1] in '。！？；.!?;':
                return start + i + 1

    # Fallback: look for any newline
    newline_pos = search_region.rfind('\n', 0, target_pos - start)
    if newline_pos != -1:
        return start + newline_pos + 1

    return target_pos


def smart_split(text: str, max_tokens: int = 2048, overlap_tokens: int = 256) -> List[str]:
    """Split text into chunks with paragraph-aware boundaries and overlap."""
    max_chars = int(max_tokens * 1.5)
    overlap_chars = int(overlap_tokens * 1.5)

    chunks = []
    pos = 0

    while pos < len(text):
        if len(text) - pos <= max_chars:
            chunks.append(text[pos:])
            break

        target_end = pos + max_chars
        break_point = find_paragraph_break(text, target_end, window=300)

        chunk = text[pos:break_point].strip()
        chunks.append(chunk)

        pos = break_point - overlap_chars
        if pos < 0:
            pos = break_point

    return chunks


def extract_sections(md_path: Path, book_name: str) -> tuple[List[Dict], List[Dict]]:
    """
    Extract pure content and examples from merged markdown.
    Returns (pure_sections, examples).
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    sections = []
    examples = []
    current_section = None
    current_example = None

    for line in lines:
        # Detect section start (## headers)
        if line.startswith('## '):
            # Save previous section
            if current_section and current_section['content'].strip():
                sections.append(current_section)

            # Save previous example
            if current_example and current_example['content'].strip():
                examples.append(current_example)

            # Start new section
            title = line[3:].strip()

            # Try to extract chapter/section numbers
            chapter = None
            section_num = None

            # Pattern: "1.2 Title" or "§1.2 Title"
            if match := re.match(r'(\d+)\.(\d+)\s+(.+)', title):
                chapter = match.group(1)
                section_num = match.group(2)
                title = match.group(3)
            elif match := re.match(r'§\s*(\d+)\.(\d+)\s+(.+)', title):
                chapter = match.group(1)
                section_num = match.group(2)
                title = match.group(3)
            elif match := re.match(r'Chapter\s+(\d+)', title, re.IGNORECASE):
                chapter = match.group(1)
            elif match := re.match(r'(\d+)\.\s+(.+)', title):
                chapter = match.group(1)
                title = match.group(2)

            current_section = {
                'book': book_name,
                'chapter': chapter,
                'section': section_num,
                'title': title,
                'content': '',
                'type': 'content',
            }
            current_example = None

        # Detect example start
        elif re.match(r'^(Example|例题|例)\s*\d*', line, re.IGNORECASE):
            # Save previous section
            if current_section and current_section['content'].strip():
                sections.append(current_section)
                current_section = None

            # Save previous example
            if current_example and current_example['content'].strip():
                examples.append(current_example)

            # Start new example
            current_example = {
                'book': book_name,
                'title': line.strip(),
                'content': '',
                'type': 'example',
            }

        # Detect exercise start
        elif re.match(r'^(Exercise|习题|练习)\s*\d*', line, re.IGNORECASE):
            # Save previous
            if current_section and current_section['content'].strip():
                sections.append(current_section)
                current_section = None
            if current_example and current_example['content'].strip():
                examples.append(current_example)

            current_example = {
                'book': book_name,
                'title': line.strip(),
                'content': '',
                'type': 'exercise',
            }

        # Accumulate content
        else:
            if current_example is not None:
                if current_example['content']:
                    current_example['content'] += '\n' + line
                else:
                    current_example['content'] = line
            elif current_section is not None:
                if current_section['content']:
                    current_section['content'] += '\n' + line
                else:
                    current_section['content'] = line

    # Don't forget the last items
    if current_section and current_section['content'].strip():
        sections.append(current_section)
    if current_example and current_example['content'].strip():
        examples.append(current_example)

    # Filter out very small sections
    sections = [s for s in sections if len(s['content'].strip()) > 100]
    examples = [e for e in examples if len(e['content'].strip()) > 50]

    return sections, examples


def chunk_entries(entries: List[Dict[str, Any]], max_tokens: int = 2048, overlap_tokens: int = 256) -> List[Dict[str, Any]]:
    """Chunk entries that exceed max_tokens, keep short ones as-is."""
    chunked = []

    for entry in entries:
        content = entry['content']
        tokens = estimate_tokens(content)

        if tokens <= max_tokens:
            chunked.append(entry)
        else:
            chunks = smart_split(content, max_tokens, overlap_tokens)

            for i, chunk_text in enumerate(chunks):
                chunk_entry = entry.copy()
                chunk_entry['content'] = chunk_text
                chunk_entry['chunk_index'] = i
                chunk_entry['total_chunks'] = len(chunks)

                if len(chunks) > 1:
                    chunk_entry['title'] = f"{entry.get('title', '')} (part {i+1}/{len(chunks)})"

                chunked.append(chunk_entry)

    return chunked


def main():
    base_dir = Path('/home/usamimira/PHY-LLM/CC_Solver/textbook')

    books = {
        'ahlfors': 'ahlfors_output/ahlfors.md',
        'cft': 'cft_output/cft.md',
        'special_functions': 'special_functions_output/special_functions.md',
    }

    all_sections = []
    all_examples = []

    print("Processing new textbooks...\n")

    for book_name, md_path_rel in books.items():
        md_path = base_dir / md_path_rel
        print(f"Processing {book_name}...")

        if not md_path.exists():
            print(f"  ⚠️  File not found: {md_path}")
            continue

        sections, examples = extract_sections(md_path, book_name)
        print(f"  Sections: {len(sections)}")
        print(f"  Examples/Exercises: {len(examples)}")

        all_sections.extend(sections)
        all_examples.extend(examples)

    print(f"\nTotal sections: {len(all_sections)}")
    print(f"Total examples/exercises: {len(all_examples)}")

    # Chunk with smart splitting
    print("\nChunking sections (max 2048 tokens, 256 token overlap)...")
    chunked_sections = chunk_entries(all_sections, max_tokens=2048, overlap_tokens=256)
    print(f"  Result: {len(chunked_sections)} chunks")

    print("\nChunking examples (max 2048 tokens, 256 token overlap)...")
    chunked_examples = chunk_entries(all_examples, max_tokens=2048, overlap_tokens=256)
    print(f"  Result: {len(chunked_examples)} chunks")

    # Combine for RAG
    all_chunks = chunked_sections + chunked_examples
    print(f"\nTotal chunks for RAG: {len(all_chunks)}")

    # Save
    output_dir = base_dir / 'merged_new'
    output_dir.mkdir(exist_ok=True)

    with open(output_dir / 'pure_sections.json', 'w', encoding='utf-8') as f:
        json.dump(chunked_sections, f, ensure_ascii=False, indent=2)

    with open(output_dir / 'examples.json', 'w', encoding='utf-8') as f:
        json.dump(chunked_examples, f, ensure_ascii=False, indent=2)

    with open(output_dir / 'chunks_final.json', 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_dir}:")
    print(f"  pure_sections.json: {len(chunked_sections)} chunks")
    print(f"  examples.json: {len(chunked_examples)} chunks")
    print(f"  chunks_final.json: {len(all_chunks)} chunks")

    # Stats
    print("\nChunk size distribution:")
    sizes = [len(c['content']) for c in all_chunks]
    tokens = [estimate_tokens(c['content']) for c in all_chunks]
    print(f"  Min: {min(sizes)} chars ({min(tokens)} tokens)")
    print(f"  Max: {max(sizes)} chars ({max(tokens)} tokens)")
    print(f"  Avg: {sum(sizes)//len(sizes)} chars ({sum(tokens)//len(tokens)} tokens)")

    # Count split entries
    split_sections = sum(1 for c in chunked_sections if c.get('total_chunks', 1) > 1)
    split_examples = sum(1 for c in chunked_examples if c.get('total_chunks', 1) > 1)
    print(f"\nSplit entries:")
    print(f"  Sections: {split_sections} split")
    print(f"  Examples: {split_examples} split")


if __name__ == '__main__':
    main()
