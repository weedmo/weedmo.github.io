#!/usr/bin/env python3
"""Join broken bullet items - fix PPT line wrapping artifacts.

Two patterns:
  Pattern A: "- text" followed by continuation lines (non-bullet, non-blank)
             → join continuation into the bullet line
  Pattern B: "-" alone on a line, content on next line(s) until next bullet/blank/heading
             → merge into "- content"
"""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "empty_bullets_joined": 0,
    "continuation_joined": 0,
    "files_modified": 0,
}


def is_break_line(s: str) -> bool:
    """Lines that signal end of a bullet's content."""
    if s == "":
        return True
    if s == "-":
        return True
    if s.startswith(("- ", "## ", "# ", "![", "```", "|", "---")):
        return True
    if re.match(r"^\d+\.\s", s):
        return True
    return False


def fix_content(text: str) -> str:
    lines = text.split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Pattern B: bare "-" alone on a line, content on next line(s)
        if stripped == "-" and i + 1 < len(lines):
            content_parts = []
            j = i + 1
            while j < len(lines):
                next_s = lines[j].strip()
                if is_break_line(next_s):
                    break
                content_parts.append(next_s)
                j += 1
            if content_parts:
                joined = "- " + " ".join(content_parts)
                result.append(joined)
                stats["empty_bullets_joined"] += 1
                i = j
                continue
            else:
                # bare "-" with nothing after → skip it
                i += 1
                continue

        # Pattern A: "- text" followed by continuation lines
        if stripped.startswith("- ") and len(stripped) > 2:
            parts = [stripped]
            j = i + 1
            while j < len(lines):
                next_s = lines[j].strip()
                if is_break_line(next_s):
                    break
                parts.append(next_s)
                stats["continuation_joined"] += 1
                j += 1
            result.append(" ".join(parts))
            i = j
            continue

        result.append(line)
        i += 1

    return "\n".join(result)


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

    print("=== Bullet Join Results ===")
    print(f"  Files modified:        {stats['files_modified']}")
    print(f"  Empty bullets joined:  {stats['empty_bullets_joined']}")
    print(f"  Continuations joined:  {stats['continuation_joined']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
