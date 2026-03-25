# Project Architecture — surreal-docs crawler

**Date:** 2026-03-25

## Architecture

Restructured from ad-hoc scripts (crawl.py, crawl2.py, crawl3.py) into a proper uv package:

```
surreal_docs/
    __init__.py       # package
    extract.js        # DOM → Markdown (runs inside Playwright browser)
    core.py           # Pure fns (norm, to_file, md5, diff_manifests) + async I/O (discover, crawl)
    cli.py            # argparse CLI: discover | crawl | diff
snapshots/
    2026-03-25T22-12-02/    # timestamped crawl output
        manifest.json        # {pages: {path: {title,file,chars,hash}}, errors:[], meta:{}}
        docs/surrealql/...   # markdown files with frontmatter
    latest -> 2026-03-25T22-12-02   # symlink
```

## CLI Commands

- `uv run surreal-docs discover` — list all sidebar links from live site (138 pages as of 2026-03-25)
- `uv run surreal-docs crawl` — BFS crawl all pages → new timestamped snapshot
- `uv run surreal-docs diff [old] [new]` — compare two snapshots; `--json` for machine-readable

## Key Decisions

- **Hashing:** Each page content gets an MD5 hash stored in manifest.json for precise diff detection
- **Fallback:** When comparing old manifests without hashes (like docs3/), falls back to char count comparison
- **Symlink:** `snapshots/latest` always points to most recent crawl
- **extract.js:** Converts live DOM to markdown, skipping nav/sidebar/footer; handles code blocks, tables, lists
- **BFS traversal:** Discovers links from each page's content, not just sidebar — catches deep-linked pages

## Tools Available

- `playwright-cli` — for interactive ad-hoc exploration (open, goto, snapshot, eval)
- `uv run surreal-docs` — for automated crawl/diff pipeline

## Expansion Log

- 2026-03-25: Initial architecture. Old scripts (crawl.py, crawl2.py, crawl3.py, compare.py) preserved but superseded.
- 2026-03-25: First successful crawl: 138 pages, 0 errors. docs3/ ↔ new snapshot: 100% match.
