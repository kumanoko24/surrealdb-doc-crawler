"""Core logic — pure functions + async I/O for crawling SurrealQL docs."""

import asyncio
import hashlib
import json
import time
from collections import deque
from pathlib import Path

from playwright.async_api import async_playwright

BASE_URL   = "https://surrealdb.com"
START_PATH = "/docs/surrealql"
JS_PATH    = Path(__file__).parent / "extract.js"


# ── Pure functions ────────────────────────────────────────────────────────────

def norm(path: str) -> str:
    """Normalize URL path: strip trailing slashes."""
    return path.rstrip("/") or path


def to_file(path: str, root: Path) -> Path:
    """Map URL path → filesystem .md path under root."""
    parts = path.lstrip("/").split("/")
    if len(parts) <= 1:
        return root / f"{parts[0] or 'index'}.md"
    return root.joinpath(*parts[:-1]) / f"{parts[-1]}.md"


def md5(text: str) -> str:
    """Content hash for change detection."""
    return hashlib.md5(text.encode()).hexdigest()


def load_manifest(snapshot_dir: Path) -> dict:
    """Load manifest.json from a snapshot directory."""
    p = snapshot_dir / "manifest.json"
    if not p.exists():
        return {"pages": {}, "meta": {}, "errors": []}
    return json.loads(p.read_text())


def diff_manifests(old: dict, new: dict) -> dict:
    """Compare two manifests. Returns structured diff with added/removed/changed."""
    op = {norm(k): v for k, v in old.get("pages", {}).items()}
    np = {norm(k): v for k, v in new.get("pages", {}).items()}
    old_keys, new_keys = set(op), set(np)

    changed, unchanged = [], 0
    for p in sorted(old_keys & new_keys):
        oh, nh = op[p].get("hash"), np[p].get("hash")
        # If both have hashes, compare hashes; otherwise fall back to char count
        same = (oh == nh) if (oh and nh) else (op[p].get("chars") == np[p].get("chars"))
        if not same:
            changed.append({
                "path": p,
                "old_title": op[p].get("title", ""),
                "new_title": np[p].get("title", ""),
                "old_chars": op[p].get("chars", 0),
                "new_chars": np[p].get("chars", 0),
            })
        else:
            unchanged += 1

    return {
        "added":     [{"path": p, **np[p]} for p in sorted(new_keys - old_keys)],
        "removed":   [{"path": p, **op[p]} for p in sorted(old_keys - new_keys)],
        "changed":   changed,
        "unchanged": unchanged,
        "old_meta":  old.get("meta", {}),
        "new_meta":  new.get("meta", {}),
    }


# ── I/O: Discover ────────────────────────────────────────────────────────────

async def discover() -> list[dict]:
    """Open SurrealQL docs and extract every sidebar navigation link."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"{BASE_URL}{START_PATH}", wait_until="networkidle", timeout=30_000)
        await asyncio.sleep(1)

        links = await page.evaluate("""() => {
            const seen = new Set();
            return Array.from(document.querySelectorAll('nav a[href]'))
                .map(a => {
                    const href = a.getAttribute('href').replace(/\\/+$/, '');
                    return { text: a.textContent.trim(), href };
                })
                .filter(x => x.href.startsWith('/docs/surrealql')
                           && !seen.has(x.href)
                           && seen.add(x.href));
        }""")

        await browser.close()
    return links


# ── I/O: Crawl ───────────────────────────────────────────────────────────────

async def crawl(output_dir: Path) -> dict:
    """BFS-crawl all SurrealQL docs. Saves markdown + manifest to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    js = JS_PATH.read_text(encoding="utf-8")

    queue:   deque[str] = deque([START_PATH])
    visited: set[str]   = set()
    pages:   dict       = {}
    errors:  list       = []

    print(f"Crawling {BASE_URL}{START_PATH} → {output_dir}")
    print("=" * 65)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        page = await ctx.new_page()

        idx = 0
        while queue:
            path = norm(queue.popleft())
            if path in visited:
                continue
            visited.add(path)
            idx += 1

            url = BASE_URL + path
            print(f"  [{idx:3d}] {path}  (q={len(queue)})")

            try:
                await page.goto(url, wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(0.5)

                data = await page.evaluate(js)
                title = data.get("title", path)
                body  = data.get("content", "")

                # Enqueue discovered in-scope links
                for lnk in data.get("links", []):
                    queue.append(norm(lnk))

                if not body.strip():
                    errors.append({"path": path, "reason": "empty content"})

                # Save markdown with frontmatter
                out = to_file(path, output_dir)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(
                    f"---\ntitle: {title}\nurl: {url}\n"
                    f"crawled_at: {time.strftime('%Y-%m-%dT%H:%M:%S')}\n---\n\n{body}\n",
                    encoding="utf-8",
                )

                pages[path] = {
                    "title": title,
                    "file":  str(out.relative_to(output_dir)),
                    "chars": len(body),
                    "hash":  md5(body),
                }
                print(f"         → {out.relative_to(output_dir)}  ({len(body):,} chars)")

            except Exception as exc:
                msg = str(exc)[:120]
                print(f"         ERROR: {msg}")
                errors.append({"path": path, "reason": msg})

            await asyncio.sleep(0.15)

        await browser.close()

    # ── write manifest ────────────────────────────────────────────────────────
    meta = {
        "crawled_at":  time.strftime("%Y-%m-%dT%H:%M:%S"),
        "base_url":    BASE_URL,
        "scope":       START_PATH,
        "page_count":  len(pages),
        "error_count": len(errors),
    }
    manifest = {"pages": pages, "errors": errors, "meta": meta}
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8",
    )

    print(f"\n{'='*65}")
    print(f"Done: {len(pages)} pages, {len(errors)} errors → {output_dir}")
    if errors:
        for e in errors:
            print(f"  ! {e['path']}  — {e['reason'][:80]}")

    return manifest
