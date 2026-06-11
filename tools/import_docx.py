#!/usr/bin/env python3

from pathlib import Path
import argparse
import re
import shutil
import subprocess
import sys
import zipfile

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)

def extract_images(docx_path, media_dir):
    media_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(docx_path) as z:
        images = [
            name for name in z.namelist()
            if name.startswith("word/media/")
        ]

        for image in images:
            filename = Path(image).name
            target = media_dir / filename

            with z.open(image) as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)

    return len(images)

def convert_docx_to_markdown(docx_path, markdown_path):
    subprocess.run(
        [
            "pandoc",
            str(docx_path),
            "-t",
            "markdown",
            "--extract-media",
            str(markdown_path.parent),
            "-o",
            str(markdown_path),
        ],
        check=True,
    )

def normalize_media_folder(article_dir):
    extracted = article_dir / "media"
    pandoc_media = article_dir / "media"

    # Pandoc with --extract-media article_dir usually creates media/image1.png.
    # This function exists as a placeholder for future cleanup/renaming.
    pandoc_media.mkdir(exist_ok=True)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a Google Docs DOCX export into an article folder."
    )

    parser.add_argument("docx", help="Path to the .docx file")
    parser.add_argument(
        "--title",
        help="Article title. Defaults to the DOCX filename."
    )
    parser.add_argument(
        "--written",
        required=True,
        help="Written date in YYYY-MM-DD format"
    )
    parser.add_argument(
        "--published",
        help="Published date in YYYY-MM-DD format. Defaults to written date."
    )
    parser.add_argument(
        "--type",
        default="essay",
        help="Article type, e.g. essay, short-story, college-paper"
    )
    parser.add_argument(
        "--source",
        default="google-docs",
        help="Source label"
    )
    parser.add_argument(
        "--out",
        default="articles",
        help="Output articles directory"
    )

    args = parser.parse_args()

    docx_path = Path(args.docx)
    if not docx_path.exists():
        die(f"File not found: {docx_path}")

    title = args.title or docx_path.stem
    written = args.written
    published = args.published or written

    article_dir = Path(args.out) / slugify(title)
    media_dir = article_dir / "media"
    markdown_path = article_dir / "index.md"

    article_dir.mkdir(parents=True, exist_ok=True)

    convert_docx_to_markdown(docx_path, markdown_path)
    normalize_media_folder(article_dir)

    raw_body = markdown_path.read_text(encoding="utf-8")

    front_matter = f'''---
title: "{title}"
written: {written}
published: {published}
type: {args.type}
source: {args.source}
---

'''

    markdown_path.write_text(front_matter + raw_body, encoding="utf-8")

    print(f"Created: {article_dir}")
    print(f"Markdown: {markdown_path}")
    print(f"Media: {media_dir}")

if __name__ == "__main__":
    main()