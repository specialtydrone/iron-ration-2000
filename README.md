# Iron Ration

Personal website and writing archive for Jonathan Lynch.

The site is built from Markdown source files using a small collection of Python scripts and Pandoc. Articles are stored as self-contained directories containing Markdown, generated HTML, and local media assets.

## Structure

```text
articles/
├── article-slug/
│   ├── index.md
│   ├── index.html
│   └── media/

templates/
├── site-header.html
└── site-footer.html

tools/
├── build_article.py
├── build_index.py
└── build_site.py
```

## Article Workflow

1. Create or import an article into:

   ```text
   articles/<slug>/index.md
   ```

2. Add any local images, video, or other assets to:

   ```text
   articles/<slug>/media/
   ```

3. Build the site:

   ```bash
   tools/build_site.py
   ```

## Front Matter

Each article begins with metadata:

```yaml
---
title: "Article Title"
written: 2024-01-18
published: 2024-02-09
type: essay
source: personal
---
```

## Design Philosophy

- Markdown is the canonical source.
- Generated HTML should never be edited by hand.
- Media is stored locally alongside the article.
- Templates control shared site elements.
- Git tracks the editorial history of the archive.

## Dependencies

- Python 3
- Pandoc

## Build

Rebuild all articles and the homepage:

```bash
tools/build_site.py
```