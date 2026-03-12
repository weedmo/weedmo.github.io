#!/usr/bin/env python3
"""Restructure ROS content: remove tiny images, add section headings,
separate code review sections, clean up PPT artifacts."""

import re
from pathlib import Path
from PIL import Image

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
ASSETS = Path(__file__).resolve().parent.parent / "docs" / "assets" / "images" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "tiny_images_removed": 0,
    "headings_added": 0,
    "junk_lines_removed": 0,
    "code_sections_wrapped": 0,
    "files_modified": 0,
}

# ── Tiny image detection ──────────────────────────────────────────────

def is_tiny_image(img_path: Path, max_bytes=2048, max_dim=100) -> bool:
    """Check if an image is a tiny PPT artifact (icon, bullet, text fragment)."""
    if not img_path.exists():
        return False
    size = img_path.stat().st_size
    if size > max_bytes:
        return False
    try:
        with Image.open(img_path) as img:
            w, h = img.size
            return w < max_dim and h < max_dim
    except Exception:
        return False


# ── Junk line patterns ────────────────────────────────────────────────

JUNK_PATTERNS = [
    re.compile(r"^ROS-?\s*2\s*프로그래밍\s*실습\s*$"),
    re.compile(r"^ROS-?\s*2\s*프로그래밍\s*실습\s*강의\s*자료\s*$"),
    re.compile(r"^\d+\s*[~～]\s*\d+\s*차시\s*$"),         # "1 ~ 4 차시"
    re.compile(r"^수고하셨습니다\.?\s*$"),
    re.compile(r"^감사합니다\.?\s*$"),
    re.compile(r"^Q\s*&\s*A\s*$", re.IGNORECASE),
    re.compile(r"^ROS2\s*프로그래밍\s*실습\s*목차\s*$"),
]

def is_junk_line(line: str) -> bool:
    """Check if a line is a PPT junk artifact to remove."""
    stripped = line.strip()
    if not stripped:
        return False
    for pat in JUNK_PATTERNS:
        if pat.match(stripped):
            return True
    return False


# ── Section heading detection for practice files ──────────────────────

# Major topic titles that should become ## headings
MAJOR_TOPICS = {
    # practice-01-04
    "ROS2 CLI 사용법": "ROS2 CLI 사용법",
    "ROS2 CLI": None,  # Skip standalone - too common as echo
    "ROS2 CLI 실행 명령어": "ROS2 CLI 실행 명령어",
    "ROS2 CLI 정보 명령어": "ROS2 CLI 정보 명령어",
    "ROS2 CLI 기능 보조 명령어": "ROS2 CLI 기능 보조 명령어",
    "Intra-Process Communication": "Intra-Process Communication",
    "Intra-process communication": "Intra-Process Communication",
    "QoS programming": "QoS 프로그래밍",
    "rmw_qos_profile": "rmw_qos_profile",
    "Component": "Component",
    "RQt 플러그인 스타일의 장점": "RQt 플러그인",
    "Lifecycle": "Lifecycle",
    "Security": "Security",
    # practice-04-05
    "Transformations(좌표 변환)": "좌표 변환 (Transformations)",
    "URDF": "URDF",
    # practice-05-07
    "두산 로봇 팔과 시뮬레이션 실습": "두산 로봇 팔과 시뮬레이션",
    "OpenCV와 ROS2연동": "OpenCV와 ROS2 연동",
    "OpenCV와 ROS2 연동": "OpenCV와 ROS2 연동",
    "Lane Detection": "Lane Detection",
    "Open3D": "Open3D",
}

# Sub-topic patterns that should become ### headings
SUBTOPIC_RE = re.compile(r"^✓\s*(.+)$")

# Code review title patterns
CODE_REVIEW_PATTERNS = [
    re.compile(r"코드\s*분석"),
    re.compile(r"코드\s*확인"),
    re.compile(r"[–—-]\s*코드\s*$"),
    re.compile(r"\.py\s*(분석|설정|코드)"),
    re.compile(r"setup\.py"),
    re.compile(r"__init__\.py"),
]

def is_code_review_title(text: str) -> bool:
    """Check if a line is a code review/analysis section title."""
    for pat in CODE_REVIEW_PATTERNS:
        if pat.search(text):
            return True
    return False


# ── Repeated echo detection ───────────────────────────────────────────

def detect_echo_lines(lines: list) -> set:
    """Find lines that are just echo/repetition of nearby heading text."""
    echo_indices = set()
    heading_texts = set()

    for i, line in enumerate(lines):
        s = line.strip()
        # Collect known heading-like text patterns (short standalone lines)
        m = re.match(r"^(#{1,3})\s+(.+)$", s)
        if m:
            heading_texts.add(m.group(2).replace(" ", ""))

    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith(("#", "!", "-", "|", "<", "`", "```")):
            continue
        # Short standalone text that matches a heading (echo from PPT)
        normalized = s.replace(" ", "")
        if normalized in heading_texts and len(s) < 50:
            prev_blank = (i == 0 or lines[i-1].strip() == "")
            next_blank = (i+1 >= len(lines) or lines[i+1].strip() == "")
            if prev_blank or next_blank:
                echo_indices.add(i)

    return echo_indices


# ── Main processing ──────────────────────────────────────────────────

def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    result = []
    changed = False
    n = len(lines)

    # Detect echo lines
    echo_indices = detect_echo_lines(lines)

    # Track which ## headings we've already added (avoid duplicates)
    added_headings = set()

    i = 0
    in_code_block = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Skip junk lines
        if is_junk_line(stripped):
            stats["junk_lines_removed"] += 1
            changed = True
            i += 1
            continue

        # Remove tiny image references
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if m:
            img_rel = m.group(2)
            img_abs = (filepath.parent / img_rel).resolve()
            if is_tiny_image(img_abs):
                stats["tiny_images_removed"] += 1
                changed = True
                i += 1
                continue

        # Convert major topic titles to ## headings
        if stripped in MAJOR_TOPICS and MAJOR_TOPICS[stripped] is not None:
            heading_text = MAJOR_TOPICS[stripped]
            # Only add if not already a heading and we haven't added this one yet
            if heading_text not in added_headings:
                # Check context: should be preceded by blank or start of section
                prev_blank = (i == 0 or lines[i-1].strip() == "")
                if prev_blank:
                    result.append(f"## {heading_text}")
                    added_headings.add(heading_text)
                    stats["headings_added"] += 1
                    changed = True
                    i += 1
                    continue

        # Convert ✓ sub-topics to ### headings
        m_sub = SUBTOPIC_RE.match(stripped)
        if m_sub:
            sub_title = m_sub.group(1).strip()
            if is_code_review_title(sub_title):
                # Code review section - use collapsible admonition
                result.append(f'??? example "코드 분석: {sub_title}"')
                result.append("")
                stats["code_sections_wrapped"] += 1
                changed = True
                i += 1
                # Collect content until next section break
                while i < n:
                    s = lines[i].strip()
                    # Stop at next ✓ title, major topic, or ## heading
                    if (SUBTOPIC_RE.match(s) or
                        s in MAJOR_TOPICS or
                        s.startswith("## ") or
                        s.startswith("# ")):
                        break
                    # Indent content for admonition
                    if lines[i].strip():
                        result.append(f"    {lines[i]}")
                    else:
                        result.append("")
                    i += 1
                result.append("")
                continue
            else:
                # Regular sub-topic → ### heading
                result.append(f"### {sub_title}")
                stats["headings_added"] += 1
                changed = True
                i += 1
                continue

        # Remove echo lines (PPT repetitions)
        if i in echo_indices:
            # Double-check: only remove if it's a short standalone text
            if len(stripped) < 50 and not stripped.startswith(("#", "!", "-", "|")):
                stats["junk_lines_removed"] += 1
                changed = True
                i += 1
                continue

        result.append(line)
        i += 1

    if changed:
        # Clean excessive blank lines (3+ → 2)
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
        filepath.write_text(new_text, encoding="utf-8")
        stats["files_modified"] += 1
        return True
    return False


def main():
    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Requires Pillow. Install with: pip install Pillow")
        return

    files_modified = []

    for dir_name in TARGET_DIRS:
        target_dir = DOCS / dir_name
        if not target_dir.exists():
            continue

        for md_file in sorted(target_dir.glob("*.md")):
            print(f"  Processing: {md_file.name}...", flush=True)
            if process_file(md_file):
                files_modified.append(md_file.relative_to(DOCS.parent))

    print(f"\n=== Content Restructuring Results ===")
    print(f"  Files modified:         {stats['files_modified']}")
    print(f"  Tiny images removed:    {stats['tiny_images_removed']}")
    print(f"  Headings added:         {stats['headings_added']}")
    print(f"  Junk lines removed:     {stats['junk_lines_removed']}")
    print(f"  Code sections wrapped:  {stats['code_sections_wrapped']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
