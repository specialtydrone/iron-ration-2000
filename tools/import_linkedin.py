#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import html
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
INCOMING = Path("/Volumes/Media/Jon/iron-ration/incoming/linkedin")
ARTICLES = ROOT / "articles"

def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)

def slugify(text):
    text = text.lower()
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def extract(pattern, text, label):
    match = re.search(pattern, text, re.S)
    if not match:
        die(f"Could not find {label}")
    return html.unescape(match.group(1).strip())

def clean_markdown(md):
    marker = "::: {}\n"
    if marker in md:
        md = md.split(marker, 1)[1]

    md = md.replace("\\'", "'")
    md = md.replace('\\"', '"')
    md = md.replace('{target="_blank"}', '')
    md = md.replace(":::","")
    return md.strip() + "\n"

def import_file(source):
    raw = source.read_text(encoding="utf-8", errors="ignore")

    title = extract(r"<title>(.*?)</title>", raw, "title")
    created = extract(r'Created on ([0-9]{4}-[0-9]{2}-[0-9]{2})', raw, "created date")
    published = extract(r'Published on ([0-9]{4}-[0-9]{2}-[0-9]{2})', raw, "published date")

    slug = slugify(title)
    article_dir = ARTICLES / slug
    article_dir.mkdir(parents=True, exist_ok=True)

    tmp = article_dir / "_linkedin_raw.md"

    subprocess.run(
        [
            "pandoc",
            str(source),
            "-f",
            "html",
            "-t",
            "markdown",
            "-o",
            str(tmp),
        ],
        check=True,
    )

    md = clean_markdown(tmp.read_text(encoding="utf-8"))
    tmp.unlink()

    front = f'''---
title: "{title}"
written: {created}
published: {published}
type: linkedin
source: linkedin
---

'''

    out = article_dir / "index.md"
    out.write_text(front + md, encoding="utf-8")

    print(f"Imported {source.name} -> articles/{slug}/index.md")

def main():
    if not INCOMING.exists():
        die(f"Missing incoming folder: {INCOMING}")

    files = sorted(INCOMING.glob("*.html"))

    if not files:
        die("No LinkedIn HTML files found")

    for source in files:
        import_file(source)

if __name__ == "__main__":
    main()
