#!/usr/bin/env python3
"""
SurrealQL Docs Ultra Crawler
Crawls https://surrealdb.com/docs/surrealql entirely and saves all pages as markdown files.
"""

import asyncio
import re
import os
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = "https://surrealdb.com"
OUTPUT_DIR = Path("/Users/noelbao/Tmp/surrealdb_3_crawl/docs")

# All known SurrealQL pages from navigation
SEED_URLS = [
    "/docs/surrealql",
    "/docs/surrealql/demo",
    "/docs/surrealql/operators",
    # Data types
    "/docs/surrealql/datamodel",
    "/docs/surrealql/datamodel/arrays",
    "/docs/surrealql/datamodel/booleans",
    "/docs/surrealql/datamodel/bytes",
    "/docs/surrealql/datamodel/closures",
    "/docs/surrealql/datamodel/datetimes",
    "/docs/surrealql/datamodel/durations",
    "/docs/surrealql/datamodel/files",
    "/docs/surrealql/datamodel/futures",
    "/docs/surrealql/datamodel/geometries",
    "/docs/surrealql/datamodel/none-and-null",
    "/docs/surrealql/datamodel/numbers",
    "/docs/surrealql/datamodel/objects",
    "/docs/surrealql/datamodel/ranges",
    "/docs/surrealql/datamodel/ids",
    "/docs/surrealql/datamodel/regex",
    "/docs/surrealql/datamodel/sets",
    "/docs/surrealql/datamodel/strings",
    "/docs/surrealql/datamodel/uuid",
    "/docs/surrealql/datamodel/values",
    "/docs/surrealql/datamodel/casting",
    "/docs/surrealql/datamodel/formatters",
    "/docs/surrealql/datamodel/literals",
    "/docs/surrealql/datamodel/idioms",
    "/docs/surrealql/datamodel/records",
    "/docs/surrealql/datamodel/references",
    # Statements
    "/docs/surrealql/statements",
    "/docs/surrealql/statements/access",
    "/docs/surrealql/statements/alter",
    "/docs/surrealql/statements/begin",
    "/docs/surrealql/statements/break",
    "/docs/surrealql/statements/cancel",
    "/docs/surrealql/statements/commit",
    "/docs/surrealql/statements/continue",
    "/docs/surrealql/statements/create",
    "/docs/surrealql/statements/define",
    "/docs/surrealql/statements/delete",
    "/docs/surrealql/statements/explain",
    "/docs/surrealql/statements/for",
    "/docs/surrealql/statements/ifelse",
    "/docs/surrealql/statements/info",
    "/docs/surrealql/statements/insert",
    "/docs/surrealql/statements/kill",
    "/docs/surrealql/statements/let",
    "/docs/surrealql/statements/live",
    "/docs/surrealql/statements/rebuild",
    "/docs/surrealql/statements/relate",
    "/docs/surrealql/statements/remove",
    "/docs/surrealql/statements/return",
    "/docs/surrealql/statements/select",
    "/docs/surrealql/statements/show",
    "/docs/surrealql/statements/sleep",
    "/docs/surrealql/statements/throw",
    "/docs/surrealql/statements/update",
    "/docs/surrealql/statements/upsert",
    "/docs/surrealql/statements/use",
    # Parameters
    "/docs/surrealql/parameters",
    # Clauses
    "/docs/surrealql/clauses",
    "/docs/surrealql/clauses/explain",
    "/docs/surrealql/clauses/fetch",
    "/docs/surrealql/clauses/from",
    "/docs/surrealql/clauses/group-by",
    "/docs/surrealql/clauses/limit",
    "/docs/surrealql/clauses/omit",
    "/docs/surrealql/clauses/order-by",
    "/docs/surrealql/clauses/split",
    "/docs/surrealql/clauses/where",
    "/docs/surrealql/clauses/with",
    # Transactions
    "/docs/surrealql/transactions",
    # Functions
    "/docs/surrealql/functions",
    "/docs/surrealql/functions/database",
    "/docs/surrealql/functions/script",
    "/docs/surrealql/functions/ml",
    # Comments
    "/docs/surrealql/comments",
]


def url_to_path(url_path: str) -> Path:
    """Convert URL path to file path."""
    # Remove leading slash and replace / with _
    clean = url_path.lstrip("/")
    # Replace remaining slashes with directory separators
    parts = clean.split("/")
    if len(parts) == 1:
        return OUTPUT_DIR / f"{parts[0]}.md"
    return OUTPUT_DIR / Path(*parts[:-1]) / f"{parts[-1]}.md"


async def extract_page_content(page) -> dict:
    """Extract structured content from a page."""
    result = await page.evaluate("""() => {
        // Get title
        const title = document.title || '';
        const h1 = document.querySelector('h1');
        const pageTitle = h1 ? h1.textContent.trim() : title;

        // Find main content area - try multiple selectors
        const mainSelectors = [
            'article',
            'main article',
            '.doc-content',
            '[class*="content"]',
            'main',
        ];

        let mainEl = null;
        for (const sel of mainSelectors) {
            mainEl = document.querySelector(sel);
            if (mainEl) break;
        }

        if (!mainEl) mainEl = document.body;

        // Extract text content with structure
        function processNode(node, indent) {
            if (!node) return '';

            let result = '';

            if (node.nodeType === 3) { // Text node
                const text = node.textContent;
                if (text.trim()) return text;
                return '';
            }

            if (node.nodeType !== 1) return '';

            const tag = node.tagName.toLowerCase();

            // Skip navigation, headers, footers, etc.
            if (['nav', 'header', 'footer', 'script', 'style', 'noscript'].includes(tag)) return '';
            if (node.getAttribute('role') === 'navigation') return '';
            if (node.classList.contains('sidebar') || node.classList.contains('nav')) return '';

            // Handle specific elements
            if (tag === 'h1') return '\\n# ' + node.textContent.trim() + '\\n\\n';
            if (tag === 'h2') return '\\n## ' + node.textContent.trim() + '\\n\\n';
            if (tag === 'h3') return '\\n### ' + node.textContent.trim() + '\\n\\n';
            if (tag === 'h4') return '\\n#### ' + node.textContent.trim() + '\\n\\n';
            if (tag === 'h5') return '\\n##### ' + node.textContent.trim() + '\\n\\n';
            if (tag === 'h6') return '\\n###### ' + node.textContent.trim() + '\\n\\n';

            if (tag === 'p') {
                const children = Array.from(node.childNodes).map(c => processNode(c, indent)).join('');
                return '\\n' + children.trim() + '\\n';
            }

            if (tag === 'pre' || tag === 'code') {
                if (tag === 'pre') {
                    const codeEl = node.querySelector('code');
                    const lang = codeEl ? (codeEl.className.match(/language-([\\w-]+)/) || [])[1] || '' : '';
                    const code = node.textContent;
                    return '\\n```' + lang + '\\n' + code + '\\n```\\n';
                }
                // Inline code
                return '`' + node.textContent + '`';
            }

            if (tag === 'ul') {
                const items = Array.from(node.querySelectorAll(':scope > li')).map(li => {
                    return '- ' + li.textContent.trim().replace(/\\n+/g, ' ');
                });
                return '\\n' + items.join('\\n') + '\\n';
            }

            if (tag === 'ol') {
                const items = Array.from(node.querySelectorAll(':scope > li')).map((li, i) => {
                    return (i+1) + '. ' + li.textContent.trim().replace(/\\n+/g, ' ');
                });
                return '\\n' + items.join('\\n') + '\\n';
            }

            if (tag === 'table') {
                const rows = Array.from(node.querySelectorAll('tr'));
                if (rows.length === 0) return '';

                const headerRow = rows[0];
                const headers = Array.from(headerRow.querySelectorAll('th, td')).map(cell => cell.textContent.trim());
                let tableStr = '\\n| ' + headers.join(' | ') + ' |\\n';
                tableStr += '| ' + headers.map(() => '---').join(' | ') + ' |\\n';

                for (let i = 1; i < rows.length; i++) {
                    const cells = Array.from(rows[i].querySelectorAll('td')).map(cell => cell.textContent.trim().replace(/\\n+/g, ' '));
                    if (cells.length > 0) {
                        tableStr += '| ' + cells.join(' | ') + ' |\\n';
                    }
                }
                return tableStr + '\\n';
            }

            if (tag === 'blockquote') {
                const text = node.textContent.trim().split('\\n').map(l => '> ' + l).join('\\n');
                return '\\n' + text + '\\n';
            }

            if (tag === 'a') {
                const href = node.getAttribute('href') || '';
                const text = node.textContent.trim();
                if (!text) return '';
                if (href.startsWith('#') || href.startsWith('http')) return text;
                return text;
            }

            if (tag === 'strong' || tag === 'b') return '**' + node.textContent.trim() + '**';
            if (tag === 'em' || tag === 'i') return '*' + node.textContent.trim() + '*';
            if (tag === 'hr') return '\\n---\\n';
            if (tag === 'br') return '\\n';

            // For divs and sections, recurse into children
            let children = '';
            for (const child of node.childNodes) {
                children += processNode(child, indent);
            }
            return children;
        }

        const content = processNode(mainEl, '');

        // Clean up excessive whitespace
        const cleaned = content
            .replace(/\\n{4,}/g, '\\n\\n\\n')
            .trim();

        // Also get all sidebar links for discovery
        const sidebarLinks = Array.from(document.querySelectorAll('nav a, aside a'))
            .map(a => a.getAttribute('href'))
            .filter(href => href && href.includes('/docs/surrealql'))
            .filter(href => !href.includes('#'));

        return {
            title: pageTitle,
            content: cleaned,
            url: window.location.href,
            sidebarLinks: [...new Set(sidebarLinks)]
        };
    }""")
    return result


async def crawl_page(page, url_path: str) -> tuple[dict, list]:
    """Crawl a single page and return content + discovered links."""
    full_url = BASE_URL + url_path if url_path.startswith("/") else url_path

    try:
        await page.goto(full_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(0.5)  # Let JS render

        content = await extract_page_content(page)
        return content, content.get("sidebarLinks", [])
    except Exception as e:
        print(f"  ERROR crawling {full_url}: {e}")
        return None, []


async def save_page(url_path: str, content: dict):
    """Save page content to markdown file."""
    file_path = url_to_path(url_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    title = content.get("title", url_path)
    url = content.get("url", BASE_URL + url_path)
    page_content = content.get("content", "")

    markdown = f"""---
title: {title}
url: {url}
crawled_at: {time.strftime('%Y-%m-%d %H:%M:%S')}
---

{page_content}
"""

    file_path.write_text(markdown, encoding="utf-8")
    return file_path


async def discover_sub_pages(page, url_path: str) -> list[str]:
    """Visit a page and discover all sub-page links in the navigation."""
    full_url = BASE_URL + url_path
    try:
        await page.goto(full_url, wait_until="networkidle", timeout=30000)
        await asyncio.sleep(0.5)

        links = await page.evaluate("""() => {
            return Array.from(document.querySelectorAll('nav a, aside a, [role="navigation"] a'))
                .map(a => a.getAttribute('href'))
                .filter(href => href && href.includes('/docs/surrealql') && !href.includes('#'))
                .filter((v, i, a) => a.indexOf(v) === i);
        }""")
        return links
    except Exception as e:
        print(f"  ERROR discovering {full_url}: {e}")
        return []


async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    visited = set()
    to_visit = list(SEED_URLS)
    discovered_extra = []
    all_pages_info = {}

    print(f"Starting ultra crawl of SurrealQL docs...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Total seed URLs: {len(to_visit)}")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        # Phase 1: Discover ALL pages from sidebar navigation
        print("\n[Phase 1] Discovering all pages from navigation...")
        discovery_page = await discover_sub_pages(page, "/docs/surrealql")
        for link in discovery_page:
            if link not in to_visit and link not in visited:
                discovered_extra.append(link)
                print(f"  + Discovered: {link}")

        # Check ALTER, DEFINE, and function pages for sub-pages
        expand_pages = [
            "/docs/surrealql/statements/alter",
            "/docs/surrealql/statements/define",
            "/docs/surrealql/functions/database",
        ]
        for ep in expand_pages:
            print(f"  Checking sub-pages of {ep}...")
            sub_links = await discover_sub_pages(page, ep)
            for link in sub_links:
                if link not in to_visit and link not in visited:
                    discovered_extra.append(link)
                    print(f"    + Discovered: {link}")

        # Merge all discovered unique URLs
        all_urls = list(dict.fromkeys(to_visit + discovered_extra))
        print(f"\n[Phase 1] Total URLs to crawl: {len(all_urls)}")

        # Phase 2: Crawl all pages
        print("\n[Phase 2] Crawling all pages...")
        success_count = 0
        error_count = 0

        for i, url_path in enumerate(all_urls):
            if url_path in visited:
                continue

            # Normalize URL
            if url_path.startswith("http"):
                url_path = url_path.replace(BASE_URL, "")

            if not url_path.startswith("/docs/surrealql"):
                continue

            print(f"  [{i+1}/{len(all_urls)}] {url_path}")

            content, extra_links = await crawl_page(page, url_path)
            visited.add(url_path)

            if content and content.get("content"):
                file_path = await save_page(url_path, content)
                print(f"    -> Saved: {file_path.relative_to(OUTPUT_DIR.parent)} ({len(content['content'])} chars)")
                all_pages_info[url_path] = {
                    "title": content.get("title", ""),
                    "file": str(file_path.relative_to(OUTPUT_DIR.parent)),
                    "chars": len(content.get("content", "")),
                }
                success_count += 1

                # Discover additional pages from this page's sidebar
                for link in extra_links:
                    if link not in visited and link not in all_urls:
                        if link.startswith("/docs/surrealql"):
                            all_urls.append(link)
                            print(f"    + New link discovered: {link}")
            else:
                print(f"    -> ERROR: No content extracted")
                error_count += 1

            # Small delay to be respectful
            await asyncio.sleep(0.3)

        await browser.close()

    # Phase 3: Save index
    print("\n[Phase 3] Saving index...")
    index_path = OUTPUT_DIR / "INDEX.md"

    index_content = "# SurrealQL Documentation Index\n\n"
    index_content += f"Crawled at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    index_content += f"Total pages: {success_count}\n\n"

    # Group by section
    sections = {}
    for url_path, info in sorted(all_pages_info.items()):
        parts = url_path.strip("/").split("/")
        if len(parts) >= 3:
            section = parts[2] if len(parts) > 3 else "root"
        else:
            section = "root"
        sections.setdefault(section, []).append((url_path, info))

    for section, pages in sorted(sections.items()):
        index_content += f"\n## {section.title()}\n\n"
        for url_path, info in pages:
            title = info.get("title", url_path)
            file_rel = info.get("file", "")
            chars = info.get("chars", 0)
            index_content += f"- [{title}]({file_rel}) — {chars} chars\n"

    index_path.write_text(index_content, encoding="utf-8")

    # Save JSON manifest
    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(all_pages_info, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"DONE! Successfully crawled {success_count} pages, {error_count} errors.")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Index: {index_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    asyncio.run(main())
