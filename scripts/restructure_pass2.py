#!/usr/bin/env python3
"""Second pass: fix duplicate headings, merge consecutive code blocks,
remove remaining echo text, clean up file-top TOC blocks."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "duplicate_headings_removed": 0,
    "code_blocks_merged": 0,
    "echo_lines_removed": 0,
    "toc_lines_removed": 0,
    "files_modified": 0,
}

# Known echo patterns to remove (short standalone repeated section markers)
ECHO_PATTERNS = [
    re.compile(r"^Transformations?\s*\(좌표\s*변환\)\s*$"),
    re.compile(r"^tf2\s*소개\s*$"),
    re.compile(r"^✓\s*$"),  # standalone checkmark
    re.compile(r"^ROS2\s*CLI\s*$"),
    re.compile(r"^ROS2\s*CLI\s*(사용법|실행\s*명령어|정보\s*명령어|기능\s*보조?\s*명령어|실습)\s*$"),
    re.compile(r"^DDS의?\s*QoS\s*$"),
    re.compile(r"^DDS\s*$"),
    re.compile(r"^QoS\s*$"),
    re.compile(r"^rmw_qos_profile\s*$"),
    re.compile(r"^Component\s*$"),
    re.compile(r"^Lifecycle\s*$"),
    re.compile(r"^Security\s*$"),
    re.compile(r"^ros2\s*(run|launch|pkg|node|topic|service)\s*$"),
    re.compile(r"^Intra-process\s*communication\s*$", re.IGNORECASE),
    re.compile(r"^신규\s*ROS2\s*cli\s*작성법\s*$"),
    re.compile(r"^두산\s*로봇\s*팔과\s*시뮬레이션\s*실습?\s*$"),
    re.compile(r"^ROS2\s*CLI\s*ROS2\s*CLI.*$"),  # merged echo like "ROS2 CLI ROS2 CLI사용법"
    re.compile(r"^DDS의\s*QoS\s*DDS\s*$"),       # merged echo
    re.compile(r"^ROS2\s*CLI실습\s*$"),
    re.compile(r"^ROS2\s*CLI정보\s*명령어\s*$"),
    re.compile(r"^ROS2\s*CLI기능\s*(보조\s*)?명령어\s*$"),
    re.compile(r"^ROS2\s*CLI실행\s*명령어\s*$"),
    re.compile(r"^ROS2\s*CLI사용법\s*$"),
]


def is_echo_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    for pat in ECHO_PATTERNS:
        if pat.match(stripped):
            return True
    return False


def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    n = len(lines)

    # ── Pass 1: Remove file-top TOC (lines 2-30 that are bullet lists or topic names) ──
    result = []
    in_top_toc = False
    toc_end = 0

    # Detect TOC: after # title, look for a block of bullet/topic lines
    title_line = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("# ") and i < 5:
            title_line = i
            break

    if title_line >= 0:
        # Check lines after title for TOC pattern
        j = title_line + 1
        # Skip blanks
        while j < n and lines[j].strip() == "":
            j += 1
        toc_start = j
        toc_count = 0
        while j < n:
            s = lines[j].strip()
            if s == "":
                j += 1
                continue
            # TOC-like: short topic names, bullet items listing topics
            if (s.startswith("- ") or s.startswith("주제:") or
                re.match(r"^(ROS2?\s|Python|Intra|DDS|QoS|Component|RQt|Lifecycle|Security|Urdf|Gazebo|OpenCV|Lane|Point|Open3D)", s) or
                re.match(r"^\(.+\)$", s)):
                toc_count += 1
                j += 1
            else:
                break
        if toc_count >= 5:
            toc_end = j
            stats["toc_lines_removed"] += toc_count

    # ── Pass 2: Process lines ──
    seen_headings = {}  # heading text -> line number of first occurrence
    i = 0
    in_code_block = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Skip TOC block
        if toc_end > 0 and title_line < i < toc_end:
            i += 1
            continue

        # Track code fences
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Remove echo lines
        if is_echo_line(stripped):
            stats["echo_lines_removed"] += 1
            i += 1
            continue

        # Handle duplicate ### headings (keep first, remove subsequent identical ones)
        m_h3 = re.match(r"^(###\s+.+)$", stripped)
        if m_h3:
            heading_text = m_h3.group(1)
            if heading_text in seen_headings:
                # Check if the next few lines are the same as after first occurrence
                # Just remove the duplicate heading
                stats["duplicate_headings_removed"] += 1
                i += 1
                continue
            else:
                seen_headings[heading_text] = i

        # Merge consecutive ??? example blocks with same topic
        m_adm = re.match(r'^(\?\?\?\s+example\s+"코드 분석:\s*)(.+?)("\s*)$', stripped)
        if m_adm:
            # Check if previous non-blank line is end of another ??? block
            # We want to merge adjacent blocks with similar titles
            base_title = m_adm.group(2).split("–")[0].split("-")[0].strip()

            # Look back: if the immediately preceding ??? block has same base topic, merge
            prev_idx = len(result) - 1
            while prev_idx >= 0 and result[prev_idx].strip() == "":
                prev_idx -= 1

            if prev_idx >= 0:
                prev_line = result[prev_idx].strip()
                # Check if previous content ends an admonition with same base title
                prev_adm = re.match(r'^(\?\?\?\s+example\s+"코드 분석:\s*)(.+?)("\s*)$', prev_line)
                if prev_adm:
                    prev_base = prev_adm.group(2).split("–")[0].split("-")[0].strip()
                    if prev_base == base_title:
                        # Previous is an empty admonition header, remove it and blank lines
                        while len(result) > 0 and (result[-1].strip() == "" or
                               re.match(r'^\?\?\?\s+example', result[-1].strip())):
                            result.pop()
                        stats["code_blocks_merged"] += 1

            result.append(line)
            i += 1
            continue

        result.append(line)
        i += 1

    # ── Pass 3: Clean blank lines ──
    final = []
    blank_count = 0
    for line in result:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                final.append(line)
        else:
            blank_count = 0
            final.append(line)

    new_text = "\n".join(final)
    if new_text != text:
        filepath.write_text(new_text, encoding="utf-8")
        stats["files_modified"] += 1
        return True
    return False


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

    print(f"\n=== Restructure Pass 2 Results ===")
    print(f"  Files modified:             {stats['files_modified']}")
    print(f"  Duplicate headings removed: {stats['duplicate_headings_removed']}")
    print(f"  Code blocks merged:         {stats['code_blocks_merged']}")
    print(f"  Echo lines removed:         {stats['echo_lines_removed']}")
    print(f"  TOC lines removed:          {stats['toc_lines_removed']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
