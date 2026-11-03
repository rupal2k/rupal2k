#!/usr/bin/env python3
"""headline.py - Omarchy-style headline on one line: thick stroke letters filled with
hard-stop colour bands that scroll continuously. Stdlib only.
Writes assets/hero-{theme}.svg."""

from __future__ import annotations

import html
import xml.etree.ElementTree as ET
from pathlib import Path

TEXT = "RUPAL DAS: CLIENT SUCCESS & TECHNICAL OPERATIONS"

BANDS = {  # top to bottom, (end offset %, colour)
    "dark": [(26.316, "#ECFCCB"), (36.842, "#D9F99D"), (57.895, "#A3E635"), (73.684, "#84CC16"), (100, "#4D7C0F")],
    "light": [(26.316, "#1A2E05"), (36.842, "#365314"), (57.895, "#3F6212"), (73.684, "#4D7C0F"), (100, "#65A30D")],
}

# stroke font: glyph box 4 wide x 6 tall (y down), polylines in grid units
GLYPHS = {
    "A": [[(0, 6), (0, 1), (1, 0), (3, 0), (4, 1), (4, 6)], [(0, 3.5), (4, 3.5)]],
    "C": [[(4, 0), (1, 0), (0, 1), (0, 5), (1, 6), (4, 6)]],
    "D": [[(0, 6), (0, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1.2, 6)]],
    "E": [[(4, 0), (0, 0), (0, 6), (4, 6)], [(0, 3), (3, 3)]],
    "G": [[(4, 0), (1, 0), (0, 1), (0, 5), (1, 6), (4, 6), (4, 3.2), (2, 3.2)]],
    "H": [[(0, 0), (0, 6)], [(4, 0), (4, 6)], [(0, 3), (4, 3)]],
    "I": [[(0.5, 0), (0.5, 6)]],
    "L": [[(0, 0), (0, 6), (4, 6)]],
    "N": [[(0, 6), (0, 0), (4, 6), (4, 0)]],
    "O": [[(1, 0), (3, 0), (4, 1), (4, 5), (3, 6), (1, 6), (0, 5), (0, 1), (1, 0)]],
    "P": [[(0, 6), (0, 0), (4, 0), (4, 3), (1, 3)]],
    "R": [[(0, 6), (0, 0), (4, 0), (4, 3), (1, 3)], [(2, 3), (4, 5), (4, 6)]],
    "S": [[(4, 0), (1, 0), (0, 1), (0, 3), (4, 3), (4, 5), (3, 6), (0, 6)]],
    "T": [[(0, 0), (4, 0)], [(2, 0), (2, 6)]],
    "U": [[(0, 0), (0, 5), (1, 6), (3, 6), (4, 5), (4, 0)]],
    "&": [[(4, 6), (1, 3), (1, 1), (2, 0), (3, 1), (0, 4), (0, 5), (1, 6), (2.5, 6), (4, 4)]],
    "-": [[(0.5, 3), (3.5, 3)]],
    ":": [[(0.5, 1.6), (0.5, 2.6)], [(0.5, 4.6), (0.5, 5.6)]],
    ",": [[(0.5, 4.8), (0.5, 6), (0, 7)]],
    " ": [],
}
NARROW = {"I": 1.0, ":": 1.0, ",": 1.0, " ": 1.5}  # glyph advance width before the gap; default 4
GAP, STROKE = 1.6, 0.9  # grid units
W, PAD = 1600, 12  # px; the line is scaled to fill W minus padding
BAND_SCROLL = 6.0  # seconds for the bands to scroll one letter height


def headline(theme: str) -> str:
    assert all(c in GLYPHS for c in TEXT), "missing glyph"
    units = sum(NARROW.get(c, 4) + GAP for c in TEXT) - GAP
    scale = (W - 2 * PAD) / (units + STROKE)  # + STROKE: half a stroke overhangs at each end
    top = PAD + STROKE * scale / 2
    h = round(top + 7 * scale + STROKE * scale / 2 + PAD)  # 7 units: comma tail drops below the baseline
    x0 = (W - units * scale) / 2
    d, x = [], 0.0
    for c in TEXT:
        for pts in GLYPHS[c]:
            d.append("M" + "L".join(f"{x0 + (x + px) * scale:.1f} {top + py * scale:.1f}" for px, py in pts))
        x += NARROW.get(c, 4) + GAP
    stops, prev = [], 0.0
    for end, colour in BANDS[theme]:
        stops += [f'<stop offset="{prev}%" stop-color="{colour}"/>', f'<stop offset="{end}%" stop-color="{colour}"/>']
        prev = end
    y1 = top + 6 * scale
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
        f'role="img" aria-label="{html.escape(TEXT)}"><defs>'
        f'<linearGradient id="b" gradientUnits="userSpaceOnUse" spreadMethod="repeat" '
        f'x1="0" y1="{top:.1f}" x2="0" y2="{y1:.1f}">{"".join(stops)}'
        f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="0 {y1 - top:.1f}" '
        f'dur="{BAND_SCROLL}s" repeatCount="indefinite"/></linearGradient></defs>'
        f'<path fill="none" stroke="url(#b)" stroke-width="{STROKE * scale:.1f}" stroke-linejoin="miter" '
        f'stroke-miterlimit="2" d="{"".join(d)}"/></svg>\n'
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    for theme in BANDS:
        text = headline(theme)
        ET.fromstring(text)  # self-check: well-formed XML
        (out / f"hero-{theme}.svg").write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote assets/hero-{theme}.svg ({len(text) // 1024} KB)")
