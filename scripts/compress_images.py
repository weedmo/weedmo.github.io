#!/usr/bin/env python3
"""Compress all images to WebP format with max 1200px width."""

from pathlib import Path
from PIL import Image
import os

ASSETS_ROOT = Path("/home/weed/study/study-site/assets/images")
MAX_WIDTH = 1200
WEBP_QUALITY = 85


def compress_image(img_path: Path) -> bool:
    """Compress a single image to WebP. Returns True if converted."""
    try:
        with Image.open(img_path) as img:
            # Convert RGBA to RGB for WebP compatibility
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize if wider than MAX_WIDTH
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_height = int(img.height * ratio)
                img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

            # Save as WebP
            webp_path = img_path.with_suffix(".webp")
            img.save(str(webp_path), "WebP", quality=WEBP_QUALITY)

            # Remove original if different format
            if img_path.suffix.lower() != ".webp":
                img_path.unlink()

            return True
    except Exception as e:
        print(f"  [ERROR] {img_path.name}: {e}")
        return False


def update_markdown_refs(docs_root: Path):
    """Update image references in all markdown files from png/jpg to webp."""
    for md_file in docs_root.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        original = content
        for ext in [".png", ".jpg", ".jpeg", ".bmp", ".gif"]:
            content = content.replace(f"]{ext})", "].webp)")
            # Handle cases like ![img](path/file.png)
            content = content.replace(ext + ")", ".webp)")
        if content != original:
            md_file.write_text(content, encoding="utf-8")


def main():
    print("=== Image Compression Pipeline ===\n")

    extensions = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
    images = [f for f in ASSETS_ROOT.rglob("*") if f.suffix.lower() in extensions]

    print(f"Found {len(images)} images to compress\n")

    total_original = 0
    total_compressed = 0
    converted = 0

    for img_path in images:
        original_size = img_path.stat().st_size
        total_original += original_size

        if compress_image(img_path):
            webp_path = img_path.with_suffix(".webp")
            if webp_path.exists():
                compressed_size = webp_path.stat().st_size
                total_compressed += compressed_size
                converted += 1

    # Update markdown references
    docs_root = Path("/home/weed/study/study-site/docs")
    update_markdown_refs(docs_root)

    # Report
    if total_original > 0:
        ratio = (1 - total_compressed / total_original) * 100
        print(f"\n=== Results ===")
        print(f"Images converted: {converted}/{len(images)}")
        print(f"Original size: {total_original / 1024 / 1024:.1f} MB")
        print(f"Compressed size: {total_compressed / 1024 / 1024:.1f} MB")
        print(f"Reduction: {ratio:.1f}%")
    else:
        print("No images found to compress.")

    # Total site size
    site_root = Path("/home/weed/study/study-site")
    total_site = sum(f.stat().st_size for f in site_root.rglob("*") if f.is_file())
    print(f"Total site size: {total_site / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
