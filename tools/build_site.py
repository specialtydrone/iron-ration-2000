#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
BUILD_ARTICLE = ROOT / "tools" / "build_article.py"
BUILD_INDEX = ROOT / "tools" / "build_index.py"

def die(message):
    print(f"ERROR: {message}", file=sys.stderr)
    sys.exit(1)

def run(command):
    print("+ " + " ".join(str(part) for part in command))
    subprocess.run(command, check=True)

def main():
    start = time.perf_counter()

    if not ARTICLES.exists():
        die("Missing articles directory")

    article_dirs = sorted(
        p for p in ARTICLES.iterdir()
        if p.is_dir() and (p / "index.md").exists()
    )

    for article_dir in article_dirs:
        run([sys.executable, str(BUILD_ARTICLE), str(article_dir)])

    run([sys.executable, str(BUILD_INDEX)])

    elapsed = time.perf_counter() - start

    print()
    print(f"Built {len(article_dirs)} article(s) and updated index.html")
    print(f"Total build time: {elapsed:.2f} seconds")

if __name__ == "__main__":
    main()
