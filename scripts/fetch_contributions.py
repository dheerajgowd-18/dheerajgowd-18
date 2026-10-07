#!/usr/bin/env python3
"""Fetch a GitHub user's public contribution calendar and save normalized JSON.

No GraphQL token is used. The workflow reads GitHub's public contribution-calendar
HTML and extracts each day's date, count, and level.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GITHUB_USERNAME", "dheerajgowd-18")
URL = f"https://github.com/users/{USERNAME}/contributions"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "contributions.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/142.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml",
    "X-Requested-With": "XMLHttpRequest",
}

COUNT_RE = re.compile(r"^\s*(No|[\d,]+)\s+contribution", re.IGNORECASE)


def fetch_html(url: str, attempts: int = 3) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            print(f"attempt {attempt}/{attempts} failed: {exc}", file=sys.stderr)
    raise SystemExit(f"could not fetch {url}: {last_error}")


def parse_days(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    tooltip_counts: dict[str, int] = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if not target:
            continue
        match = COUNT_RE.match(tip.get_text(" ", strip=True))
        if not match:
            continue
        raw = match.group(1)
        tooltip_counts[target] = 0 if raw.lower() == "no" else int(raw.replace(",", ""))

    days: dict[str, dict] = {}
    for cell in soup.select("td.ContributionCalendar-day"):
        iso = cell.get("data-date")
        if not iso:
            continue
        raw_count = cell.get("data-count")
        count = (
            int(raw_count)
            if raw_count and raw_count.isdigit()
            else tooltip_counts.get(cell.get("id", ""), 0)
        )
        level_raw = cell.get("data-level") or "0"
        try:
            level = int(level_raw)
        except ValueError:
            level = 0
        days[iso] = {"date": iso, "count": count, "level": level}

    if not days:
        raise SystemExit(
            "parsed 0 contribution days; GitHub's HTML may have changed or the profile is unavailable"
        )

    return [days[key] for key in sorted(days)]


def compute_stats(days: list[dict]) -> dict:
    counts = {item["date"]: item["count"] for item in days}
    total = sum(counts.values())
    active = [item for item in days if item["count"] > 0]

    longest = 0
    current_run = 0
    longest_end: date | None = None
    previous: date | None = None

    for item in days:
        current = date.fromisoformat(item["date"])
        if item["count"] > 0 and previous is not None and current - previous == timedelta(days=1):
            current_run += 1
        elif item["count"] > 0:
            current_run = 1
        else:
            current_run = 0
        if current_run > longest:
            longest = current_run
            longest_end = current
        previous = current

    reversed_days = list(reversed(days))
    offset = 1 if reversed_days and reversed_days[0]["count"] == 0 else 0
    current_streak = 0
    for item in reversed_days[offset:]:
        if item["count"] == 0:
            break
        current_streak += 1

    best = max(days, key=lambda item: item["count"])

    monthly: OrderedDict[str, int] = OrderedDict()
    for item in days:
        key = item["date"][:7]
        monthly[key] = monthly.get(key, 0) + item["count"]

    return {
        "total": total,
        "active_days": len(active),
        "max_count": best["count"],
        "best_day": {"date": best["date"], "count": best["count"]},
        "current_streak": current_streak,
        "longest_streak": longest,
        "longest_streak_end": longest_end.isoformat() if longest_end else None,
        "daily_average": round(total / len(days), 2) if days else 0,
        "monthly": monthly,
    }


def main() -> None:
    print(f"fetching {URL}")
    days = parse_days(fetch_html(URL))
    stats = compute_stats(days)

    payload = {
        "username": USERNAME,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"start": days[0]["date"], "end": days[-1]["date"]},
        "stats": stats,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT.relative_to(ROOT)} | {len(days)} days | "
        f"{stats['total']:,} contributions | current streak {stats['current_streak']}d"
    )


if __name__ == "__main__":
    main()
