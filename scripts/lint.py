#!/usr/bin/env python3
"""Basic lint checker for this LLM-Wiki repository.

Checks:
1) required directories exist
2) required core files exist
3) wiki/index.md exists
4) wiki/log.md exists
5) markdown links inside wiki/ resolve (best-effort)
6) index rows use relative .md links
7) raw directory is present
8) outputs files exist
9) orphan pages count (no inbound links, excluding index/log/overview/QUESTIONS)
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
RAW = ROOT / "raw"
OUTPUTS = ROOT / "outputs"

REQUIRED_DIRS = [
    ROOT / "raw",
    ROOT / "wiki",
    ROOT / "outputs",
    ROOT / "references",
    ROOT / "scripts",
]

REQUIRED_FILES = [
    ROOT / "wiki" / "index.md",
    ROOT / "wiki" / "log.md",
    ROOT / "wiki" / "overview.md",
    ROOT / "wiki" / "QUESTIONS.md",
    ROOT / "outputs" / "lint.md",
    ROOT / "outputs" / "query.md",
]

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def check_exists(paths: list[Path], issues: list[str], label: str) -> None:
    for path in paths:
        if not path.exists():
            issues.append(f"Missing {label}: {path.relative_to(ROOT)}")


def markdown_files(base: Path) -> list[Path]:
    return [p for p in base.rglob("*.md") if p.is_file()]


def resolve_link(src_file: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://"):
        return None
    if target.startswith("#"):
        return None
    clean = target.split("#", 1)[0]
    return (src_file.parent / clean).resolve()


def check_links(issues: list[str]) -> None:
    for md in markdown_files(WIKI):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for link in LINK_RE.findall(text):
            resolved = resolve_link(md, link)
            if resolved is None:
                continue
            if not resolved.exists():
                issues.append(
                    f"Broken link in {md.relative_to(ROOT)} -> {link}"
                )


def check_index_links(issues: list[str]) -> None:
    index_file = WIKI / "index.md"
    if not index_file.exists():
        return
    text = index_file.read_text(encoding="utf-8", errors="ignore")
    for link in LINK_RE.findall(text):
        if link.startswith("http"):
            continue
        if not link.endswith(".md"):
            issues.append(f"Non-markdown index link: {link}")


def count_orphans() -> int:
    pages = [
        p for p in markdown_files(WIKI)
        if p.name not in {"index.md", "log.md", "overview.md", "QUESTIONS.md"}
    ]
    inbound = {p: 0 for p in pages}
    by_name = {p.name: p for p in pages}

    for md in markdown_files(WIKI):
        text = md.read_text(encoding="utf-8", errors="ignore")
        for link in LINK_RE.findall(text):
            if link.startswith("http") or link.startswith("#"):
                continue
            target_name = Path(link.split("#", 1)[0]).name
            target = by_name.get(target_name)
            if target is not None and target != md:
                inbound[target] += 1

    return sum(1 for c in inbound.values() if c == 0)


def main() -> int:
    issues: list[str] = []

    check_exists(REQUIRED_DIRS, issues, "directory")
    check_exists(REQUIRED_FILES, issues, "file")

    if not RAW.exists():
        issues.append("raw/ not found")

    if not OUTPUTS.exists():
        issues.append("outputs/ not found")

    if WIKI.exists():
        check_links(issues)
        check_index_links(issues)

    orphan_count = count_orphans() if WIKI.exists() else 0

    report_lines = [
        "# Lint Report",
        "",
        f"- Total issues: {len(issues)}",
        f"- Orphan pages: {orphan_count}",
        "",
    ]

    if issues:
        report_lines.append("## Issues")
        report_lines.append("")
        report_lines.extend([f"- {i}" for i in issues])
    else:
        report_lines.append("## Status")
        report_lines.append("")
        report_lines.append("- No deterministic issues detected.")

    out = ROOT / "outputs" / "lint.md"
    out.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(f"Lint complete. Issues={len(issues)}, orphans={orphan_count}")
    print(f"Report: {out.relative_to(ROOT)}")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
