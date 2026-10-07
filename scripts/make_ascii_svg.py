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

RAMP = " .`:-=+*cs#%@"
BG = "#0d1117"
BORDER = "#21262d"
INK = "#c9d1d9"
CURSOR = "#39d353"
MUTED = "#7d8590"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
FONT_SIZE = 10.0
CHAR_W = FONT_SIZE * 0.6
LINE_H = FONT_SIZE
PAD = 18
CHROME_SCALE = 1.56
TITLEBAR_H = round(34 * CHROME_SCALE)


def to_glyph_grid(cols: int, rows: int) -> list[str]:
    if not SRC.exists():
        raise SystemExit("source-prepped.png is missing; run prep_photo.py first")
    image = Image.open(SRC).convert("L").resize((cols, rows), Image.LANCZOS)
    px = np.asarray(image, dtype=np.float32)
    indices = np.clip(np.rint((255.0 - px) / 255.0 * (len(RAMP) - 1)), 0, len(RAMP) - 1).astype(int)
    return ["".join(RAMP[index] for index in row) for row in indices]


def build(lines: list[str], cols: int, stagger: float, row_dur: float) -> str:
    art_w = cols * CHAR_W
    rows = len(lines)
    art_h = rows * LINE_H
    width = round(art_w + PAD * 2)
    top = TITLEBAR_H + 14
    height = round(top + art_h + PAD)

    out: list[str] = []
    add = out.append
    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="ASCII portrait">'
    )

    if STATIC:
        styles = ".wipe{transform:scaleX(1)}.cur{opacity:0}"
    else:
        steps = f"steps({cols},end)"
        styles = (
            "@keyframes wipe{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
            + "@keyframes ride{{from{{transform:translateX(0)}}to{{transform:translateX({}px)}}}}".format(f"{art_w:.1f}")
            + "@keyframes blinkout{0%,92%{opacity:1}100%{opacity:0}}"
            + ".wipe{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);"
            + "animation:wipe var(--d) " + steps + " forwards}"
            + ".cur{transform-box:fill-box;transform-origin:left center;opacity:0;"
            + "animation:ride var(--d) " + steps + " forwards,blinkout var(--d) linear forwards}"
        )
    add(
        "<style>"
        f".art{{font-family:{MONO};font-size:{FONT_SIZE}px;fill:{INK};white-space:pre;dominant-baseline:hanging}}"
        f"{styles}</style>"
    )

    add(
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )
    add(f'<line x1="0" y1="{TITLEBAR_H}" x2="{width}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>')
    scale = CHROME_SCALE
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        add(
            f'<circle cx="{(22 + i * 18) * scale:.1f}" cy="{TITLEBAR_H / 2}" '
            f'r="{5.5 * scale:.1f}" fill="{dot}"/>'
        )
    add(
        f'<text x="{82 * scale:.1f}" y="{TITLEBAR_H / 2 + 4 * scale:.1f}" font-family="{MONO}" '
        f'font-size="{12 * scale:.1f}" fill="{MUTED}">./portrait.sh</text>'
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
            f'<rect class="cur" x="{PAD}" y="{y:.2f}" width="{CHAR_W:.2f}" height="{LINE_H:.2f}" '
            f'fill="{CURSOR}"{style}/>'
        )

    add("</svg>")
    return "".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cols", type=int, default=92)
    parser.add_argument("--rows", type=int, default=0)
    parser.add_argument("--stagger", type=float, default=0.045)
    parser.add_argument("--row-dur", type=float, default=0.5)
    args = parser.parse_args()

    if not SRC.exists():
        raise SystemExit("source-prepped.png is missing; run prep_photo.py first")

    rows = args.rows
    if rows <= 0:
        w, h = Image.open(SRC).size
        rows = max(1, int(round(args.cols * (h / w) * (CHAR_W / LINE_H))))

    lines = to_glyph_grid(args.cols, rows)
    OUT.write_text(build(lines, args.cols, args.stagger, args.row_dur) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
