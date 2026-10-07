#!/usr/bin/env python3
"""Render source-prepped.png as a self-typing monochrome ASCII SVG."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-prepped.png"
OUT = ROOT / "dheeraj-ascii.svg"
STATIC = os.environ.get("STATIC") == "1"

RAMP = " .:-=+*#%@"
BG = "#0d1117"
BORDER = "#21262d"
INK = "#c9d1d9"
CURSOR = "#39d353"
MUTED = "#7d8590"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

WIDTH = 390
HEIGHT = 420
PAD = 18
TITLEBAR_H = 34
DEFAULT_COLS = 56
DEFAULT_ROWS = 35
LINE_H = 10.0


def to_glyph_grid(cols: int, rows: int) -> list[str]:
    if not SRC.exists():
        raise SystemExit("source-prepped.png is missing; run prep_photo.py first")
    image = Image.open(SRC).convert("L").resize((cols, rows), Image.LANCZOS)
    px = np.asarray(image, dtype=np.float32)
    indices = np.clip(np.rint(px / 255.0 * (len(RAMP) - 1)), 0, len(RAMP) - 1).astype(int)
    return ["".join(RAMP[index] for index in row) for row in indices]


def build(lines: list[str], cols: int, stagger: float, row_dur: float) -> str:
    art_w = WIDTH - (PAD * 2)
    rows = len(lines)
    art_h = rows * LINE_H
    char_w = art_w / cols
    top = TITLEBAR_H + 16

    out: list[str] = []
    add = out.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="ASCII portrait">'
    )

    if STATIC:
        styles = ".wipe{transform:scaleX(1)}.cur{opacity:0}"
    else:
        steps = f"steps({cols},end)"
        styles = (
            "@keyframes wipe{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
            + f"@keyframes ride{{from{{transform:translateX(0)}}to{{transform:translateX({art_w:.1f}px)}}}}"
            + "@keyframes blinkout{0%,92%{opacity:1}100%{opacity:0}}"
            + ".wipe{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);"
            + "animation:wipe var(--d) "
            + steps
            + " forwards}"
            + ".cur{transform-box:fill-box;transform-origin:left center;opacity:0;"
            + "animation:ride var(--d) "
            + steps
            + " forwards,blinkout var(--d) linear forwards}"
        )
    add(
        "<style>"
        f".art{{font-family:{MONO};font-size:{LINE_H}px;fill:{INK};white-space:pre;dominant-baseline:hanging}}"
        f"{styles}</style>"
    )

    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )
    add(f'<line x1="0" y1="{TITLEBAR_H}" x2="{WIDTH}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>')
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        add(f'<circle cx="{22 + i * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')
    add(
        f'<text x="82" y="{TITLEBAR_H / 2 + 4}" font-family="{MONO}" '
        f'font-size="12" fill="{MUTED}">whoami --portrait</text>'
    )

    add("<defs>")
    for row in range(rows):
        y = top + row * LINE_H
        delay = row * stagger
        style = "" if STATIC else f' style="--d:{row_dur}s;animation-delay:{delay:.3f}s"'
        add(
            f'<clipPath id="w{row}"><rect class="wipe" x="{PAD}" y="{y:.2f}" '
            f'width="{art_w:.2f}" height="{LINE_H:.2f}"{style}/></clipPath>'
        )
    add("</defs>")

    for row, line in enumerate(lines):
        y = top + row * LINE_H
        add(
            f'<text class="art" x="{PAD}" y="{y:.2f}" clip-path="url(#w{row})" '
            f'textLength="{art_w:.2f}" lengthAdjust="spacingAndGlyphs" xml:space="preserve">{escape(line)}</text>'
        )

    for row in range(rows):
        y = top + row * LINE_H
        delay = row * stagger
        style = "" if STATIC else f' style="--d:{row_dur}s;animation-delay:{delay:.3f}s"'
        add(
            f'<rect class="cur" x="{PAD}" y="{y:.2f}" width="{char_w:.2f}" height="{LINE_H:.2f}" '
            f'fill="{CURSOR}"{style}/>'
        )

    add("</svg>")
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cols", type=int, default=DEFAULT_COLS)
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--stagger", type=float, default=0.04)
    parser.add_argument("--row-dur", type=float, default=0.45)
    args = parser.parse_args()

    if not SRC.exists():
        raise SystemExit("source-prepped.png is missing; run prep_photo.py first")

    lines = to_glyph_grid(args.cols, args.rows)
    OUT.write_text(build(lines, args.cols, args.stagger, args.row_dur) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
