# surreal-docs

Playwright-based crawler for [SurrealDB SurrealQL documentation](https://surrealdb.com/docs/surrealql). Crawls all pages, saves timestamped snapshots, and diffs between crawls to detect documentation changes.

## Setup

```bash
uv sync
uv run playwright install chromium
```

## Commands

### discover

List all doc pages from the live site sidebar.

```bash
uv run surreal-docs discover
```

### crawl

BFS-crawl all pages and save a new timestamped snapshot under `snapshots/`.

```bash
uv run surreal-docs crawl
```

Output:

```
snapshots/
  2026-03-25T22-12-02/
    manifest.json         # page index with titles, char counts, MD5 hashes
    docs/surrealql/...    # markdown files with YAML frontmatter
  latest -> 2026-03-25T22-12-02
```

### diff

Compare two snapshots to detect added, removed, or changed pages.

```bash
# Latest vs previous snapshot
uv run surreal-docs diff

# Compare specific directories
uv run surreal-docs diff docs3 snapshots/latest

# Machine-readable JSON output
uv run surreal-docs diff --json
```

## How it works

1. **extract.js** runs inside the Playwright browser to convert live DOM into markdown — handles headings, code blocks, tables, lists, and links while skipping nav/sidebar/footer.
2. **BFS traversal** starts at `/docs/surrealql` and follows every in-scope link discovered on each page.
3. Each page's content is hashed (MD5) and stored in `manifest.json` for precise change detection.
4. **diff** compares two manifests by hash (falls back to char count for legacy manifests without hashes).

## Project structure

```
surreal_docs/
    __init__.py       # package
    extract.js        # DOM → Markdown (runs in browser)
    core.py           # pure functions + async crawl/discover
    cli.py            # CLI: discover | crawl | diff
snapshots/            # timestamped crawl outputs
```

## Interactive exploration

Use `playwright-cli` for ad-hoc inspection of specific pages:

```bash
playwright-cli open https://surrealdb.com/docs/surrealql
playwright-cli snapshot
playwright-cli eval "document.querySelector('h1').textContent"
playwright-cli close
```
