#!/usr/bin/env python3
"""mark.py - animated "RD" monogram: thick strokes drawn one after another
over hard-stop colour bands, then held and erased on a loop. Stdlib only."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

CYCLE = 7.0  # seconds per loop
HOLD_END, ERASE_END = 5.4, 6.2  # all strokes hold until HOLD_END, erased by ERASE_END

# (d, start s, duration s, direction) on a 1200 grid, stroke 80; +1 draws forward, -1 backward
PATHS = [
    ("M120 1160V40H440V560H200", 0.00, 0.60, 1),           # R stem + bowl
    ("M280 560L440 720V1160", 0.55, 0.25, 1),              # R leg, 45° like the D corners
    ("M680 1160V40H1000L1120 160V1040L1000 1160H780", 0.70, 0.75, 1),  # D outline, gap at foot
    ("M920 360V840", 1.40, 0.12, -1),                      # D inner tick
    ("M40 1160H120", 1.55, 0.08, -1),                      # R serif
]

BANDS = {  # top to bottom, (end offset %, colour)
    "dark": [(26.316, "#ECFCCB"), (36.842, "#D9F99D"), (57.895, "#A3E635"), (73.684, "#84CC16"), (100, "#4D7C0F")],
    "light": [(26.316, "#1A2E05"), (36.842, "#365314"), (57.895, "#3F6212"), (73.684, "#4D7C0F"), (100, "#65A30D")],
}


def pct(t: float) -> str:
    return f"{t / CYCLE * 100:.3f}%"


def svg(theme: str) -> str:
    stops, prev = [], 0.0
    for end, colour in BANDS[theme]:
        stops += [f'<stop offset="{prev}%" stop-color="{colour}"/>', f'<stop offset="{end}%" stop-color="{colour}"/>']
        prev = end
    css, paths = [], []
    for i, (d, start, dur, direction) in enumerate(PATHS):
        assert start + dur <= HOLD_END, f"path {i} still drawing after hold starts"
        css.append(
            f"@keyframes p{i}{{0%,{pct(start)}{{stroke-dashoffset:{direction}px;animation-timing-function:cubic-bezier(.45,0,.25,1)}}"
            f"{pct(start + dur)},{pct(HOLD_END)}{{stroke-dashoffset:0;animation-timing-function:cubic-bezier(.55,0,.75,.2)}}"
            f"{pct(ERASE_END)},100%{{stroke-dashoffset:{-direction}px}}}}"
            f".p{i}{{animation:p{i} {CYCLE}s infinite}}"
        )
        paths.append(f'<path class="p{i}" pathLength="1" d="{d}"/>')
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="1200" height="1200" '
        'fill="none" stroke="url(#bands)" stroke-width="80" role="img" aria-label="RD monogram">'
        f'<defs><linearGradient id="bands" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="1200">{"".join(stops)}</linearGradient></defs>'
        f'<style>path{{stroke-dasharray:1px}}{"".join(css)}'
        "@media (prefers-reduced-motion:reduce){path{animation:none!important;stroke-dashoffset:0}}</style>"
        f'{"".join(paths)}</svg>\n'
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    for theme in BANDS:
        text = svg(theme)
        ET.fromstring(text)  # self-check: well-formed XML
        (out / f"mark-{theme}.svg").write_text(text, encoding="utf-8")
        print(f"wrote assets/mark-{theme}.svg")
