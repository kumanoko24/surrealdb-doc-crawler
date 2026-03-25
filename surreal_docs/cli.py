"""CLI entry point — surreal-docs discover | crawl | diff."""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

from . import core

SNAPSHOTS = Path("snapshots")


# ── Subcommands ───────────────────────────────────────────────────────────────

def cmd_discover(_args):
    """List all doc pages from the live site sidebar."""
    links = asyncio.run(core.discover())
    for link in links:
        print(f"  {link['href']:55s}  {link['text']}")
    print(f"\n{len(links)} pages discovered")


def cmd_crawl(_args):
    """Full BFS crawl → timestamped snapshot under snapshots/."""
    ts = time.strftime("%Y-%m-%dT%H-%M-%S")
    output_dir = SNAPSHOTS / ts

    asyncio.run(core.crawl(output_dir))

    # Update 'latest' symlink
    latest = SNAPSHOTS / "latest"
    if latest.is_symlink() or latest.exists():
        latest.unlink()
    latest.symlink_to(ts)

    print(f"\nSnapshot: {output_dir}")
    print(f"Symlink:  {latest} → {ts}")


def cmd_diff(args):
    """Compare two snapshots (or any two directories with manifest.json)."""
    # Resolve new (right-hand side)
    if args.new:
        new_dir = Path(args.new)
    else:
        new_dir = _resolve_latest()

    if not new_dir or not (new_dir / "manifest.json").exists():
        print(f"No manifest.json in {new_dir}. Run 'surreal-docs crawl' first.", file=sys.stderr)
        sys.exit(1)

    # Resolve old (left-hand side)
    if args.old:
        old_dir = Path(args.old)
    else:
        old_dir = _resolve_previous(new_dir)

    if not old_dir or not (old_dir / "manifest.json").exists():
        print(f"Cannot find a previous snapshot to diff against.", file=sys.stderr)
        print(f"Usage: surreal-docs diff <old-dir> <new-dir>", file=sys.stderr)
        sys.exit(1)

    old_m = core.load_manifest(old_dir)
    new_m = core.load_manifest(new_dir)
    diff  = core.diff_manifests(old_m, new_m)

    _print_diff(old_dir, new_dir, diff)

    # Also write machine-readable JSON
    if args.json:
        print(json.dumps(diff, indent=2, ensure_ascii=False))


# ── Helpers ───────────────────────────────────────────────────────────────────

def _resolve_latest() -> Path | None:
    """Find the latest snapshot."""
    latest = SNAPSHOTS / "latest"
    if latest.is_symlink() or latest.exists():
        return latest.resolve()
    dirs = _snapshot_dirs()
    return dirs[-1] if dirs else None


def _resolve_previous(current: Path) -> Path | None:
    """Find the snapshot right before `current`."""
    dirs = _snapshot_dirs()
    others = [d for d in dirs if d.resolve() != current.resolve()]
    return others[-1] if others else None


def _snapshot_dirs() -> list[Path]:
    """List snapshot directories sorted by name (ascending)."""
    if not SNAPSHOTS.exists():
        return []
    return sorted(
        d for d in SNAPSHOTS.iterdir()
        if d.is_dir() and d.name != "latest"
    )


def _print_diff(old_dir: Path, new_dir: Path, diff: dict):
    """Human-readable diff report."""
    print(f"Comparing: {old_dir.name} → {new_dir.name}")
    print("=" * 65)

    added   = diff["added"]
    removed = diff["removed"]
    changed = diff["changed"]

    if added:
        print(f"\n+ ADDED ({len(added)} pages):")
        for p in added:
            print(f"  + {p['path']:50s}  {p.get('title','')}")

    if removed:
        print(f"\n- REMOVED ({len(removed)} pages):")
        for p in removed:
            print(f"  - {p['path']:50s}  {p.get('title','')}")

    if changed:
        print(f"\n~ CHANGED ({len(changed)} pages):")
        for p in changed:
            delta = p["new_chars"] - p["old_chars"]
            sign = "+" if delta >= 0 else ""
            print(f"  ~ {p['path']:50s}  {sign}{delta} chars  ({p['old_chars']:,} → {p['new_chars']:,})")

    print(f"\n  Unchanged: {diff['unchanged']} pages")

    if not added and not removed and not changed:
        print("\n  No changes detected.")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="surreal-docs",
        description="SurrealDB docs crawler — crawl, snapshot, and diff SurrealQL documentation",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("discover", help="List all doc pages from live site sidebar")
    sub.add_parser("crawl",    help="Crawl all pages → new timestamped snapshot")

    diff_p = sub.add_parser("diff", help="Compare two snapshots")
    diff_p.add_argument("old",    nargs="?", help="Old snapshot dir (default: previous)")
    diff_p.add_argument("new",    nargs="?", help="New snapshot dir (default: latest)")
    diff_p.add_argument("--json", action="store_true", help="Also print JSON diff")

    args = parser.parse_args()
    {"discover": cmd_discover, "crawl": cmd_crawl, "diff": cmd_diff}[args.command](args)
