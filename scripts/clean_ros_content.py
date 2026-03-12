#!/usr/bin/env python3
"""Clean PPT artifacts from ROS markdown files."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"

TARGET_DIRS = ["intro", "basics", "practice", "projects"]

# Patterns to remove (entire lines)
REMOVE_PATTERNS = [
    re.compile(r"^.*ROKEY BOOT CAMP.*$", re.MULTILINE),
    re.compile(r"^.*HUMAN AI ROBOTICS.*$", re.MULTILINE),
    re.compile(r"^\d{1,3}$", re.MULTILINE),          # Bare slide numbers
    re.compile(r"^Contents$", re.MULTILINE),
    re.compile(r"^undefined$", re.MULTILINE),
    re.compile(r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s*\d{4}$", re.MULTILINE),
]

stats = {
    "rokey": 0,
    "human_ai": 0,
    "slide_numbers": 0,
    "bullets_converted": 0,
    "headings_converted": 0,
    "blank_lines_cleaned": 0,
    "files_processed": 0,
}


def clean_content(text: str) -> str:
    # 1. Remove ROKEY BOOT CAMP lines
    text, n = re.subn(r"^.*ROKEY BOOT CAMP.*\n?", "", text, flags=re.MULTILINE)
    stats["rokey"] += n

    # 2. Remove HUMAN AI ROBOTICS lines
    text, n = re.subn(r"^.*HUMAN AI ROBOTICS.*\n?", "", text, flags=re.MULTILINE)
    stats["human_ai"] += n

    # 3. Remove bare slide numbers (1-3 digit numbers on their own line)
    text, n = re.subn(r"^\d{1,3}\s*\n", "", text, flags=re.MULTILINE)
    stats["slide_numbers"] += n

    # 4. Remove "Contents" and "undefined" lines
    text = re.sub(r"^Contents\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"^undefined\s*\n", "", text, flags=re.MULTILINE)

    # 5. Remove date-only header lines like "Apr, 2025"
    text = re.sub(
        r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s*\d{4}\s*\n",
        "",
        text,
        flags=re.MULTILINE,
    )

    # 6. Convert ▪ bullets to markdown list items
    text, n = re.subn(r"^▪\s*", "- ", text, flags=re.MULTILINE)
    stats["bullets_converted"] += n

    # 7. Convert ▶ to ## headings
    text, n = re.subn(r"^▶\s*", "## ", text, flags=re.MULTILINE)
    stats["headings_converted"] += n

    # 8. Collapse 3+ consecutive blank lines to 2
    original_len = len(text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    if len(text) < original_len:
        stats["blank_lines_cleaned"] += 1

    # 9. Strip trailing whitespace on each line
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    return text


def main():
    files_processed = []

    for dir_name in TARGET_DIRS:
        target_dir = DOCS / dir_name
        if not target_dir.exists():
            print(f"  Skipping {dir_name}/ (not found)")
            continue

        for md_file in sorted(target_dir.glob("*.md")):
            original = md_file.read_text(encoding="utf-8")
            cleaned = clean_content(original)

            if cleaned != original:
                md_file.write_text(cleaned, encoding="utf-8")
                files_processed.append(md_file.relative_to(DOCS.parent))
                stats["files_processed"] += 1

    print("=== ROS Content Cleanup Results ===")
    print(f"  Files modified:      {stats['files_processed']}")
    print(f"  ROKEY BOOT CAMP:     {stats['rokey']} lines removed")
    print(f"  HUMAN AI ROBOTICS:   {stats['human_ai']} lines removed")
    print(f"  Slide numbers:       {stats['slide_numbers']} lines removed")
    print(f"  ▪ → list items:      {stats['bullets_converted']} converted")
    print(f"  ▶ → headings:        {stats['headings_converted']} converted")
    print(f"  Blank line cleanup:  {stats['blank_lines_cleaned']} files")
    print()
    for f in files_processed:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
