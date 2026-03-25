#!/usr/bin/env python3
"""
SurrealQL Docs — Ultra Full BFS Traversal Crawler v2
Dynamically discovers and crawls every link within /docs/surrealql.
Uses page.content() + Python html.parser — no fragile JS injection.
"""

import asyncio
import json
import re
import time
from collections import deque
from html.parser import HTMLParser
from pathlib import Path

from playwright.async_api import async_playwright

BASE_URL = "https://surrealdb.com"
START_PATH = "/docs/surrealql"
SCOPE_PREFIX = "/docs/surrealql"
OUTPUT_DIR = Path("/Users/noelbao/Tmp/surrealdb_3_crawl/docs2")

# ── HTML → Markdown converter ─────────────────────────────────────────────────

class MarkdownExtractor(HTMLParser):
    # void elements: never have a closing tag → must NOT touch skip_depth
    VOID_SKIP_TAGS = {"img", "input", "source", "track", "area", "embed", "wbr"}
    # non-void elements we want to skip entirely (open + close balances)
    BLOCK_SKIP_TAGS = {"script", "style", "noscript", "button", "svg"}
    SKIP_TAGS = VOID_SKIP_TAGS | BLOCK_SKIP_TAGS
    BLOCK_TAGS = {"div", "section", "article", "main", "aside", "nav", "header",
                  "footer", "li", "tr", "td", "th", "dd", "dt", "figure"}

    def __init__(self):
        super().__init__()
        self.buf: list[str] = []
        self.skip_depth = 0
        self.in_pre = False
        self.in_code_inline = False
        self.code_lang = ""
        self.tag_stack: list[str] = []
        self.list_counters: list[int] = []
        self.in_nav = False
        self.nav_depth = 0
        self._skip_nav_classes = {
            "sidebar", "nav", "navigation", "breadcrumb",
            "pagination", "toc", "table-of-contents",
        }

    def _attrs(self, attrs):
        return dict(attrs)

    def _is_nav(self, tag, attrs):
        d = self._attrs(attrs)
        role = d.get("role", "")
        cls = d.get("class", "")
        if tag in {"nav", "header", "footer"}: return True
        if role in {"navigation", "banner", "contentinfo"}: return True
        if any(s in cls for s in self._skip_nav_classes): return True
        return False

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)

        if self._is_nav(tag, attrs):
            self.in_nav = True
            self.nav_depth += 1
            return

        if self.in_nav:
            self.nav_depth += 1
            return

        if tag in self.VOID_SKIP_TAGS:
            return  # void — no closing tag, must NOT touch skip_depth

        if tag in self.BLOCK_SKIP_TAGS:
            self.skip_depth += 1
            return

        if self.skip_depth > 0:
            return

        d = self._attrs(attrs)

        if tag == "pre":
            self.in_pre = True
            self.buf.append("\n```")
            return

        if tag == "code":
            if self.in_pre:
                cls = d.get("class", "")
                m = re.search(r"language-([\w-]+)", cls)
                lang = m.group(1) if m else ""
                # patch the opening ``` with language
                for i in range(len(self.buf)-1, -1, -1):
                    if self.buf[i].startswith("\n```"):
                        self.buf[i] = f"\n```{lang}"
                        break
            else:
                self.in_code_inline = True
                self.buf.append("`")
            return

        if tag == "h1": self.buf.append("\n# ")
        elif tag == "h2": self.buf.append("\n## ")
        elif tag == "h3": self.buf.append("\n### ")
        elif tag == "h4": self.buf.append("\n#### ")
        elif tag == "h5": self.buf.append("\n##### ")
        elif tag == "h6": self.buf.append("\n###### ")
        elif tag == "p":  self.buf.append("\n")
        elif tag == "br": self.buf.append("\n")
        elif tag == "hr": self.buf.append("\n---\n")
        elif tag == "strong" or tag == "b": self.buf.append("**")
        elif tag == "em" or tag == "i":     self.buf.append("*")
        elif tag == "ul": self.list_counters.append(0)
        elif tag == "ol": self.list_counters.append(0)
        elif tag == "li":
            if self.list_counters:
                self.list_counters[-1] += 1
                cnt = self.list_counters[-1]
                # figure out if parent is ol or ul
                # walk tag_stack backwards to find ul/ol
                parent_ol = False
                for t in reversed(self.tag_stack[:-1]):
                    if t == "ol": parent_ol = True; break
                    if t == "ul": break
                if parent_ol:
                    self.buf.append(f"\n{cnt}. ")
                else:
                    self.buf.append("\n- ")
            else:
                self.buf.append("\n- ")
        elif tag == "blockquote": self.buf.append("\n> ")
        elif tag == "table": self.buf.append("\n")
        elif tag == "tr":   self.buf.append("\n| ")
        elif tag in {"th", "td"}:  pass  # content handled in data
        elif tag == "a":
            href = self._attrs(attrs).get("href", "")
            if href and not href.startswith("#"):
                self.buf.append("[")

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()

        if self.in_nav:
            self.nav_depth -= 1
            if self.nav_depth <= 0:
                self.in_nav = False
                self.nav_depth = 0
            return

        if tag in self.VOID_SKIP_TAGS:
            return  # void — no closing tag ever

        if tag in self.BLOCK_SKIP_TAGS:
            self.skip_depth = max(0, self.skip_depth - 1)
            return

        if self.skip_depth > 0:
            return

        if tag == "pre":
            self.in_pre = False
            self.buf.append("\n```\n")
            return

        if tag == "code":
            if not self.in_pre:
                self.in_code_inline = False
                self.buf.append("`")
            return

        if tag in {"h1","h2","h3","h4","h5","h6"}: self.buf.append("\n")
        elif tag == "p": self.buf.append("\n")
        elif tag in {"strong","b"}: self.buf.append("**")
        elif tag in {"em","i"}:     self.buf.append("*")
        elif tag in {"ul","ol"}:
            if self.list_counters:
                self.list_counters.pop()
            self.buf.append("\n")
        elif tag in {"tr"}:  self.buf.append(" |")
        elif tag in {"th","td"}: self.buf.append(" |")

    def handle_data(self, data):
        if self.in_nav or self.skip_depth > 0:
            return
        if self.in_pre or self.in_code_inline:
            self.buf.append(data)
            return
        # Collapse whitespace for normal text
        collapsed = re.sub(r"\s+", " ", data)
        self.buf.append(collapsed)

    def result(self) -> str:
        raw = "".join(self.buf)
        # Collapse excessive blank lines
        raw = re.sub(r"\n{4,}", "\n\n\n", raw)
        return raw.strip()


def html_to_markdown(html: str) -> tuple[str, str]:
    """Returns (title, markdown_content)."""
    # Extract title
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.DOTALL | re.IGNORECASE)
    title = ""
    if title_m:
        title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip()
    if not title:
        title_m2 = re.search(r"<title[^>]*>(.*?)</title>", html, re.DOTALL | re.IGNORECASE)
        if title_m2:
            title = re.sub(r"<[^>]+>", "", title_m2.group(1)).strip()

    # Find main content region
    # Try <article>, then <main>, then fall back to body
    for pattern in [
        r"<article[^>]*>(.*?)</article>",
        r"<main[^>]*>(.*?)</main>",
    ]:
        m = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if m:
            html = m.group(1)
            break

    parser = MarkdownExtractor()
    parser.feed(html)
    return title, parser.result()


def extract_links_from_html(html: str, scope: str) -> list[str]:
    """Extract all in-scope hrefs from raw HTML."""
    hrefs = re.findall(r'<a\s[^>]*href="([^"#][^"]*)"', html, re.IGNORECASE)
    result = set()
    for href in hrefs:
        href = href.split("#")[0].strip()
        if not href:
            continue
        if href.startswith(BASE_URL):
            path = href[len(BASE_URL):]
        elif href.startswith("http"):
            continue
        elif href.startswith("//"):
            continue
        else:
            path = href
        path = path.rstrip("/") or "/"
        if path.startswith(scope):
            result.add(path)
    return list(result)


def path_to_file(path: str) -> Path:
    parts = path.lstrip("/").split("/")
    if len(parts) <= 1:
        return OUTPUT_DIR / f"{parts[0] or 'index'}.md"
    return OUTPUT_DIR.joinpath(*parts[:-1]) / f"{parts[-1]}.md"


# ── Main crawler ──────────────────────────────────────────────────────────────

async def crawl():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    queue: deque[str] = deque([START_PATH])
    visited: set[str] = set()
    results: dict = {}
    errors: list = []

    print(f"Ultra BFS traversal: {BASE_URL}{START_PATH}")
    print(f"Scope prefix : {SCOPE_PREFIX}")
    print(f"Output       : {OUTPUT_DIR}")
    print("=" * 65)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
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

            print(f"  [{idx:3d}] {path}  (q={len(queue)} vis={len(visited)})")

            try:
                resp = await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(0.35)

                html = await page.content()

                # Discover new links
                new_links = [
                    l for l in extract_links_from_html(html, SCOPE_PREFIX)
                    if l not in visited
                ]
                added = 0
                for l in new_links:
                    if l not in queue:
                        queue.append(l)
                        added += 1
                if added:
                    print(f"         +{added} new links")

                # Convert to markdown
                title, content = html_to_markdown(html)

                if not content.strip():
                    print(f"         WARNING: empty content")
                    errors.append({"path": path, "reason": "empty content"})

                # Save
                out = path_to_file(path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(
                    f"---\ntitle: {title}\nurl: {url}\n"
                    f"crawled_at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n{content}\n",
                    encoding="utf-8",
                )
                size = len(content)
                rel = out.relative_to(OUTPUT_DIR.parent)
                print(f"         -> {rel}  ({size} chars)")

                results[path] = {
                    "title": title,
                    "file": str(rel),
                    "chars": size,
                }

            except Exception as exc:
                print(f"         ERROR: {exc}")
                errors.append({"path": path, "reason": str(exc)})

            await asyncio.sleep(0.15)

        await browser.close()

    # ── Write index ────────────────────────────────────────────────────────────
    lines = [
        "# SurrealQL Docs — BFS Traversal Index",
        "",
        f"Crawled: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Pages: {len(results)}  |  Errors: {len(errors)}",
        "",
    ]
    for path, info in sorted(results.items()):
        lines.append(f"- [{info['title']}]({info['file']}) — {info['chars']} chars")

    (OUTPUT_DIR / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    (OUTPUT_DIR / "manifest.json").write_text(
        json.dumps({"pages": results, "errors": errors}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n" + "=" * 65)
    print(f"DONE. Pages crawled: {len(results)}, Errors: {len(errors)}")
    if errors:
        for e in errors:
            print(f"  ERROR  {e['path']} — {e['reason'][:80]}")
    print(f"Index   : {OUTPUT_DIR}/INDEX.md")
    print(f"Manifest: {OUTPUT_DIR}/manifest.json")


if __name__ == "__main__":
    asyncio.run(crawl())
