#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import re
import subprocess
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
HEADER_PATH = ROOT / "templates" / "site-header.html"

def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)

def parse_front_matter(md_path):
    text = md_path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)

    if not match:
        die(f"Missing front matter in {md_path}")

    raw_meta = match.group(1)
    meta = {}

    for line in raw_meta.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')

    return meta

def display_date(iso_date):
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

def build(article_dir):
    article_dir = Path(article_dir)
    md_path = article_dir / "index.md"
    html_path = article_dir / "index.html"

    if not md_path.exists():
        die(f"No index.md found in {article_dir}")

    if not HEADER_PATH.exists():
        die("Missing templates/site-header.html")

    meta = parse_front_matter(md_path)

    title = meta.get("title")
    written = meta.get("written")

    if not title:
        die("Missing title in front matter")

    if not written:
        die("Missing written date in front matter")

    subprocess.run(
        [
            "pandoc",
            str(md_path),
            "--standalone",
            "--metadata",
            f"title={title}",
            "--css",
            "../../styles.css",
            "-o",
            str(html_path),
        ],
        check=True,
    )

    html = html_path.read_text(encoding="utf-8")

    site_header = HEADER_PATH.read_text(encoding="utf-8")
    from datetime import datetime


    footer = (
        ROOT / "templates" / "site-footer.html"
    ).read_text(encoding="utf-8")

    footer = footer.replace(
        "{{YEAR}}",
        str(datetime.now().year)
    )

    html = html.replace(
        "</head>",
        '  <link rel="icon" href="../../images/favicon.svg" type="image/svg+xml" />\n</head>',
        1,
    )


    html = html.replace("<body>", "<body>\n" + site_header, 1)

    # H1 to title heading
    html = re.sub(
        r'<h1 class="title">.*?</h1>',
        f'<p class="article-date">{display_date(written)}</p>\n'
        f'<h1 class="title">{title}</h1>\n'
        f'<hr>',
        html,
        count=1,
        flags=re.S,
    )

    # Remove duplicate title if the source document also began with a bold title.
    html = html.replace(f"<p><strong>{title}</strong></p>", "", 1)

    # Headings to div headers
    html = re.sub(
        r"<h[23][^>]*>(.*?)</h[23]>",
        r'<div class="article-header">\1</div>',
        html,
        flags=re.S
    )

    # Footnotes
    html = re.sub(
        r'(<section[^>]*class="[^"]*footnotes[^"]*"[^>]*>\s*)<hr\s*/?>',
        r'\1<div class="article-header">Footnotes</div>',
        html,
        count=1,
        flags=re.S,
    )

    # Footer
    html = html.replace(
        "</body>",
        footer + "\n</body>",
        1
    )


    html_path.write_text(html, encoding="utf-8")
    print(f"Built {html_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        die("Usage: tools/build_article.py articles/article-folder")

    build(sys.argv[1])
