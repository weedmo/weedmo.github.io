#!/usr/bin/env python3
"""Extract text and images from PDFs and generate markdown files."""

import fitz  # pymupdf
import os
import sys
import yaml
from pathlib import Path

STUDY_ROOT = Path("/home/weed/study")
SITE_ROOT = Path("/home/weed/study/study-site")
DOCS_ROOT = SITE_ROOT / "docs"
ASSETS_ROOT = SITE_ROOT / "assets" / "images"
ROS_STUDY = STUDY_ROOT / "ROS-study"

# PDF to section/page mapping
PDF_MAP = {
    # 입문 (Introduction)
    "ros/intro": {
        "lesson-01": "강의_3기_ROS2입문_1차시.pdf",
        "lesson-02": "강의_3기_ROS2입문_2차시.pdf",
        "lesson-03": "강의_3기_ROS2입문_3차시.pdf",
        "lesson-04": "강의_3기_ROS2입문_4차시.pdf",
        "lesson-05": "강의_3기_ROS2입문_5차시.pdf",
        "lesson-06": "강의_3기_ROS2입문_6차시.pdf",
        "lesson-07": "강의_3기_ROS2입문_7차시.pdf",
        "lesson-08": "강의_3기_ROS2입문_8차시.pdf",
        "lesson-09": "강의_3기_ROS2입문_9차시.pdf",
    },
    # 기초 (Fundamentals)
    "ros/basics": {
        "lesson-01": "강의_3기_ROS2_기초_1차시.pdf",
        "lesson-02": "강의_3기_ROS2_기초_2차시.pdf",
        "lesson-03": "강의_3기_ROS2_기초_3차시.pdf",
        "lesson-04": "강의_3기_ROS2_기초_4차시.pdf",
        "lesson-05": "강의_3기_ROS2_기초_5차시.pdf",
    },
    # 실습 (Practice)
    "ros/practice": {
        "practice-01-04": "강의_3기_ROS2_실습_1_4차시.pdf",
        "practice-04-05": "강의_3기_ROS2_실습_4_5차시.pdf",
        "practice-05-07": "강의_3기_ROS2_실습_5_7차시.pdf",
    },
    # 프로젝트 (Projects)
    "ros/projects": {
        "rviz2": "01_로키 - 두산 프로젝트 교안(RVIZ2)_김루진_0225.pdf",
        "gazebo": "02_로키 - 두산 프로젝트 교안(GAZEBO)_0305.pdf",
        "simulation": "로키 - 시뮬레이션 - 협업_김루진_0303.pdf",
        "aruco-conveyor": "로키 -  아로크마커, 컨베어벨트 프로젝트 교안_0412.pdf",
        "autonomous-driving": "로키 -  자율주행 디지털 트윈 프로젝트 교안.pdf",
        "thread-database": "쓰레드와 데이터베이스.pdf",
    },
}

# Quality thresholds
MIN_CHARS_PER_PAGE = 10  # Below this, use full-page PNG fallback
FALLBACK_DPI = 150


def extract_pdf(pdf_path: Path, section: str, page_name: str) -> str:
    """Extract text and images from a PDF, return markdown content."""
    doc = fitz.open(str(pdf_path))
    img_dir = ASSETS_ROOT / section / page_name
    img_dir.mkdir(parents=True, exist_ok=True)

    md_lines = []
    title = pdf_path.stem
    md_lines.append(f"# {title}\n")

    total_pages = len(doc)
    fallback_pages = 0
    img_counter = 0

    for page_num in range(total_pages):
        page = doc[page_num]
        text = page.get_text("text").strip()

        # Relative path from the markdown file to assets
        rel_img_base = f"../../assets/images/{section}/{page_name}"

        if len(text) < MIN_CHARS_PER_PAGE:
            # Fallback: render full page as image
            fallback_pages += 1
            pix = page.get_pixmap(dpi=FALLBACK_DPI)
            img_name = f"page_{page_num + 1:03d}.png"
            img_path = img_dir / img_name
            pix.save(str(img_path))
            md_lines.append(f"\n![Page {page_num + 1}]({rel_img_base}/{img_name})\n")
        else:
            # Extract text
            if text:
                md_lines.append(f"\n{text}\n")

            # Extract images from page
            images = page.get_images(full=True)
            for img_info in images:
                xref = img_info[0]
                try:
                    base_image = doc.extract_image(xref)
                    if base_image and base_image["image"]:
                        img_counter += 1
                        ext = base_image.get("ext", "png")
                        img_name = f"img_{page_num + 1:03d}_{img_counter:03d}.{ext}"
                        img_path = img_dir / img_name
                        with open(img_path, "wb") as f:
                            f.write(base_image["image"])
                        md_lines.append(f"\n![Image {img_counter}]({rel_img_base}/{img_name})\n")
                except Exception:
                    pass  # Skip problematic images

    doc.close()

    quality = 1.0 - (fallback_pages / total_pages) if total_pages > 0 else 1.0
    print(f"  [{page_name}] {total_pages} pages, {img_counter} images, "
          f"{fallback_pages} fallback pages, quality: {quality:.0%}")

    return "\n".join(md_lines)


def main():
    print("=== PDF Extraction Pipeline ===\n")

    total_pdfs = 0
    total_fallback = 0

    for section, pages in PDF_MAP.items():
        print(f"\nSection: {section}")
        docs_dir = DOCS_ROOT / section
        docs_dir.mkdir(parents=True, exist_ok=True)

        for page_name, pdf_filename in pages.items():
            pdf_path = ROS_STUDY / "docs" / pdf_filename
            if not pdf_path.exists():
                print(f"  [WARNING] PDF not found: {pdf_filename}")
                # Create placeholder
                md_path = docs_dir / f"{page_name}.md"
                md_path.write_text(f"# {pdf_filename}\n\n> PDF file not found.\n")
                continue

            total_pdfs += 1
            md_content = extract_pdf(pdf_path, section, page_name)
            md_path = docs_dir / f"{page_name}.md"
            md_path.write_text(md_content, encoding="utf-8")

    print(f"\n=== Done: {total_pdfs} PDFs processed ===")


if __name__ == "__main__":
    main()
