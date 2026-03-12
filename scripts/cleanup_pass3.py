#!/usr/bin/env python3
"""Third-pass cleanup: remove PPT slide breadcrumbs, fix titles, remove sub-TOCs."""

import re
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "titles_fixed": 0,
    "breadcrumbs_removed": 0,
    "sub_tocs_removed": 0,
    "tags_removed": 0,
    "files_modified": 0,
}

# Known breadcrumb phrases from PPT slides (plain text, not ## headings)
# These appear as navigation breadcrumbs between sections
BREADCRUMB_PHRASES = {
    # Intro course breadcrumbs
    "ROS2 프로그래밍이란?",
    "토픽 프로그래밍",
    "토픽퍼블리셔코드",
    "토픽서브스크라이버코드",
    "인터페이스 프로그래밍",
    "인터페이스 패키지",
    "서비스 프로그래밍",
    "서비스프로그래밍",
    "서비스서버코드",
    "서비스클라이언트코드",
    "액션 프로그래밍",
    "액션프로그래밍",
    "액션서버코드",
    "액션클라이언트코드",
    "Launch 프로그래밍",
    "토픽 프로그래밍 토픽퍼블리셔코드",
    "토픽 프로그래밍 토픽서브스크라이버코드",
    "서비스 프로그래밍 서비스서버코드",
    "서비스 프로그래밍 서비스클라이언트코드",
    "액션 프로그래밍 액션서버코드",
    "액션 프로그래밍 액션클라이언트코드",
    "인터페이스프로그래밍(응용_1)",
    "인터페이스프로그래밍(응용_2)",
    "인터페이스 프로그래밍(응용_1)",
    "인터페이스 프로그래밍(응용_2)",
    # rclpy
    "rclpy",
    "rclpy 란?",
    "rclpy 정의",
    # Basics breadcrumbs
    "로봇의 역사",
    "로봇의 어원",
    "로봇의 발전",
    "진짜 로봇의 탄생",
    "로봇의 종류",
    "컴퓨터 구조",
    "리눅스와 운영 체계",
    "리눅스 CLI",
    "네트워크와 통신",
    "센서 기초",
    "로봇 기초",
    "ROS2 소개",
    "ROS2 소개 및 활용",
    "Python을 이용한 패키지 생성",
    "Python을 이용한 패키지 생성 실습",
    # Practice/Projects breadcrumbs
    "tf2",
    "URDF",
    "로봇의 시각적 모델 만들기",
}

# Patterns with ㅡ separator (PPT sub-titles like "Message ㅡTopic")
DASH_SUBTITLE_RE = re.compile(r"^.+\s*ㅡ\s*.+$")

# Bracket tags like [Topic], [Service], [Action]
TAG_RE = re.compile(r"^\[(Topic|Service|Action|Parameter|Request|Response)\]\s*$")

# Title mapping for # headings
TITLE_MAP = {
    "강의_3기_ROS2입문_1차시": "ROS2 입문 1차시 - 프로그래밍 기초",
    "강의_3기_ROS2입문_2차시": "ROS2 입문 2차시 - 인터페이스 패키지",
    "강의_3기_ROS2입문_3차시": "ROS2 입문 3차시 - 인터페이스 프로그래밍 (1)",
    "강의_3기_ROS2입문_4차시": "ROS2 입문 4차시 - 인터페이스 프로그래밍 (2)",
    "강의_3기_ROS2입문_5차시": "ROS2 입문 5차시 - rclpy 이해",
    "강의_3기_ROS2입문_6차시": "ROS2 입문 6차시 - ROS2 응용",
    "강의_3기_ROS2입문_7차시": "ROS2 입문 7차시 - ROS2 복습 (1)",
    "강의_3기_ROS2입문_8차시": "ROS2 입문 8차시 - ROS2 복습 (2)",
    "강의_3기_ROS2입문_9차시": "ROS2 입문 9차시 - ROS2 복습 (3)",
    "강의_3기_ROS2_기초_1차시": "ROS2 기초 1차시 - 로봇과 리눅스",
    "강의_3기_ROS2_기초_2차시": "ROS2 기초 2차시 - 네트워크와 프로그래밍",
    "강의_3기_ROS2_기초_3차시": "ROS2 기초 3차시 - 센서와 ROS2 소개",
    "강의_3기_ROS2_기초_4차시": "ROS2 기초 4차시 - ROS2 실습",
    "강의_3기_ROS2_기초_5차시": "ROS2 기초 5차시 - Topic, Service, Action",
    "강의_3기_ROS2_실습_1_4차시": "ROS2 실습 1~4차시",
    "강의_3기_ROS2_실습_4_5차시": "ROS2 실습 4~5차시 - TF2와 URDF",
    "강의_3기_ROS2_실습_5_7차시": "ROS2 실습 5~7차시",
}


def is_breadcrumb(line: str, heading_texts: set) -> bool:
    """Check if a plain text line is a PPT breadcrumb."""
    stripped = line.strip()
    if not stripped:
        return False
    # Exact match with known breadcrumbs
    if stripped in BREADCRUMB_PHRASES:
        return True
    # Normalized match (no spaces)
    normalized = stripped.replace(" ", "")
    for phrase in BREADCRUMB_PHRASES:
        if normalized == phrase.replace(" ", ""):
            return True
    # Check if it matches an existing ## heading text (slide echo)
    if normalized in heading_texts and len(stripped) < 50:
        return True
    return False


def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    result = []
    n = len(lines)

    # Collect ## heading texts for echo detection
    heading_texts = set()
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m:
            heading_texts.add(m.group(1).replace(" ", ""))

    i = 0
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fix # title
        m = re.match(r"^#\s+(.+)$", stripped)
        if m and m.group(1) in TITLE_MAP:
            result.append(f"# {TITLE_MAP[m.group(1)]}")
            stats["titles_fixed"] += 1
            i += 1
            continue

        # Remove standalone course subtitle lines (like "ROS2 프로그래밍 입문")
        if re.match(r"^ROS2\s+(프로그래밍\s+입문|기초)\s*$", stripped):
            stats["breadcrumbs_removed"] += 1
            i += 1
            continue

        # Remove sub-TOC blocks: numbered lists right after ## heading
        # Pattern: ## Heading\n1. item\n2. item\n...
        if stripped.startswith("## "):
            result.append(line)
            i += 1
            # Look ahead for sub-TOC (numbered list immediately after heading)
            # Skip blank lines
            while i < n and lines[i].strip() == "":
                result.append(lines[i])
                i += 1
            # Check for numbered TOC
            toc_start = i
            toc_count = 0
            while i < n and re.match(r"^\d+\.\s+\S", lines[i].strip()):
                toc_count += 1
                i += 1
            if toc_count >= 2:
                # It's a sub-TOC, remove it
                stats["sub_tocs_removed"] += toc_count
            else:
                # Not a sub-TOC, put lines back
                i = toc_start
            continue

        # Remove breadcrumb lines
        if is_breadcrumb(stripped, heading_texts):
            # Don't remove if it's a heading, bullet, image, etc.
            if not stripped.startswith(("#", "-", "!", "`", "|", "<")):
                stats["breadcrumbs_removed"] += 1
                i += 1
                continue

        # Remove ㅡ sub-titles (like "Message ㅡTopic")
        if DASH_SUBTITLE_RE.match(stripped) and "ㅡ" in stripped and len(stripped) < 40:
            stats["breadcrumbs_removed"] += 1
            i += 1
            continue

        # Remove bracket tags
        if TAG_RE.match(stripped):
            stats["tags_removed"] += 1
            i += 1
            continue

        # Remove standalone numbered items that are TOC remnants at file top
        if i < 10 and re.match(r"^\d+\.\s+.+$", stripped) and len(stripped) < 60:
            # Check if this is an isolated numbered item (not part of content list)
            prev_is_blank = (i == 0 or lines[i - 1].strip() == "")
            next_is_blank = (i + 1 >= n or lines[i + 1].strip() == "")
            if prev_is_blank and next_is_blank:
                stats["sub_tocs_removed"] += 1
                i += 1
                continue

        result.append(line)
        i += 1

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

    print(f"\n=== Cleanup Pass 3 Results ===")
    print(f"  Files modified:        {stats['files_modified']}")
    print(f"  Titles fixed:          {stats['titles_fixed']}")
    print(f"  Breadcrumbs removed:   {stats['breadcrumbs_removed']}")
    print(f"  Sub-TOCs removed:      {stats['sub_tocs_removed']}")
    print(f"  Tags removed:          {stats['tags_removed']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
