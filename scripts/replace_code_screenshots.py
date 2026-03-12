#!/usr/bin/env python3
"""Detect code screenshot images (dark background) and replace with code blocks or references.

Strategy:
1. For each image referenced in markdown, check if it's a code screenshot
   (dark average color = likely terminal/code capture)
2. If code screenshot AND we have matching code in code-ref, replace with code block + reference
3. If code screenshot but no matching code, add a note that this was a code screenshot
"""

import re
from pathlib import Path
from PIL import Image
import numpy as np

DOCS = Path(__file__).resolve().parent.parent / "docs" / "ros"
ASSETS = Path(__file__).resolve().parent.parent / "docs" / "assets" / "images" / "ros"
TARGET_DIRS = ["intro", "basics", "practice", "projects"]

stats = {
    "images_checked": 0,
    "code_screenshots_found": 0,
    "replaced_with_code": 0,
    "replaced_with_ref": 0,
    "files_modified": 0,
}

# Mapping: lesson file → code-ref file and relevant code sections
LESSON_CODE_MAP = {
    "intro/lesson-02": {
        "ref": "/ros/code-ref/pubsub-qos/",
        "label": "Pub/Sub & QoS 전체 소스코드",
    },
    "intro/lesson-03": {
        "ref": "/ros/code-ref/calculator/",
        "label": "Calculator 프로젝트 전체 소스코드",
    },
    "intro/lesson-04": {
        "ref": "/ros/code-ref/calculator/",
        "label": "Calculator 프로젝트 전체 소스코드",
    },
    "intro/lesson-05": {
        "ref": "/ros/code-ref/calculator/",
        "label": "Calculator 프로젝트 전체 소스코드",
    },
    "intro/lesson-06": {
        "ref": "/ros/code-ref/calculator/",
        "label": "Calculator 프로젝트 전체 소스코드",
    },
}


def is_code_screenshot(img_path: Path) -> bool:
    """Check if an image is a code screenshot based on average brightness."""
    try:
        with Image.open(img_path) as img:
            # Convert to RGB if needed
            if img.mode != "RGB":
                img = img.convert("RGB")
            arr = np.array(img)
            avg_brightness = arr.mean()
            # Code screenshots have dark backgrounds (avg brightness < 80)
            # Relaxed aspect ratio - code can be square or tall
            w, h = img.size
            aspect = w / h if h > 0 else 0
            return avg_brightness < 80 and aspect > 0.5
    except Exception:
        return False


def is_terminal_screenshot(img_path: Path) -> bool:
    """Check if image is a terminal screenshot (dark but with some light text)."""
    try:
        with Image.open(img_path) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            arr = np.array(img)
            avg = arr.mean()
            # Terminal: dark background but not as dark as code editors
            return 30 < avg < 100
    except Exception:
        return False


def get_code_ref_link(lesson_key: str) -> str:
    """Get a reference link for a lesson's code."""
    if lesson_key in LESSON_CODE_MAP:
        info = LESSON_CODE_MAP[lesson_key]
        return f'\n!!! tip "소스코드 참조"\n    이 코드의 전체 내용은 [{info["label"]}]({info["ref"]}) 페이지에서 확인할 수 있습니다.\n'
    return ""


def process_file(filepath: Path) -> bool:
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    result = []
    changed = False

    # Determine lesson key
    rel = filepath.relative_to(DOCS)
    lesson_key = str(rel.parent / rel.stem)  # e.g., "intro/lesson-03"

    # Track if we've already added a code-ref link for this file
    ref_added = False

    i = 0
    n = len(lines)
    in_code_block = False

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Check for image reference
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", stripped)
        if m:
            alt_text = m.group(1)
            img_rel_path = m.group(2)

            # Resolve image path
            img_abs = (filepath.parent / img_rel_path).resolve()
            stats["images_checked"] += 1

            if img_abs.exists() and is_code_screenshot(img_abs):
                stats["code_screenshots_found"] += 1

                # Replace code screenshot with reference
                if lesson_key in LESSON_CODE_MAP and not ref_added:
                    ref_link = get_code_ref_link(lesson_key)
                    result.append(ref_link)
                    ref_added = True
                    stats["replaced_with_ref"] += 1
                    changed = True
                else:
                    # Just remove the code screenshot image (code already referenced above)
                    stats["replaced_with_code"] += 1
                    changed = True

                i += 1
                continue

        result.append(line)
        i += 1

    if changed:
        # Clean excessive blank lines
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
    # Check dependencies
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("ERROR: Requires Pillow and numpy. Install with:")
        print("  pip install Pillow numpy")
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

    print(f"\n=== Code Screenshot Replacement Results ===")
    print(f"  Images checked:          {stats['images_checked']}")
    print(f"  Code screenshots found:  {stats['code_screenshots_found']}")
    print(f"  Replaced with ref link:  {stats['replaced_with_ref']}")
    print(f"  Screenshots removed:     {stats['replaced_with_code']}")
    print(f"  Files modified:          {stats['files_modified']}")
    print()
    for f in files_modified:
        print(f"  Modified: {f}")


if __name__ == "__main__":
    main()
