#!/usr/bin/env python3
"""Compare live SurrealQL docs sidebar links vs docs3/ crawled contents."""

import json
from pathlib import Path

# Live site links extracted via playwright-cli (2026-03-25)
LIVE_LINKS = [
    {"text": "Overview", "href": "/docs/surrealql"},
    {"text": "Demo data", "href": "/docs/surrealql/demo"},
    {"text": "Operators", "href": "/docs/surrealql/operators"},
    {"text": "Introduction", "href": "/docs/surrealql/datamodel"},
    {"text": "Arrays", "href": "/docs/surrealql/datamodel/arrays"},
    {"text": "Booleans", "href": "/docs/surrealql/datamodel/booleans"},
    {"text": "Bytes", "href": "/docs/surrealql/datamodel/bytes"},
    {"text": "Closures", "href": "/docs/surrealql/datamodel/closures"},
    {"text": "Datetimes", "href": "/docs/surrealql/datamodel/datetimes"},
    {"text": "Durations", "href": "/docs/surrealql/datamodel/durations"},
    {"text": "Files", "href": "/docs/surrealql/datamodel/files"},
    {"text": "Futures", "href": "/docs/surrealql/datamodel/futures"},
    {"text": "Geometries", "href": "/docs/surrealql/datamodel/geometries"},
    {"text": "None and Null", "href": "/docs/surrealql/datamodel/none-and-null"},
    {"text": "Numbers", "href": "/docs/surrealql/datamodel/numbers"},
    {"text": "Objects", "href": "/docs/surrealql/datamodel/objects"},
    {"text": "Ranges", "href": "/docs/surrealql/datamodel/ranges"},
    {"text": "Record IDs", "href": "/docs/surrealql/datamodel/ids"},
    {"text": "Regex", "href": "/docs/surrealql/datamodel/regex"},
    {"text": "Sets", "href": "/docs/surrealql/datamodel/sets"},
    {"text": "Strings", "href": "/docs/surrealql/datamodel/strings"},
    {"text": "UUIDs", "href": "/docs/surrealql/datamodel/uuid"},
    {"text": "Values", "href": "/docs/surrealql/datamodel/values"},
    {"text": "Casting", "href": "/docs/surrealql/datamodel/casting"},
    {"text": "Formatters", "href": "/docs/surrealql/datamodel/formatters"},
    {"text": "Literals", "href": "/docs/surrealql/datamodel/literals"},
    {"text": "Idioms", "href": "/docs/surrealql/datamodel/idioms"},
    {"text": "Record links", "href": "/docs/surrealql/datamodel/records"},
    {"text": "Record references", "href": "/docs/surrealql/datamodel/references"},
    {"text": "Introduction", "href": "/docs/surrealql/statements"},
    {"text": "ACCESS", "href": "/docs/surrealql/statements/access"},
    {"text": "ALTER", "href": "/docs/surrealql/statements/alter/"},
    {"text": "DATABASE", "href": "/docs/surrealql/statements/alter/database"},
    {"text": "FIELD", "href": "/docs/surrealql/statements/alter/field"},
    {"text": "INDEX", "href": "/docs/surrealql/statements/alter/indexes"},
    {"text": "NAMESPACE", "href": "/docs/surrealql/statements/alter/namespace"},
    {"text": "SEQUENCE", "href": "/docs/surrealql/statements/alter/sequence"},
    {"text": "SYSTEM", "href": "/docs/surrealql/statements/alter/system"},
    {"text": "TABLE", "href": "/docs/surrealql/statements/alter/table"},
    {"text": "BEGIN", "href": "/docs/surrealql/statements/begin"},
    {"text": "BREAK", "href": "/docs/surrealql/statements/break"},
    {"text": "CANCEL", "href": "/docs/surrealql/statements/cancel"},
    {"text": "COMMIT", "href": "/docs/surrealql/statements/commit"},
    {"text": "CONTINUE", "href": "/docs/surrealql/statements/continue"},
    {"text": "CREATE", "href": "/docs/surrealql/statements/create"},
    {"text": "DEFINE", "href": "/docs/surrealql/statements/define/"},
    {"text": "DEFINE ACCESS", "href": "/docs/surrealql/statements/define/access/"},
    {"text": "BEARER", "href": "/docs/surrealql/statements/define/access/bearer"},
    {"text": "JWT", "href": "/docs/surrealql/statements/define/access/jwt"},
    {"text": "RECORD", "href": "/docs/surrealql/statements/define/access/record"},
    {"text": "DEFINE ANALYZER", "href": "/docs/surrealql/statements/define/analyzer"},
    {"text": "DEFINE API", "href": "/docs/surrealql/statements/define/api"},
    {"text": "DEFINE BUCKET", "href": "/docs/surrealql/statements/define/bucket"},
    {"text": "DEFINE CONFIG", "href": "/docs/surrealql/statements/define/config"},
    {"text": "DEFINE DATABASE", "href": "/docs/surrealql/statements/define/database"},
    {"text": "DEFINE EVENT", "href": "/docs/surrealql/statements/define/event"},
    {"text": "DEFINE FIELD", "href": "/docs/surrealql/statements/define/field"},
    {"text": "DEFINE FUNCTION", "href": "/docs/surrealql/statements/define/function"},
    {"text": "DEFINE INDEX", "href": "/docs/surrealql/statements/define/indexes"},
    {"text": "DEFINE MODULE", "href": "/docs/surrealql/statements/define/module"},
    {"text": "DEFINE NAMESPACE", "href": "/docs/surrealql/statements/define/namespace"},
    {"text": "DEFINE PARAM", "href": "/docs/surrealql/statements/define/param"},
    {"text": "DEFINE SCOPE", "href": "/docs/surrealql/statements/define/scope"},
    {"text": "DEFINE SEQUENCE", "href": "/docs/surrealql/statements/define/sequence"},
    {"text": "DEFINE TABLE", "href": "/docs/surrealql/statements/define/table"},
    {"text": "DEFINE TOKEN", "href": "/docs/surrealql/statements/define/token"},
    {"text": "DEFINE USER", "href": "/docs/surrealql/statements/define/user"},
    {"text": "DELETE", "href": "/docs/surrealql/statements/delete"},
    {"text": "EXPLAIN", "href": "/docs/surrealql/statements/explain"},
    {"text": "FOR", "href": "/docs/surrealql/statements/for"},
    {"text": "IF ELSE", "href": "/docs/surrealql/statements/ifelse"},
    {"text": "INFO", "href": "/docs/surrealql/statements/info"},
    {"text": "INSERT", "href": "/docs/surrealql/statements/insert"},
    {"text": "KILL", "href": "/docs/surrealql/statements/kill"},
    {"text": "LET", "href": "/docs/surrealql/statements/let"},
    {"text": "LIVE", "href": "/docs/surrealql/statements/live"},
    {"text": "REBUILD", "href": "/docs/surrealql/statements/rebuild"},
    {"text": "RELATE", "href": "/docs/surrealql/statements/relate"},
    {"text": "REMOVE", "href": "/docs/surrealql/statements/remove"},
    {"text": "RETURN", "href": "/docs/surrealql/statements/return"},
    {"text": "SELECT", "href": "/docs/surrealql/statements/select"},
    {"text": "SHOW", "href": "/docs/surrealql/statements/show"},
    {"text": "SLEEP", "href": "/docs/surrealql/statements/sleep"},
    {"text": "THROW", "href": "/docs/surrealql/statements/throw"},
    {"text": "UPDATE", "href": "/docs/surrealql/statements/update"},
    {"text": "UPSERT", "href": "/docs/surrealql/statements/upsert"},
    {"text": "USE", "href": "/docs/surrealql/statements/use"},
    {"text": "Parameters", "href": "/docs/surrealql/parameters"},
    {"text": "Introduction", "href": "/docs/surrealql/clauses"},
    {"text": "EXPLAIN", "href": "/docs/surrealql/clauses/explain"},
    {"text": "FETCH", "href": "/docs/surrealql/clauses/fetch"},
    {"text": "FROM", "href": "/docs/surrealql/clauses/from"},
    {"text": "GROUP BY", "href": "/docs/surrealql/clauses/group-by"},
    {"text": "LIMIT", "href": "/docs/surrealql/clauses/limit"},
    {"text": "OMIT", "href": "/docs/surrealql/clauses/omit"},
    {"text": "ORDER BY", "href": "/docs/surrealql/clauses/order-by"},
    {"text": "SPLIT", "href": "/docs/surrealql/clauses/split"},
    {"text": "WHERE", "href": "/docs/surrealql/clauses/where"},
    {"text": "WITH", "href": "/docs/surrealql/clauses/with"},
    {"text": "Transactions", "href": "/docs/surrealql/transactions"},
    {"text": "Introduction", "href": "/docs/surrealql/functions"},
    {"text": "Database Functions", "href": "/docs/surrealql/functions/database/"},
    {"text": "API functions", "href": "/docs/surrealql/functions/database/api"},
    {"text": "Array functions", "href": "/docs/surrealql/functions/database/array"},
    {"text": "Bytes functions", "href": "/docs/surrealql/functions/database/bytes"},
    {"text": "Count function", "href": "/docs/surrealql/functions/database/count"},
    {"text": "Crypto functions", "href": "/docs/surrealql/functions/database/crypto"},
    {"text": "Duration functions", "href": "/docs/surrealql/functions/database/duration"},
    {"text": "Encoding functions", "href": "/docs/surrealql/functions/database/encoding"},
    {"text": "File functions", "href": "/docs/surrealql/functions/database/file"},
    {"text": "Geo functions", "href": "/docs/surrealql/functions/database/geo"},
    {"text": "HTTP functions", "href": "/docs/surrealql/functions/database/http"},
    {"text": "Math functions", "href": "/docs/surrealql/functions/database/math"},
    {"text": "Meta functions", "href": "/docs/surrealql/functions/database/meta"},
    {"text": "Not function", "href": "/docs/surrealql/functions/database/not"},
    {"text": "Object functions", "href": "/docs/surrealql/functions/database/object"},
    {"text": "Parse functions", "href": "/docs/surrealql/functions/database/parse"},
    {"text": "Rand functions", "href": "/docs/surrealql/functions/database/rand"},
    {"text": "Record functions", "href": "/docs/surrealql/functions/database/record"},
    {"text": "Search functions", "href": "/docs/surrealql/functions/database/search"},
    {"text": "Sequence functions", "href": "/docs/surrealql/functions/database/sequence"},
    {"text": "Session functions", "href": "/docs/surrealql/functions/database/session"},
    {"text": "Set functions", "href": "/docs/surrealql/functions/database/set"},
    {"text": "Sleep function", "href": "/docs/surrealql/functions/database/sleep"},
    {"text": "String functions", "href": "/docs/surrealql/functions/database/string"},
    {"text": "Time functions", "href": "/docs/surrealql/functions/database/time"},
    {"text": "Type functions", "href": "/docs/surrealql/functions/database/type"},
    {"text": "Value functions", "href": "/docs/surrealql/functions/database/value"},
    {"text": "Vector functions", "href": "/docs/surrealql/functions/database/vector"},
    {"text": "JavaScript functions", "href": "/docs/surrealql/functions/script/"},
    {"text": "Arguments", "href": "/docs/surrealql/functions/script/arguments"},
    {"text": "Built-in functions", "href": "/docs/surrealql/functions/script/built-in-functions"},
    {"text": "Function context", "href": "/docs/surrealql/functions/script/context"},
    {"text": "Type conversion", "href": "/docs/surrealql/functions/script/type-conversion"},
    {"text": "SurrealQL functions", "href": "/docs/surrealql/functions/script/surrealql-functions"},
    {"text": "SurrealML Functions", "href": "/docs/surrealql/functions/ml/"},
    {"text": "Machine learning functions", "href": "/docs/surrealql/functions/ml/functions"},
    {"text": "Comments", "href": "/docs/surrealql/comments"},
]

DOCS3_DIR = Path("docs3")
MANIFEST  = DOCS3_DIR / "manifest.json"


def norm(path: str) -> str:
    """Normalize path: strip trailing slash, ensure no double slashes."""
    return path.rstrip("/") or path


def path_to_file(path: str) -> Path:
    """Convert URL path to expected docs3 file path (mirrors crawl3.py logic)."""
    parts = path.lstrip("/").split("/")
    if len(parts) <= 1:
        return DOCS3_DIR / f"{parts[0] or 'index'}.md"
    return DOCS3_DIR.joinpath(*parts[:-1]) / f"{parts[-1]}.md"


def main():
    # --- live site paths (deduplicated, normalized) ---
    live_paths = {}
    for link in LIVE_LINKS:
        p = norm(link["href"])
        live_paths[p] = link["text"]

    # --- docs3 manifest paths ---
    manifest = json.loads(MANIFEST.read_text())
    crawled_paths = {}
    for path, info in manifest["pages"].items():
        p = norm(path)
        crawled_paths[p] = info

    live_set    = set(live_paths.keys())
    crawled_set = set(crawled_paths.keys())

    # --- also check actual .md files on disk ---
    disk_files = set()
    for f in DOCS3_DIR.rglob("*.md"):
        if f.name in ("INDEX.md",):
            continue
        rel = str(f.relative_to(DOCS3_DIR)).removesuffix(".md")
        disk_files.add("/" + rel)

    print("=" * 70)
    print("SurrealQL Docs — Live Site vs docs3/ Comparison")
    print("=" * 70)
    print(f"\nLive sidebar links (unique paths): {len(live_set)}")
    print(f"docs3/ manifest pages:             {len(crawled_set)}")
    print(f"docs3/ .md files on disk:          {len(disk_files)}")

    # 1. Pages on live site but NOT in docs3/
    only_live = sorted(live_set - crawled_set)
    print(f"\n{'─'*70}")
    print(f"MISSING from docs3/ (on live site but not crawled): {len(only_live)}")
    print(f"{'─'*70}")
    for p in only_live:
        expected = path_to_file(p)
        on_disk = expected.exists()
        print(f"  {p:55s}  [{live_paths[p]}]  disk={'YES' if on_disk else 'NO'}")

    # 2. Pages in docs3/ but NOT on live site sidebar
    only_crawled = sorted(crawled_set - live_set)
    print(f"\n{'─'*70}")
    print(f"EXTRA in docs3/ (crawled but not in live sidebar): {len(only_crawled)}")
    print(f"{'─'*70}")
    for p in only_crawled:
        info = crawled_paths[p]
        print(f"  {p:55s}  [{info['title']}]  {info['chars']:,} chars")

    # 3. Pages present in both — compare titles
    both = sorted(live_set & crawled_set)
    title_mismatches = []
    for p in both:
        live_title = live_paths[p]
        crawled_title = crawled_paths[p]["title"]
        if live_title.lower() != crawled_title.lower():
            title_mismatches.append((p, live_title, crawled_title))

    print(f"\n{'─'*70}")
    print(f"Title mismatches (sidebar vs crawled h1): {len(title_mismatches)}")
    print(f"{'─'*70}")
    for p, lt, ct in title_mismatches:
        print(f"  {p}")
        print(f"    sidebar:  {lt}")
        print(f"    crawled:  {ct}")

    # 4. Disk files not in manifest
    disk_not_manifest = sorted(disk_files - crawled_set)
    print(f"\n{'─'*70}")
    print(f"Disk .md files not in manifest: {len(disk_not_manifest)}")
    print(f"{'─'*70}")
    for p in disk_not_manifest:
        print(f"  {p}")

    # 5. Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"  Live sidebar unique pages:  {len(live_set)}")
    print(f"  docs3/ crawled pages:       {len(crawled_set)}")
    print(f"  In both:                    {len(both)}")
    print(f"  Missing from docs3/:        {len(only_live)}")
    print(f"  Extra in docs3/:            {len(only_crawled)}")
    print(f"  Title mismatches:           {len(title_mismatches)}")
    print(f"  Coverage:                   {len(both)/len(live_set)*100:.1f}%")


if __name__ == "__main__":
    main()
