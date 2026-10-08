#!/usr/bin/env python3
"""Render contributions.json as an understated technical telemetry SVG."""

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

# Restrained palette: deep obsidian slate up to signature cyan
PALETTE = ["#0F141C", "#142834", "#1B4358", "#246786", "#3798C4", "#65D9FF"]
BG = "#080A0D"
BORDER = "#161D27"
CELL_EMPTY_BORDER = "#141B24"
FG = "#F2F4F7"
MUTED = "#8A949E"
SUBTLE = "#4D5B6A"
ACCENT = "#65D9FF"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

CELL = 11
GAP = 3
PITCH = CELL + GAP
RADIUS = 2
PAD = 24
LABEL_W = 28
HEADER_H = 28
WIDTH = 860
HEIGHT = 170
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
    grid_y = HEADER_H + 19
    grid_h = 7 * PITCH - GAP
    grid_w = weeks * PITCH - GAP
    footer_y = grid_y + grid_h + 15

    shift = max(0, (WIDTH - (grid_x + grid_w + PAD)) // 2)
    gx = grid_x + shift

    out: list[str] = []
    add = out.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="GitHub Contribution Telemetry: {payload["stats"]["total"]:,} contributions in the last year">'
    )

    if STATIC:
        styles = ".cell,.fade{opacity:1}"
    else:
        styles = (
            "@keyframes pop{from{opacity:0;transform:scale(.75)}to{opacity:1;transform:scale(1)}}"
            "@keyframes fadeup{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}"
            ".cell{opacity:0;transform-box:fill-box;transform-origin:center;"
            "animation:pop .35s cubic-bezier(.2,.8,.3,1) forwards}"
            ".fade{opacity:0;animation:fadeup .5s ease-out forwards}"
        )
    add(f"<style>.mono{{font-family:{MONO};}}{styles}</style>")

    # Outer container
    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="8" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Technical Header
    add(
        f'<text class="mono fade" x="{PAD}" y="18.5" font-size="10" font-weight="600" '
        f'fill="{FG}" letter-spacing="1.5">CONTRIBUTION TELEMETRY</text>'
    )
    add(f'<circle class="fade" cx="214" cy="15" r="2.8" fill="{ACCENT}"/>')
    add(
        f'<text class="mono fade" x="224" y="18.5" font-size="9" fill="{MUTED}" '
        f'letter-spacing="0.8">52-WEEK ACTIVITY MATRIX</text>'
    )
    add(
        f'<text class="mono fade" x="{WIDTH - PAD}" y="18.5" font-size="9" fill="{SUBTLE}" '
        f'text-anchor="end" letter-spacing="0.8">UTC // DAILY REFRESH</text>'
    )
    add(f'<line x1="0" y1="{HEADER_H}" x2="{WIDTH}" y2="{HEADER_H}" stroke="{BORDER}" stroke-width="1"/>')

    # Month Labels
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
            f'<text class="mono fade" x="{x}" y="{grid_y - 7}" font-size="9" fill="{MUTED}" '
            f'style="animation-delay:.1s">{MONTHS[cell["dt"].month - 1]}</text>'
        )

    # Day Labels
    for row, label in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        y = grid_y + row * PITCH + CELL - 2
        add(
            f'<text class="mono fade" x="{gx - 8}" y="{y}" font-size="8.5" fill="{MUTED}" '
            f'text-anchor="end" style="animation-delay:.1s">{label}</text>'
        )

    # Cells
    for cell in cells:
        x = gx + cell["week"] * PITCH
        y = grid_y + cell["row"] * PITCH
        delay = 0.15 + (cell["week"] + cell["row"] * 1.5) * 0.008
        style = "" if STATIC else f' style="animation-delay:{delay:.3f}s"'
        label = f'{cell["count"]} contribution{("" if cell["count"] == 1 else "s")} on {cell["date"]}'
        fill = PALETTE[cell["level"]]
        stroke_attr = f' stroke="{CELL_EMPTY_BORDER}" stroke-width="0.6"' if cell["level"] == 0 else ""
        add(
            f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="{RADIUS}" '
            f'fill="{fill}"{stroke_attr}{style}><title>{escape(label)}</title></rect>'
        )

    tail = 0.15 + (weeks + 6 * 1.5) * 0.008

    def delayed(extra: float) -> str:
        return "" if STATIC else f' style="animation-delay:{tail + extra:.2f}s"'

    stats = payload["stats"]

    # Footer metrics (left aligned)
    add(
        f'<text class="mono fade" x="{gx}" y="{footer_y}" font-size="11" fill="{MUTED}"{delayed(0.1)}>'
        f'<tspan fill="{FG}" font-weight="600">{stats["total"]:,}</tspan> contributions in last year '
        f'<tspan fill="{SUBTLE}">//</tspan> {stats["longest_streak"]}d max streak · {stats["active_days"]} active days'
        f'</text>'
    )

    # Understated Legend (right aligned)
    box = 9
    legend_boxes = len(PALETTE)
    lx = gx + grid_w
    lx_start = lx - (legend_boxes * (box + 2) - 2) - 34

    add(
        f'<text class="mono fade" x="{lx_start - 6}" y="{footer_y}" font-size="9" fill="{MUTED}" '
        f'text-anchor="end"{delayed(0.05)}>Less</text>'
    )
    for index, colour in enumerate(PALETTE):
        stroke_attr = f' stroke="{CELL_EMPTY_BORDER}" stroke-width="0.5"' if index == 0 else ""
        add(
            f'<rect class="fade" x="{lx_start + index * (box + 2)}" y="{footer_y - 8}" width="{box}" '
            f'height="{box}" rx="1.5" fill="{colour}"{stroke_attr}{delayed(0.05 + index * 0.03)}/>'
        )
    add(
        f'<text class="mono fade" x="{lx_start + legend_boxes * (box + 2) + 4}" y="{footer_y}" '
        f'font-size="9" fill="{MUTED}"{delayed(0.25)}>More</text>'
    )

    add("</svg>")
    return "".join(out)


def main() -> None:
    if not DATA.exists():
        raise SystemExit(f"missing {DATA}; run fetch_contributions.py first")
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.write_text(build(payload) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
