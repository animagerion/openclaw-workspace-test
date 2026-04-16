#!/usr/bin/env python3
"""Split chapters into two halves for subagent translation."""
import sys, os, re

CHAPTERS_DIR = "/home/gerion/.openclaw/workspace/skills/epub-translator/chapters"

def find_split_point(lines):
    """Find natural split point at section number boundaries."""
    # Look for numbered sections like "1. ", "2. ", etc.
    section_lines = []
    for i, line in enumerate(lines):
        m = re.match(r'^(\d+)\.\s', line.strip())
        if m:
            section_lines.append((int(m.group(1)), i))

    if len(section_lines) >= 2:
        # Split at roughly half
        mid = len(section_lines) // 2
        split_idx = section_lines[mid][1]
        return split_idx

    # Fallback: split at line count / 2
    return len(lines) // 2

def split_chapter(filepath):
    filename = os.path.basename(filepath)
    chapter_num = filename.replace("chapter_", "").replace(".txt", "")

    with open(filepath, "r") as f:
        content = f.read()

    # Extract header lines (CHAPTER_TITLE, CHAPTER_NUM, SOURCE_FILE)
    header_lines = []
    body_lines = []
    in_body = False
    for line in content.split("\n"):
        if line.startswith("---"):
            in_body = True
            body_lines.append(line)
        elif not in_body and line.startswith("CHAPTER_"):
            header_lines.append(line)
        elif not in_body:
            header_lines.append(line)
        else:
            body_lines.append(line)

    split_idx = find_split_point(body_lines)
    half1_lines = body_lines[:split_idx]
    half2_lines = body_lines[split_idx:]

    header = "\n".join(header_lines) + "\n"

    half1_content = header + "\n".join(half1_lines)
    half2_content = header + "\n".join(half2_lines)

    half1_path = filepath.replace(".txt", "_half1.txt")
    half2_path = filepath.replace(".txt", "_half2.txt")

    with open(half1_path, "w") as f:
        f.write(half1_content)
    with open(half2_path, "w") as f:
        f.write(half2_content)

    print(f"{filename} -> split at line {split_idx}")
    print(f"  Half1: {len(half1_lines)} lines -> {half1_path}")
    print(f"  Half2: {len(half2_lines)} lines -> {half2_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            split_chapter(f)
    else:
        print("Usage: python3 split_chapters.py <chapter_file>...")
        print("Splits given chapter files into half1 and half2 at natural section boundaries.")
