#!/usr/bin/env python3
"""
SurrealQL Docs — Ultra BFS Playwright Crawler v3
- Full JS rendering (no raw HTML regex)
- Extracts content via extract.js running inside the live browser DOM
- BFS traversal: every link discovered on every page is followed
"""

import asyncio
import json
import time
from collections import deque
from pathlib import Path

from playwright.async_api import async_playwright

BASE_URL     = "https://surrealdb.com"
START_PATH   = "/docs/surrealql"
SCOPE        = "/docs/surrealql"
OUTPUT_DIR   = Path("/Users/noelbao/Tmp/surrealdb_3_crawl/docs3")
EXTRACT_JS   = Path(__file__).parent / "extract.js"


def path_to_file(path: str) -> Path:
    parts = path.lstrip("/").split("/")
    if len(parts) <= 1:
        return OUTPUT_DIR / f"{parts[0] or 'index'}.md"
    return OUTPUT_DIR.joinpath(*parts[:-1]) / f"{parts[-1]}.md"


async def crawl():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    js_fn = EXTRACT_JS.read_text(encoding="utf-8")

    queue:   deque[str] = deque([START_PATH])
    visited: set[str]   = set()
    results: dict       = {}
    errors:  list       = []

    print(f"BFS traverse: {BASE_URL}{START_PATH}")
    print(f"Output      : {OUTPUT_DIR}")
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
            path = queue.popleft()
            if path in visited:
                continue
            visited.add(path)
            idx += 1

            url = BASE_URL + path
            print(f"  [{idx:3d}] {path}  (q={len(queue)}, vis={len(visited)})")

            try:
                await page.goto(url, wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(0.5)   # let React / hydration settle

                data = await page.evaluate(js_fn)

                title   = data.get("title", path)
                content = data.get("content", "")
                links   = data.get("links", [])

                # Enqueue new in-scope links
                added = 0
                for lnk in links:
                    if lnk not in visited and lnk not in queue:
                        queue.append(lnk)
                        added += 1
                if added:
                    print(f"         +{added} new links")

                if not content.strip():
                    print(f"         WARNING: empty content")
                    errors.append({"path": path, "reason": "empty content"})

                # Save markdown
                out = path_to_file(path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(
                    f"---\ntitle: {title}\nurl: {url}\n"
                    f"crawled_at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n{content}\n",
                    encoding="utf-8",
                )
                print(f"         -> {out.relative_to(OUTPUT_DIR.parent)}  ({len(content):,} chars)")
                results[path] = {
                    "title": title,
                    "file":  str(out.relative_to(OUTPUT_DIR.parent)),
                    "chars": len(content),
                }

            except Exception as exc:
                msg = str(exc)[:120]
                print(f"         ERROR: {msg}")
                errors.append({"path": path, "reason": msg})

            await asyncio.sleep(0.15)

        await browser.close()

    # ── index ──────────────────────────────────────────────────────────────────
    lines = [
        "# SurrealQL Docs — BFS Playwright Traversal",
        "",
        f"Crawled : {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Pages   : {len(results)}",
        f"Errors  : {len(errors)}",
        "",
    ]
    for path, info in sorted(results.items()):
        lines.append(f"- [{info['title']}]({info['file']}) — {info['chars']:,} chars")

    (OUTPUT_DIR / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps({"pages": results, "errors": errors}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print(f"DONE — pages: {len(results)}, errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ! {e['path']}  —  {e['reason'][:80]}")
    print(f"Index   : {OUTPUT_DIR}/INDEX.md")
    print(f"Manifest: {OUTPUT_DIR}/manifest.json")


if __name__ == "__main__":
    asyncio.run(crawl())
