#!/usr/bin/env python3
"""Second-pass cleanup for ROS markdown files.

Handles:
1. Non-functional TOC sections (전체 목차, 훈련 일정, numbered TOC lists)
2. Slide sub-header echoes (plain text repeating ## heading content)
3. Orphan subtitle lines (차시 subtitles without ##)
4. Re-run spacing verification with kiwipiepy
"""

import re
from pathlib import Path
from kiwipiepy import Kiwi

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

kiwi = Kiwi()

stats = {
    "toc_blocks_removed": 0,
    "schedule_blocks_removed": 0,
    "slide_echoes_removed": 0,
    "spacing_lines_fixed": 0,
    "files_modified": 0,
}


# === PHASE 1: Remove non-functional TOC and schedule blocks ===

def remove_toc_and_schedule(lines: list[str]) -> list[str]:
    """Remove non-functional TOC blocks and training schedule blocks."""
    result = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Pattern: "전체 목차(N차시)" followed by ## headings that are just TOC
        if re.match(r"^전체\s*목차", stripped):
            stats["toc_blocks_removed"] += 1
            i += 1
            # Skip blank lines
            while i < n and lines[i].strip() == "":
                i += 1
            # Skip consecutive ## lines that are TOC entries (no content after)
            while i < n:
                s = lines[i].strip()
                if s.startswith("## ") and i + 1 < n and (
                    lines[i + 1].strip().startswith("## ") or
                    lines[i + 1].strip() == "" and i + 2 < n and lines[i + 2].strip().startswith("## ")
                ):
                    i += 1
                    continue
                # Last ## in the TOC sequence
                if s.startswith("## ") and i + 1 < n and not lines[i + 1].strip().startswith("## "):
                    # Check if this is the last TOC entry (next non-blank is not ##)
                    j = i + 1
                    while j < n and lines[j].strip() == "":
                        j += 1
                    if j < n and not lines[j].strip().startswith("## "):
                        i += 1  # skip this last TOC ##
                        break
                break
            continue

        # Pattern: "훈련 일정" schedule block
        if re.match(r"^훈련\s*일정", stripped):
            stats["schedule_blocks_removed"] += 1
            i += 1
            # Skip until we hit a real content section (non-list, non-blank, not a schedule item)
            # Schedule items typically: "오전", "오후", "N차시", "- item"
            while i < n:
                s = lines[i].strip()
                # End of schedule: empty line followed by non-schedule content
                if s == "":
                    # Look ahead for content
                    j = i + 1
                    while j < n and lines[j].strip() == "":
                        j += 1
                    if j < n:
                        next_s = lines[j].strip()
                        # If next content is not a schedule-like line, stop
                        if not re.match(r"^(오전|오후|\d+차시)", next_s) and not next_s.startswith("- "):
                            i = j
                            break
                i += 1
            continue

        # Pattern: "ROS2 프로그래밍 입문(N차시)" or "ROS2 기초-N차시" standalone subtitle
        if re.match(r"^ROS2\s+(프로그래밍\s+입문|기초)\s*[\-\(]?\s*\d+차시", stripped):
            stats["slide_echoes_removed"] += 1
            i += 1
            continue

        # Pattern: Bare numbered TOC like "1. 제목\n2. 제목\n3. 제목" at file start
        # Only if it looks like a TOC (multiple consecutive numbered items without real content)
        if re.match(r"^\d+\.\s+\S", stripped):
            # Check if this is part of a TOC block (3+ consecutive numbered items)
            j = i
            numbered_count = 0
            while j < n:
                s = lines[j].strip()
                if re.match(r"^\d+\.\s+\S", s):
                    numbered_count += 1
                    j += 1
                elif s == "":
                    j += 1
                else:
                    break
            # Only remove if it's 3+ items AND the next real content starts with ##
            if numbered_count >= 3:
                # Check what follows
                k = j
                while k < n and lines[k].strip() == "":
                    k += 1
                if k < n and lines[k].strip().startswith("## "):
                    stats["toc_blocks_removed"] += 1
                    i = j
                    continue

        result.append(line)
        i += 1

    return result


# === PHASE 2: Remove slide sub-header echoes ===

def remove_slide_echoes(lines: list[str]) -> list[str]:
    """Remove plain text lines that just echo the ## heading above or below."""
    result = []
    n = len(lines)

    # Collect all ## heading texts for matching
    heading_texts = set()
    for line in lines:
        m = re.match(r"^##\s+(.+)$", line.strip())
        if m:
            # Normalize: remove spaces for matching
            heading_texts.add(m.group(1).replace(" ", ""))

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip blanks, headings, bullets, images, code blocks, etc.
        if (stripped == "" or stripped.startswith("#") or
            stripped.startswith("- ") or stripped.startswith("![") or
            stripped.startswith("```") or stripped.startswith("|") or
            stripped.startswith("<") or stripped.startswith("[") or
            re.match(r"^\d+\.\s", stripped)):
            result.append(line)
            continue

        # Check if this plain text line matches a heading (slide echo)
        normalized = stripped.replace(" ", "")
        if normalized in heading_texts and len(stripped) < 40:
            # Verify it's between sections (near a ## heading)
            stats["slide_echoes_removed"] += 1
            continue

        # Pattern: "섹션명\n소제목" where 소제목 echoes a heading
        # e.g., "토픽 프로그래밍\n토픽퍼블리셔코드" - remove both if they match headings
        if normalized in heading_texts and len(stripped) < 50:
            stats["slide_echoes_removed"] += 1
            continue

        result.append(line)

    return result


# === PHASE 3: Korean spacing fix (re-run) ===

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
    ("빌 드", "빌드"),
    ("컴 파일", "컴파일"),
    ("시뮬레 이 션", "시뮬레이션"),
    ("시뮬레 이션", "시뮬레이션"),
    ("네 이게 이 션", "네이게이션"),
    ("네 이게이션", "네이게이션"),
    ("네이게 이션", "네이게이션"),
    ("퍼 블 리 셔", "퍼블리셔"),
    ("퍼 블리셔", "퍼블리셔"),
    ("퍼블 리셔", "퍼블리셔"),
    ("서브 스 크 라이브", "서브스크라이브"),
    ("서브 스크라이브", "서브스크라이브"),
    ("서브스 크라이브", "서브스크라이브"),
    ("서브 스 크라 이브", "서브스크라이브"),
    ("서브스크 라이브", "서브스크라이브"),
    ("서브 스크라 이버", "서브스크라이버"),
    ("서브스크라 이버", "서브스크라이버"),
    ("서브 스 크라이버", "서브스크라이버"),
    ("서브스 크라이버", "서브스크라이버"),
    ("래 핑", "래핑"),
    ("그리 퍼", "그리퍼"),
    ("브로드 캐스터", "브로드캐스터"),
    ("브로드 캐스트", "브로드캐스트"),
    ("파라메터", "파라미터"),
    ("반지 름", "반지름"),
    ("투명 도", "투명도"),
]


def should_skip(line: str) -> bool:
    for p in SKIP_PATTERNS:
        if p.match(line):
            return True
    return False


def space_korean_segment(text: str) -> str:
    if len(text.strip()) <= 1:
        return text
    result = kiwi.space(text)
    result = re.sub(r"  +", " ", result)
    return result


def fix_spacing_line(line: str) -> str:
    prefix = ""
    content = line
    m = re.match(r"^(\s*- )", line)
    if m:
        prefix = m.group(1)
        content = line[len(prefix):]

    if not content.strip():
        return line
    if not re.search(r"[가-힣]", content):
        return line

    parts = []
    last_end = 0

    for match in SEGMENT_RE.finditer(content):
        start, end = match.span()
        if start > last_end:
            parts.append(("other", content[last_end:start]))
        korean_text = match.group(0)
        if len(korean_text.replace(" ", "").replace(",", "").replace(".", "")) >= 4:
            spaced = space_korean_segment(korean_text)
            parts.append(("korean", spaced))
        else:
            parts.append(("korean", korean_text))
        last_end = end

    if last_end < len(content):
        parts.append(("other", content[last_end:]))

    result = "".join(p[1] for p in parts)
    result = re.sub(r"  +", " ", result)

    for wrong, correct in POST_FIX:
        result = result.replace(wrong, correct)

    final = prefix + result

    if final != line:
        stats["spacing_lines_fixed"] += 1

    return final


# === PHASE 4: Clean excessive blank lines ===

def clean_blank_lines(lines: list[str]) -> list[str]:
    """Collapse 3+ consecutive blank lines to 2."""
    result = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= 2:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    return result


# === Main processing ===

def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Phase 1: Remove TOC and schedule blocks
    lines = remove_toc_and_schedule(lines)

    # Phase 2: Remove slide echoes
    lines = remove_slide_echoes(lines)

    # Phase 3: Fix spacing (only non-code, non-special lines)
    new_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue
        if in_code_block or should_skip(line):
            new_lines.append(line)
            continue
        fixed = fix_spacing_line(line)
        new_lines.append(fixed)

    # Phase 4: Clean blank lines
    new_lines = clean_blank_lines(new_lines)

    new_text = "\n".join(new_lines)
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

    print(f"\n=== Cleanup Pass 2 Results ===")
    print(f"  Files modified:        {stats['files_modified']}")
    print(f"  TOC blocks removed:    {stats['toc_blocks_removed']}")
    print(f"  Schedule blocks removed: {stats['schedule_blocks_removed']}")
    print(f"  Slide echoes removed:  {stats['slide_echoes_removed']}")
    print(f"  Spacing lines fixed:   {stats['spacing_lines_fixed']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
