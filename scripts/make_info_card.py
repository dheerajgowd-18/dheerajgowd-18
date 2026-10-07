#!/usr/bin/env python3
"""Generate the animated terminal-style AI profile card."""

from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

BG = "#0d1117"
BORDER = "#21262d"
FG = "#c9d1d9"
MUTED = "#7d8590"
KEY = "#39d353"
ACCENT = "#58a6ff"
RULE = "#30363d"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"

USER = "dheeraj"
HOST = "github"

ROWS: list[tuple[str | None, str]] = [
    ("Name", "Dheeraj Gowd"),
    ("Role", "AI / GenAI Engineer"),
    ("Focus", "LLM apps · RAG · Agentic AI"),
    ("--", ""),
    ("Now", "Enterprise Agentic RAG"),
    ("", "Verified Research Agent"),
    ("", "NEXORA 2026"),
    ("--", ""),
    ("Stack", "Python · FastAPI · LangChain"),
    ("", "LangGraph · Embeddings · Vector Search"),
    ("", "Qdrant · ChromaDB · GitHub Actions"),
    ("--", ""),
    ("Build", "Retrieval pipelines · tool calling"),
    ("", "evaluation · guardrails · automation"),
    ("--", ""),
    ("Links", "github.com/dheerajgowd-18"),
    ("", "agentic-rag · lpdg-nexora-2026"),
]

SWATCHES = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0", "#58a6ff", "#c9d1d9"]
WIDTH = 560
PAD = 22
TITLEBAR_H = 34
LINE_H = 17
KEY_W = 86


def build() -> str:
    parts: list[str] = []
    add = parts.append

    y = TITLEBAR_H + 30
    prompt_y = y
    y += LINE_H + 8
    heights: list[int] = []
    for key, _ in ROWS:
        heights.append(y)
        y += 9 if key == "--" else LINE_H

    swatch_y = y + 10
    height = swatch_y + 14 + PAD

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="AI engineer profile card">'
    )

    if STATIC:
        anim = ".row{opacity:1}"
    else:
        anim = (
            "@keyframes slidein{from{opacity:0;transform:translateX(-9px)}"
            "to{opacity:1;transform:translateX(0)}}"
            ".row{opacity:0;animation:slidein .42s ease-out forwards}"
        )
    add(f"<style>.mono{{font-family:{MONO};}}{anim}</style>")

    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="10" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )
    add(f'<line x1="0" y1="{TITLEBAR_H}" x2="{WIDTH}" y2="{TITLEBAR_H}" stroke="{BORDER}"/>')
    for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        add(f'<circle cx="{22 + i * 18}" cy="{TITLEBAR_H / 2}" r="5.5" fill="{dot}"/>')
    add(
        f'<text class="mono" x="82" y="{TITLEBAR_H / 2 + 4}" font-size="12" fill="{MUTED}">neofetch</text>'
    )

    def delay(index: float) -> str:
        return "" if STATIC else f' style="animation-delay:{0.15 + index * 0.055:.3f}s"'

    add(
        f'<text class="mono row" x="{PAD}" y="{prompt_y}" font-size="13.5"{delay(0)}>'
        f'<tspan fill="{KEY}" font-weight="600">{escape(USER)}</tspan>'
        f'<tspan fill="{MUTED}">@</tspan>'
        f'<tspan fill="{ACCENT}" font-weight="600">{escape(HOST)}</tspan></text>'
    )
    add(
        f'<line class="row" x1="{PAD}" y1="{prompt_y + 8}" x2="{WIDTH - PAD}" y2="{prompt_y + 8}" '
        f'stroke="{RULE}"{delay(1)}/>'
    )

    for index, ((key, value), row_y) in enumerate(zip(ROWS, heights), start=2):
        if key == "--":
            add(
                f'<line class="row" x1="{PAD}" y1="{row_y}" x2="{WIDTH - PAD}" y2="{row_y}" '
                f'stroke="{RULE}"{delay(index)}/>'
            )
            continue

        add(f'<g class="row"{delay(index)}>')
        if key:
            add(
                f'<text class="mono" x="{PAD}" y="{row_y}" font-size="12" fill="{KEY}" '
                f'font-weight="600">{escape(key)}</text>'
            )
            add(
                f'<text class="mono" x="{PAD + KEY_W - 15}" y="{row_y}" font-size="12" fill="{MUTED}">:</text>'
            )
        add(
            f'<text class="mono" x="{PAD + KEY_W}" y="{row_y}" font-size="12" '
            f'fill="{FG if key else MUTED}">{escape(value)}</text>'
        )
        add("</g>")

    n = len(ROWS) + 2
    for index, colour in enumerate(SWATCHES):
        add(
            f'<rect class="row" x="{PAD + index * 20}" y="{swatch_y}" width="16" height="10" rx="2" '
            f'fill="{colour}"{delay(n + index * 0.4)}/>'
        )

    add("</svg>")
    return "".join(parts)


def main() -> None:
    OUT.write_text(build() + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
