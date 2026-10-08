#!/usr/bin/env python3
"""Generate ai-signal.svg — A minimal generative AI flow visualization.

Represents the core autonomous workflow:
Retrieval → Reasoning → Verification → Action.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ai-signal.svg"

WIDTH = 860
HEIGHT = 128
BG = "#080A0D"
BORDER = "#161D27"
ACCENT = "#65D9FF"
MUTED_LINE = "#1A2E3D"
SUBTLE_LINE = "#11202B"
TEXT_PRIMARY = "#F2F4F7"
TEXT_SECONDARY = "#8A949E"
TEXT_MUTED = "#485461"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def build_svg() -> str:
    parts: list[str] = []
    add = parts.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="Generative AI Information Flow: Retrieval, Reasoning, Verification, and Action">'
    )

    # Styles: 1-shot elegant CSS reveal
    add(
        "<style>"
        f".mono{{font-family:{MONO};}}"
        "@keyframes drawLine{from{stroke-dashoffset:1000}to{stroke-dashoffset:0}}"
        "@keyframes fadeIn{from{opacity:0}to{opacity:1}}"
        "@keyframes popNode{from{opacity:0;transform:scale(0.5)}to{opacity:1;transform:scale(1)}}"
        ".flow-primary{stroke-dasharray:1000;stroke-dashoffset:1000;animation:drawLine 1.6s cubic-bezier(.2,.8,.3,1) forwards}"
        ".flow-subtle{opacity:0;animation:fadeIn 1.2s ease-out 0.2s forwards}"
        ".flow-node{opacity:0;transform-origin:center;transform-box:fill-box;animation:popNode .6s ease-out forwards}"
        ".meta-text{opacity:0;animation:fadeIn .9s ease-out .4s forwards}"
        "</style>"
    )

    # Card background and fine structural border
    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="6" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Architectural corner tick markers (+)
    for cx, cy in [(24, 18), (WIDTH - 24, 18), (24, HEIGHT - 18), (WIDTH - 24, HEIGHT - 18)]:
        add(
            f'<path d="M {cx - 3} {cy} L {cx + 3} {cy} M {cx} {cy - 3} L {cx} {cy + 3}" '
            f'stroke="{BORDER}" stroke-width="1"/>'
        )

    # Micro-labels (Header metadata)
    add(
        f'<text class="mono meta-text" x="42" y="21" font-size="9" fill="{TEXT_MUTED}" '
        f'letter-spacing="1">SYS.ID // NEURAL_FLOW.01</text>'
    )
    add(
        f'<text class="mono meta-text" x="{WIDTH - 42}" y="21" font-size="9" fill="{TEXT_MUTED}" '
        f'text-anchor="end" letter-spacing="1">STATUS: VERIFIED // LATENCY: NOMINAL</text>'
    )

    # Subtle horizontal center baseline
    add(
        f'<line x1="45" y1="60" x2="{WIDTH - 45}" y2="60" '
        f'stroke="{SUBTLE_LINE}" stroke-width="1" stroke-dasharray="3 6"/>'
    )

    # Harmonic secondary wave paths (contextual vector field)
    # Upper branch: reasoning exploration
    add(
        f'<path class="flow-subtle" d="M 130 60 C 200 32, 270 32, 340 60 C 410 88, 480 88, 550 60 C 620 32, 680 42, 740 60" '
        f'fill="none" stroke="{SUBTLE_LINE}" stroke-width="1.2"/>'
    )
    # Lower branch: dense retrieval field
    add(
        f'<path class="flow-subtle" d="M 60 74 C 95 74, 110 65, 130 60" '
        f'fill="none" stroke="{MUTED_LINE}" stroke-width="1"/>'
    )
    add(
        f'<path class="flow-subtle" d="M 60 46 C 95 46, 110 55, 130 60" '
        f'fill="none" stroke="{MUTED_LINE}" stroke-width="1"/>'
    )

    # Intermediate feedback loop / verification gate arc
    add(
        f'<path class="flow-subtle" d="M 340 60 C 410 36, 480 36, 550 60 C 480 84, 410 84, 340 60" '
        f'fill="none" stroke="{MUTED_LINE}" stroke-width="1" stroke-dasharray="2 4"/>'
    )

    # PRIMARY ACTIVE SIGNAL (Cyan trajectory)
    add(
        f'<path class="flow-primary" '
        f'd="M 60 60 L 130 60 C 200 52, 270 68, 340 60 C 410 52, 480 52, 550 60 L 740 60 L 800 60" '
        f'fill="none" stroke="{ACCENT}" stroke-width="1.6" stroke-linecap="round"/>'
    )

    # Action terminal arrow tick at x=800
    add(
        f'<path class="meta-text" d="M 795 56 L 800 60 L 795 64" '
        f'fill="none" stroke="{ACCENT}" stroke-width="1.5" stroke-linecap="round"/>'
    )

    # STAGE NODES & LABELS
    stages = [
        (130, "01", "RETRIEVAL", 0.5),
        (340, "02", "REASONING", 0.8),
        (550, "03", "VERIFICATION", 1.1),
        (740, "04", "ACTION", 1.4),
    ]

    for x, num, name, delay in stages:
        # Outer ring
        add(
            f'<circle class="flow-node" cx="{x}" cy="60" r="6" '
            f'fill="none" stroke="{ACCENT}" stroke-width="1" stroke-opacity="0.35" '
            f'style="animation-delay:{delay}s"/>'
        )
        # Inner core
        add(
            f'<circle class="flow-node" cx="{x}" cy="60" r="2.8" '
            f'fill="{ACCENT}" style="animation-delay:{delay}s"/>'
        )
        # Vertical alignment guide tick
        add(
            f'<line class="flow-subtle" x1="{x}" y1="67" x2="{x}" y2="82" '
            f'stroke="{BORDER}" stroke-width="1" stroke-dasharray="2 2"/>'
        )
        # Stage Number
        add(
            f'<text class="mono meta-text" x="{x}" y="94" font-size="8.5" fill="{ACCENT}" '
            f'font-weight="600" text-anchor="middle" letter-spacing="0.5">{num}</text>'
        )
        # Stage Name
        add(
            f'<text class="mono meta-text" x="{x}" y="107" font-size="9" fill="{TEXT_SECONDARY}" '
            f'font-weight="500" text-anchor="middle" letter-spacing="1">{name}</text>'
        )

    add("</svg>")
    return "".join(parts)


def main() -> None:
    OUT.write_text(build_svg() + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
