#!/usr/bin/env python3
"""Render contributions.json as an animated SVG heatmap."""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"
STATIC = os.environ.get("STATIC") == "1"

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG = "#0d1117"
BORDER = "#21262d"
FG = "#c9d1d9"
MUTED = "#7d8590"
ACCENT = "#39d353"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

CELL = 11
GAP = 3
PITCH = CELL + GAP
RADIUS = 2.5
PAD = 22
LABEL_W = 30
TITLEBAR_H = 34
WIDTH = 860
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def sunday_index(value: date) -> int:
    return (value.weekday() + 1) % 7


def boost_level(level: int, count: int, peak: int) -> int:
    if level >= 4 and peak > 0 and count >= max(peak * 0.75, 1):
        return 5
    return max(0, min(level, 5))


def layout(days: list[dict], peak: int) -> tuple[list[dict], int]:
    cells = []
    week = 0
    previous_row: int | None = None
    for item in days:
        dt = date.fromisoformat(item["date"])
        row = sunday_index(dt)
        if previous_row is not None and row <= previous_row:
            week += 1
        previous_row = row
        cells.append(
            {
                "date": item["date"],
                "dt": dt,
                "count": item["count"],
                "level": boost_level(item["level"], item["count"], peak),
                "week": week,
                "row": row,
            }
        )
    return cells, week + 1


def build(payload: dict) -> str:
    cells, weeks = layout(payload["days"], payload["stats"]["max_count"])
    grid_x = PAD + LABEL_W
    grid_y = TITLEBAR_H + 16 + 18
    grid_h = 7 * PITCH - GAP
    grid_w = weeks * PITCH - GAP
    legend_y = grid_y + grid_h + 26
    footer_y = legend_y + 30
    height = footer_y + 16

    shift = max(0, (WIDTH - (grid_x + grid_w + PAD)) // 2)
    gx = grid_x + shift

    out: list[str] = []
    add = out.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" '
        f'aria-label="{payload["stats"]["total"]:,} contributions in the last year">'
    )

    if STATIC:
        styles = ".cell,.fade{opacity:1}"
    else:
        styles = (
            "@keyframes pop{from{opacity:0;transform:translateY(-7px) scale(.55)}"
            "to{opacity:1;transform:translateY(0) scale(1)}}"
            "@keyframes fadeup{from{opacity:0;transform:translateY(5px)}"
            "to{opacity:1;transform:translateY(0)}}"
            ".cell{opacity:0;transform-box:fill-box;transform-origin:center;"
            "animation:pop .5s cubic-bezier(.2,.8,.3,1) forwards}"
            ".fade{opacity:0;animation:fadeup .6s ease-out forwards}"
        )
    add(f'<style>.mono{{font-family:{MONO};}}{styles}</style>')

    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )
    add(f'<line x1="0" y1="{TITLEBAR_H}" x2="{WIDTH}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>')
    for index, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        add(f'<circle cx="{22 + index * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')
    add(
        f'<text class="mono" x="82" y="{TITLEBAR_H / 2 + 4}" font-size="12" fill="{MUTED}">'
        f'contributions --user {escape(payload["username"])} --last-year</text>'
    )

    seen_months: set[tuple[int, int]] = set()
    previous_label_week = -99
    for cell in cells:
        key = (cell["dt"].year, cell["dt"].month)
        if key in seen_months or cell["week"] - previous_label_week < 3:
            continue
        seen_months.add(key)
        previous_label_week = cell["week"]
        x = gx + cell["week"] * PITCH
        add(
            f'<text class="mono fade" x="{x}" y="{grid_y - 7}" font-size="10.5" fill="{MUTED}" '
            f'style="animation-delay:.15s">{MONTHS[cell["dt"].month - 1]}</text>'
        )

    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = grid_y + row * PITCH + CELL - 2
        add(
            f'<text class="mono fade" x="{gx - 8}" y="{y}" font-size="10" fill="{MUTED}" '
            f'text-anchor="end" style="animation-delay:.15s">{label}</text>'
        )

    for cell in cells:
        x = gx + cell["week"] * PITCH
        y = grid_y + cell["row"] * PITCH
        delay = 0.25 + (cell["week"] + cell["row"] * 1.6) * 0.014
        style = "" if STATIC else f' style="animation-delay:{delay:.3f}s"'
        label = f'{cell["count"]} contribution{("" if cell["count"] == 1 else "s")} on {cell["date"]}'
        add(
            f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RADIUS}" '
            f'fill="{PALETTE[cell["level"]]}"{style}><title>{escape(label)}</title></rect>'
        )

    tail = 0.25 + (weeks + 6 * 1.6) * 0.014

    def delayed(extra: float) -> str:
        return "" if STATIC else f' style="animation-delay:{tail + extra:.2f}s"'

    box = 10
    legend_boxes = len(PALETTE)
    lx = gx + grid_w
    lx_start = lx - (legend_boxes * (box + 3) - 3) - 74
    add(
        f'<text class="mono fade" x="{lx_start - 8}" y="{legend_y + 9}" font-size="10.5" fill="{MUTED}" '
        f'text-anchor="end"{delayed(0.05)}>Less</text>'
    )
    for index, colour in enumerate(PALETTE):
        style = "" if STATIC else f' style="animation-delay:{tail + 0.05 + index * 0.05:.2f}s"'
        add(
            f'<rect class="cell" x="{lx_start + index * (box + 3)}" y="{legend_y}" width="{box}" '
            f'height="{box}" rx="2" fill="{colour}"{style}/>'
        )
    add(
        f'<text class="mono fade" x="{lx_start + legend_boxes * (box + 3) + 5}" y="{legend_y + 9}" '
        f'font-size="10.5" fill="{MUTED}"{delayed(0.35)}>More</text>'
    )

    stats = payload["stats"]
    add(
        f'<text class="mono fade" x="{gx}" y="{footer_y}" font-size="12.5" fill="{FG}"{delayed(0.15)}>'
        f'<tspan fill="{ACCENT}" font-weight="600">{stats["total"]:,}</tspan>'
        f'<tspan fill="{FG}"> contributions in the last year</tspan></text>'
    )
    right = (
        f'{stats["current_streak"]}d current  ·  {stats["longest_streak"]}d longest  ·  '
        f'{stats["active_days"]} active days  ·  peak {stats["max_count"]}'
    )
    add(
        f'<text class="mono fade" x="{gx + grid_w}" y="{footer_y}" font-size="11" fill="{MUTED}" '
        f'text-anchor="end"{delayed(0.25)}>{escape(right)}</text>'
    )
    add("</svg>")
    return "".join(out)


def main() -> None:
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; run fetch_contributions.py first")
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.write_text(build(payload) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
