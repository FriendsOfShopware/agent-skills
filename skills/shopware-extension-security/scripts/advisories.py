#!/usr/bin/env python3
"""Fetch published Shopware advisories for extension security pattern research."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


API_ROOT = "https://api.github.com"
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch and filter published GitHub repository advisories."
    )
    parser.add_argument("--repo", default="shopware/shopware", help="GitHub owner/repo")
    parser.add_argument(
        "--format",
        choices=("table", "stats", "json"),
        default="table",
        help="output format",
    )
    parser.add_argument("--search", help="case-insensitive text/CWE/GHSA/CVE filter")
    parser.add_argument("--since", help="only advisories published on/after YYYY-MM-DD")
    parser.add_argument("--input", type=Path, help="read a cached API JSON response")
    return parser.parse_args()


def fetch_with_gh(repo: str) -> list[dict[str, Any]] | None:
    if not shutil.which("gh"):
        return None
    auth = subprocess.run(
        ["gh", "auth", "status", "-h", "github.com"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if auth.returncode != 0:
        return None
    result = subprocess.run(
        [
            "gh",
            "api",
            "--paginate",
            "--slurp",
            "-H",
            "Accept: application/vnd.github+json",
            f"/repos/{repo}/security-advisories?per_page=100",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    pages = json.loads(result.stdout)
    if pages and isinstance(pages[0], list):
        return [item for page in pages for item in page]
    return pages


def next_link(value: str | None) -> str | None:
    if not value:
        return None
    for part in value.split(","):
        match = re.match(r'\s*<([^>]+)>;\s*rel="([^"]+)"', part)
        if match and match.group(2) == "next":
            return match.group(1)
    return None


def fetch_public(repo: str) -> list[dict[str, Any]]:
    url: str | None = f"{API_ROOT}/repos/{repo}/security-advisories?per_page=100"
    records: list[dict[str, Any]] = []
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    while url:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "shopware-extension-security",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            page = json.load(response)
            if not isinstance(page, list):
                raise ValueError("GitHub returned a non-list advisory response")
            records.extend(page)
            url = next_link(response.headers.get("Link"))
    return records


def load_records(args: argparse.Namespace) -> list[dict[str, Any]]:
    if args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        data = fetch_with_gh(args.repo)
        if data is None:
            data = fetch_public(args.repo)
    if not isinstance(data, list):
        raise ValueError("advisory data must be a JSON list")
    return [
        record
        for record in data
        if record.get("state") == "published" and not record.get("withdrawn_at")
    ]


def searchable(record: dict[str, Any]) -> str:
    values = [
        record.get("ghsa_id"),
        record.get("cve_id"),
        record.get("summary"),
        record.get("description"),
        " ".join(record.get("cwe_ids") or []),
    ]
    return "\n".join(str(value) for value in values if value).casefold()


def filter_records(
    records: list[dict[str, Any]], args: argparse.Namespace
) -> list[dict[str, Any]]:
    if args.since and not re.match(r"^\d{4}-\d{2}-\d{2}$", args.since):
        raise ValueError("--since must use YYYY-MM-DD")
    query = args.search.casefold() if args.search else None
    filtered = []
    for record in records:
        published = str(record.get("published_at") or "")[:10]
        if args.since and published < args.since:
            continue
        if query and query not in searchable(record):
            continue
        filtered.append(record)
    return sorted(filtered, key=lambda item: item.get("published_at") or "", reverse=True)


def print_table(records: list[dict[str, Any]]) -> None:
    columns = ("published", "severity", "ghsa", "cve", "cwes", "summary")
    print("\t".join(columns))
    for record in records:
        row = (
            str(record.get("published_at") or "")[:10],
            str(record.get("severity") or ""),
            str(record.get("ghsa_id") or ""),
            str(record.get("cve_id") or ""),
            ",".join(record.get("cwe_ids") or []),
            str(record.get("summary") or "").replace("\t", " ").replace("\n", " "),
        )
        print("\t".join(row))


def print_stats(records: list[dict[str, Any]]) -> None:
    severity = Counter(str(record.get("severity") or "unknown") for record in records)
    years = Counter(str(record.get("published_at") or "unknown")[:4] for record in records)
    cwes = Counter(cwe for record in records for cwe in record.get("cwe_ids") or [])
    result = {
        "count": len(records),
        "severity": dict(sorted(severity.items())),
        "years": dict(sorted(years.items())),
        "cwes": [{"cwe": cwe, "count": count} for cwe, count in cwes.most_common()],
    }
    print(json.dumps(result, indent=2))


def main() -> int:
    args = parse_args()
    if not REPO_PATTERN.fullmatch(args.repo):
        print("error: --repo must be owner/repo", file=sys.stderr)
        return 2
    try:
        records = filter_records(load_records(args), args)
    except (OSError, ValueError, subprocess.SubprocessError, urllib.error.URLError) as error:
        print(f"error: unable to load advisories: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(records, indent=2))
    elif args.format == "stats":
        print_stats(records)
    else:
        print_table(records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
