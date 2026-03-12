#!/usr/bin/env python3
"""Fix missing line breaks in ROS markdown files migrated from PPT."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "heading_breaks": 0,
    "image_breaks": 0,
    "bullet_converts": 0,
    "list_breaks": 0,
    "duplicate_headers": 0,
    "files_modified": 0,
}


def fix_content(text: str) -> str:
    lines = text.split("\n")
    result = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        prev = result[-1].strip() if result else ""
        prev2 = result[-2].strip() if len(result) >= 2 else ""

        # 1. Convert remaining • bullets to - list items
        if stripped.startswith("•"):
            new_line = line.replace("•", "-", 1)
            stats["bullet_converts"] += 1
            line = new_line
            stripped = line.strip()

        # 2. Ensure blank line before ## headings
        if stripped.startswith("## ") and prev != "" and not prev.startswith("#"):
            result.append("")
            stats["heading_breaks"] += 1

        # 3. Ensure blank line before image lines
        if stripped.startswith("![") and prev != "":
            result.append("")
            stats["image_breaks"] += 1

        # 4. Ensure blank line after image lines (look ahead)
        if prev.startswith("![") and prev.endswith(")") and stripped != "" and not stripped.startswith("!["):
            result.append("")
            stats["image_breaks"] += 1

        # 5. Ensure blank line before list items if prev line is not a list item or blank
        if stripped.startswith("- ") and prev != "" and not prev.startswith("- ") and not prev.startswith("#"):
            result.append("")
            stats["list_breaks"] += 1

        # 6. Ensure blank line before numbered items (1. 2. etc) if prev is not numbered or blank
        if re.match(r"^\d+\.\s", stripped) and prev != "" and not re.match(r"^\d+\.\s", prev) and not prev.startswith("#"):
            result.append("")
            stats["list_breaks"] += 1

        result.append(line)

    text = "\n".join(result)

    # 7. Remove duplicate slide headers - lines that appear as repeated section titles
    # Pattern: short Korean-only title lines that repeat throughout the file
    # e.g., "토픽프로그래밍\n토픽퍼블리셔코드" appearing multiple times as slide headers
    # Remove lines that are exact duplicates of a ## heading (without the ##)
    headings = set()
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("## "):
            headings.add(s[3:].strip())

    new_lines = []
    for line in text.split("\n"):
        s = line.strip()
        # Skip lines that are exact duplicates of heading text (slide title echoes)
        if s in headings and not line.strip().startswith("##"):
            stats["duplicate_headers"] += 1
            continue
        new_lines.append(line)
    text = "\n".join(new_lines)

    # 8. Collapse 3+ consecutive blank lines to 2
    text = re.sub(r"\n{4,}", "\n\n\n", text)

    # 9. Strip trailing whitespace
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    return text


def main():
    files_modified = []

    for dir_name in TARGET_DIRS:
        target_dir = DOCS / dir_name
        if not target_dir.exists():
            continue

        for md_file in sorted(target_dir.glob("*.md")):
            original = md_file.read_text(encoding="utf-8")
            fixed = fix_content(original)

            if fixed != original:
                md_file.write_text(fixed, encoding="utf-8")
                files_modified.append(md_file.relative_to(DOCS.parent))
                stats["files_modified"] += 1

    print("=== Line Break Fix Results ===")
    print(f"  Files modified:       {stats['files_modified']}")
    print(f"  Heading breaks added: {stats['heading_breaks']}")
    print(f"  Image breaks added:   {stats['image_breaks']}")
    print(f"  Bullet converts:      {stats['bullet_converts']}")
    print(f"  List breaks added:    {stats['list_breaks']}")
    print(f"  Duplicate headers:    {stats['duplicate_headers']} removed")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
