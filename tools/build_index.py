#!/usr/bin/env python3

from pathlib import Path
from datetime import datetime
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ARTICLES = ROOT / "articles"
HEADER_PATH = ROOT / "templates" / "site-header.html"
FOOTER_PATH = ROOT / "templates" / "site-footer.html"

START = "<!-- WRITING-LIST:START -->"
END = "<!-- WRITING-LIST:END -->"

def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)

def read_template(path):
    if not path.exists():
        die(f"Missing template: {path}")

    template = path.read_text(encoding="utf-8")
    return template.replace("{{YEAR}}", str(datetime.now().year))

def parse_front_matter(md_path):
    text = md_path.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)

    if not match:
        return None

    meta = {}

    for line in match.group(1).splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')

    return meta

def display_date(iso_date):
    dt = datetime.strptime(iso_date, "%Y-%m-%d")
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

def collect_articles():
    posts = []

    for md in sorted(ARTICLES.glob("*/index.md")):
        meta = parse_front_matter(md)

        if not meta:
            continue

        title = meta.get("title")
        written = meta.get("written")

        if not title or not written:
            continue

        posts.append({
            "title": title,
            "written": written,
            "slug": md.parent.name,
        })

    return sorted(posts, key=lambda p: p["written"], reverse=True)

def build_writing_list(posts):
    lines = [START, '            <ul class="writing-list">']

    for post in posts:
        lines.append(
            f'                <li class="writing-entry">'
            f'<span class="writing-date">{display_date(post["written"])}</span>'
            f'<a href="articles/{post["slug"]}/index.html">{post["title"]}</a></li>'
        )

    lines.extend(["            </ul>", f"            {END}"])
    return "\n".join(lines)

def replace_site_header(html):
    header = read_template(HEADER_PATH)

    pattern = re.compile(
        r'\s*<header class="site-header">.*?</header>',
        re.S
    )

    if pattern.search(html):
        return pattern.sub("\n" + header, html, count=1)

    return html.replace("<body>", "<body>\n" + header, 1)

def replace_site_footer(html):
    footer = read_template(FOOTER_PATH)

    pattern = re.compile(
        r'\s*<footer class="site-footer">.*?</footer>',
        re.S
    )

    if pattern.search(html):
        return pattern.sub("\n" + footer, html, count=1)

    return html.replace("</body>", footer + "\n</body>", 1)

def main():
    if not INDEX.exists():
        die("Missing index.html")

    html = INDEX.read_text(encoding="utf-8")
    posts = collect_articles()
    writing_list = build_writing_list(posts)

    html = replace_site_header(html)
    html = replace_site_footer(html)

    if START in html and END in html:
        pattern = re.compile(f"{re.escape(START)}.*?{re.escape(END)}", re.S)
        html = pattern.sub(writing_list, html)
    else:
        die("Could not find Writing list markers in index.html")

    INDEX.write_text(html, encoding="utf-8")
    print(f"Updated {INDEX} with {len(posts)} article(s)")

if __name__ == "__main__":
    main()