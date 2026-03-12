#!/usr/bin/env python3
"""Fix Korean spacing in ROS markdown files using kiwipiepy.

Strategy: split lines into Korean-only vs non-Korean segments,
apply kiwi.space() only to Korean segments, then reassemble.
"""

import re
from pathlib import Path
from kiwipiepy import Kiwi

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

kiwi = Kiwi()

stats = {"lines_fixed": 0, "files_modified": 0}

# Post-fix: kiwi over-splits these compound words/proper nouns
# Format: (wrong_split, correct) - applied after kiwi spacing
POST_FIX = [
    ("단 방향", "단방향"),
    ("양 방향", "양방향"),
    ("콜 백", "콜백"),
    ("프레임 워크", "프레임워크"),
    ("사출 물", "사출물"),
    ("로 섬", "로섬"),
    ("아 시모", "아시모"),
    ("아 이 보", "아이보"),
    ("아 이보", "아이보"),
    ("유 니 메이트", "유니메이트"),
    ("유 니메이트", "유니메이트"),
    ("유니 메이트", "유니메이트"),
    ("차 펙", "차펙"),
    ("터 미네이터", "터미네이터"),
    ("매트 릭스", "매트릭스"),
    ("로보 타", "로보타"),
    ("이벤트 루프", "이벤트루프"),
]

# Segment splitter: Korean text vs everything else
# Korean block = consecutive Korean chars + some punctuation that's part of Korean text
SEGMENT_RE = re.compile(r"([가-힣][가-힣,.\s]*[가-힣]|[가-힣])")

SKIP_PATTERNS = [
    re.compile(r"^\s*$"),
    re.compile(r"^\s*#"),
    re.compile(r"^\s*!\["),
    re.compile(r"^\s*```"),
    re.compile(r"^\s*\|"),
    re.compile(r"^\s*---"),
    re.compile(r"^<"),
]


def should_skip(line: str) -> bool:
    for p in SKIP_PATTERNS:
        if p.match(line):
            return True
    return False


def space_korean_segment(text: str) -> str:
    """Apply kiwi spacing to a pure-Korean text segment."""
    if len(text.strip()) <= 1:
        return text
    result = kiwi.space(text)
    # Clean double spaces
    result = re.sub(r"  +", " ", result)
    return result


def fix_line(line: str) -> str:
    """Fix spacing in a single line by processing Korean segments only."""
    # Extract list prefix
    prefix = ""
    content = line
    m = re.match(r"^(\s*- )", line)
    if m:
        prefix = m.group(1)
        content = line[len(prefix):]

    if not content.strip():
        return line

    # Check if there's any Korean
    if not re.search(r"[가-힣]", content):
        return line

    # Split into segments: find all Korean chunks and non-Korean chunks
    parts = []
    last_end = 0

    for match in SEGMENT_RE.finditer(content):
        start, end = match.span()
        # Add non-Korean part before this match
        if start > last_end:
            parts.append(("other", content[last_end:start]))
        # Add Korean part
        korean_text = match.group(0)
        if len(korean_text.replace(" ", "").replace(",", "").replace(".", "")) >= 4:
            # Only apply spacing to segments with 4+ Korean chars
            spaced = space_korean_segment(korean_text)
            parts.append(("korean", spaced))
        else:
            parts.append(("korean", korean_text))
        last_end = end

    # Add remaining non-Korean part
    if last_end < len(content):
        parts.append(("other", content[last_end:]))

    result = "".join(p[1] for p in parts)
    result = re.sub(r"  +", " ", result)

    # Apply post-fix dictionary
    for wrong, correct in POST_FIX:
        result = result.replace(wrong, correct)

    final = prefix + result

    if final != line:
        stats["lines_fixed"] += 1

    return final


def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    new_lines = []
    in_code_block = False
    changed = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block or should_skip(line):
            new_lines.append(line)
            continue

        fixed = fix_line(line)
        if fixed != line:
            changed = True
        new_lines.append(fixed)

    if changed:
        filepath.write_text("\n".join(new_lines), encoding="utf-8")
        stats["files_modified"] += 1

    return changed


def main():
    files_modified = []

    for dir_name in TARGET_DIRS:
        target_dir = DOCS / dir_name
        if not target_dir.exists():
            continue

        for md_file in sorted(target_dir.glob("*.md")):
            print(f"  Processing: {md_file.name}...", flush=True)
            if process_file(md_file):
                files_modified.append(md_file.relative_to(DOCS.parent))

    print(f"\n=== Spacing Fix Results ===")
    print(f"  Files modified:  {stats['files_modified']}")
    print(f"  Lines fixed:     {stats['lines_fixed']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
