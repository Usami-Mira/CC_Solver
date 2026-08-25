#!/usr/bin/env python3
"""
Merge OCR output parts into single files per book.
Combines full.md from all parts in order.
"""

import os
from pathlib import Path


def merge_book_parts(output_dir: Path, book_name: str):
    """Merge all part_*/full.md files into a single {book_name}.md file."""

    # Find all part directories
    part_dirs = sorted([d for d in output_dir.iterdir()
                       if d.is_dir() and d.name.startswith('part_')])

    if not part_dirs:
        print(f"  ⚠️  No part directories found in {output_dir}")
        return

    print(f"  Found {len(part_dirs)} parts")

    # Merge full.md from each part
    merged_content = []
    for part_dir in part_dirs:
        full_md = part_dir / 'full.md'
        if full_md.exists():
            print(f"    ✓ {part_dir.name}")
            with open(full_md, 'r', encoding='utf-8') as f:
                content = f.read()
            merged_content.append(f"\n\n<!-- {part_dir.name} -->\n\n{content}")
        else:
            print(f"    ✗ {part_dir.name} (no full.md)")

    # Write merged file
    output_file = output_dir / f"{book_name}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(merged_content))

    print(f"  ✅ Merged to {output_file}")
    print(f"     Size: {output_file.stat().st_size / 1024:.1f} KB")


def main():
    base_dir = Path('/home/usamimira/PHY-LLM/CC_Solver/textbook')

    books = {
        'ahlfors': 'ahlfors_output',
        'cft': 'cft_output',
        'special_functions': 'special_functions_output',
    }

    print("Merging OCR output parts...\n")

    for book_name, output_dir_name in books.items():
        output_dir = base_dir / output_dir_name
        print(f"Processing {book_name}...")

        if not output_dir.exists():
            print(f"  ⚠️  Directory not found: {output_dir}")
            continue

        merge_book_parts(output_dir, book_name)
        print()

    print("✅ All books merged!")


if __name__ == '__main__':
    main()
