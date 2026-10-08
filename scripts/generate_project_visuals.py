#!/usr/bin/env python3
"""Generate project-rag-signal.svg and project-agent-signal.svg.

Fine, restrained system-line vector graphics illustrating the core
technical architecture for each featured project.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT_RAG = ROOT / "project-rag-signal.svg"
OUT_AGENT = ROOT / "project-agent-signal.svg"

WIDTH = 860
HEIGHT = 40
BG = "#080A0D"
BORDER = "#161D27"
ACCENT = "#65D9FF"
MUTED_LINE = "#1C2836"
TEXT_SEC = "#8A949E"
TEXT_MUT = "#4D5B6A"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"


def build_rag_svg() -> str:
    parts: list[str] = []
    add = parts.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="Enterprise Agentic RAG System Pipeline Architecture">'
    )
    add(
        f"<style>.mono{{font-family:{MONO};}}"
        "@keyframes drawLine{from{stroke-dashoffset:800}to{stroke-dashoffset:0}}"
        "@keyframes fadeIn{from{opacity:0}to{opacity:1}}"
        ".line-flow{stroke-dasharray:800;stroke-dashoffset:800;animation:drawLine 1.2s cubic-bezier(.2,.8,.3,1) forwards}"
        ".fade{opacity:0;animation:fadeIn 0.8s ease-out 0.2s forwards}"
        "</style>"
    )
    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="6" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Connecting backbone
    add(
        f'<path class="line-flow" d="M 40 20 L 820 20" fill="none" stroke="{MUTED_LINE}" stroke-width="1"/>'
    )
    # Active pipeline segment
    add(
        f'<path class="line-flow" d="M 50 20 L 780 20" fill="none" stroke="{ACCENT}" stroke-width="1.2" stroke-opacity="0.8"/>'
    )

    steps = [
        (90, "01", "INGEST & ROUTE", 0.3),
        (280, "02", "HYBRID RETRIEVAL", 0.5),
        (490, "03", "GUARDRAIL FILTER", 0.7),
        (700, "04", "SYNTHESIS & EVAL", 0.9),
    ]

    for x, num, label, delay in steps:
        add(
            f'<circle class="fade" cx="{x}" cy="20" r="3" fill="{ACCENT}" style="animation-delay:{delay}s"/>'
        )
        add(
            f'<circle class="fade" cx="{x}" cy="20" r="6" fill="none" stroke="{ACCENT}" stroke-width="0.8" stroke-opacity="0.4" style="animation-delay:{delay}s"/>'
        )
        add(
            f'<text class="mono fade" x="{x + 12}" y="24" font-size="9" fill="{TEXT_MUT}" font-weight="600">{num}</text>'
        )
        add(
            f'<text class="mono fade" x="{x + 30}" y="24" font-size="9" fill="{TEXT_SEC}" letter-spacing="0.5">{escape(label)}</text>'
        )

    # Arrowhead at end
    add(
        f'<path class="fade" d="M 816 17 L 821 20 L 816 23" fill="none" stroke="{ACCENT}" stroke-width="1.2" stroke-linecap="round"/>'
    )

    add("</svg>")
    return "".join(parts)


def build_agent_svg() -> str:
    parts: list[str] = []
    add = parts.append

    add(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        f'aria-label="Verified Research Agent Multi-Hop Verification Graph">'
    )
    add(
        f"<style>.mono{{font-family:{MONO};}}"
        "@keyframes drawLine{from{stroke-dashoffset:800}to{stroke-dashoffset:0}}"
        "@keyframes fadeIn{from{opacity:0}to{opacity:1}}"
        ".line-flow{stroke-dasharray:800;stroke-dashoffset:800;animation:drawLine 1.2s cubic-bezier(.2,.8,.3,1) forwards}"
        ".fade{opacity:0;animation:fadeIn 0.8s ease-out 0.2s forwards}"
        "</style>"
    )
    add(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="6" '
        f'fill="{BG}" stroke="{BORDER}" stroke-width="1"/>'
    )

    # Connecting backbone
    add(
        f'<path class="line-flow" d="M 40 20 L 820 20" fill="none" stroke="{MUTED_LINE}" stroke-width="1"/>'
    )
    # Verification loop arc between x=330 and x=560
    add(
        f'<path class="fade" d="M 540 17 C 480 6, 390 6, 340 17" fill="none" stroke="{ACCENT}" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.6"/>'
    )
    # Active pipeline segment
    add(
        f'<path class="line-flow" d="M 50 20 L 780 20" fill="none" stroke="{ACCENT}" stroke-width="1.2" stroke-opacity="0.8"/>'
    )

    steps = [
        (90, "01", "HYPOTHESIS DECOMP", 0.3),
        (300, "02", "EVIDENCE HARVEST", 0.5),
        (510, "03", "CLAIM VERIFY GATE", 0.7),
        (710, "04", "DEFENSIBLE BRIEF", 0.9),
    ]

    for x, num, label, delay in steps:
        add(
            f'<circle class="fade" cx="{x}" cy="20" r="3" fill="{ACCENT}" style="animation-delay:{delay}s"/>'
        )
        add(
            f'<circle class="fade" cx="{x}" cy="20" r="6" fill="none" stroke="{ACCENT}" stroke-width="0.8" stroke-opacity="0.4" style="animation-delay:{delay}s"/>'
        )
        add(
            f'<text class="mono fade" x="{x + 12}" y="24" font-size="9" fill="{TEXT_MUT}" font-weight="600">{num}</text>'
        )
        add(
            f'<text class="mono fade" x="{x + 30}" y="24" font-size="9" fill="{TEXT_SEC}" letter-spacing="0.5">{escape(label)}</text>'
        )

    # Arrowhead at end
    add(
        f'<path class="fade" d="M 816 17 L 821 20 L 816 23" fill="none" stroke="{ACCENT}" stroke-width="1.2" stroke-linecap="round"/>'
    )

    add("</svg>")
    return "".join(parts)


def main() -> None:
    OUT_RAG.write_text(build_rag_svg() + "\n", encoding="utf-8")
    print(f"wrote {OUT_RAG.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")

    OUT_AGENT.write_text(build_agent_svg() + "\n", encoding="utf-8")
    print(f"wrote {OUT_AGENT.relative_to(ROOT)} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
