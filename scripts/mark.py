#!/usr/bin/env python3
"""mark.py - Omarchy-style stroke animations: the "RD" monogram and the headline.
Thick strokes draw one after another over hard-stop colour bands, hold, then erase.
Stdlib only. Writes assets/mark-{theme}.svg and assets/headline-{theme}.svg."""

from __future__ import annotations

import html
import xml.etree.ElementTree as ET
from pathlib import Path

BANDS = {  # top to bottom, (end offset %, colour)
    "dark": [(26.316, "#ECFCCB"), (36.842, "#D9F99D"), (57.895, "#A3E635"), (73.684, "#84CC16"), (100, "#4D7C0F")],
    "light": [(26.316, "#1A2E05"), (36.842, "#365314"), (57.895, "#3F6212"), (73.684, "#4D7C0F"), (100, "#65A30D")],
}
EASE_IN = "cubic-bezier(.45,0,.25,1)"
EASE_OUT = "cubic-bezier(.55,0,.75,.2)"

# ---- monogram: (d, start s, duration s, direction) on a 1200 grid; -1 draws backward
MARK = [
    ("M120 1160V40H440V560H200", 0.00, 0.60, 1),            # R stem + bowl
    ("M280 560L440 720V1160", 0.55, 0.25, 1),               # R leg, 45° like the D corners
    ("M680 1160V40H1000L1120 160V1040L1000 1160H780", 0.70, 0.75, 1),  # D outline, gap at foot
    ("M920 360V840", 1.40, 0.12, -1),                       # D inner tick
    ("M40 1160H120", 1.55, 0.08, -1),                       # R serif
]

# ---- stroke font: glyph box 4 wide x 6 tall (y down), polylines in grid units
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
# (text, scale px per unit, baseline-top y px); scale chosen so each line fits 1200 px
LINES = [("RUPAL DAS:", 13.0, 20), ("HANDS-ON, TECHNICAL", 8.6, 150), ("& AGENTIC CLIENT SUCCESS", 8.6, 240)]
HEAD_W, HEAD_H = 1200, 310
LETTER_STEP, LETTER_DUR = 0.075, 0.42  # stagger between letters, draw time per letter
HEAD_CYCLE, HEAD_HOLD, HEAD_ERASE = 11.0, 8.6, 9.6
BAND_SCROLL = 6.0  # seconds for the bands to scroll one line height


def keyframes(name: str, start: float, dur: float, direction: int, cycle: float, hold: float, erase: float) -> str:
    assert start + dur <= hold, f"{name} still drawing after the hold starts"
    pct = lambda t: f"{t / cycle * 100:.3f}%"  # noqa: E731
    return (
        f"@keyframes {name}{{0%,{pct(start)}{{stroke-dashoffset:{direction}px;animation-timing-function:{EASE_IN}}}"
        f"{pct(start + dur)},{pct(hold)}{{stroke-dashoffset:0;animation-timing-function:{EASE_OUT}}}"
        f"{pct(erase)},100%{{stroke-dashoffset:{-direction}px}}}}.{name}{{animation:{name} {cycle}s infinite}}"
    )


def bands(theme: str, gid: str, y0: float, y1: float, scroll: bool) -> str:
    stops, prev = [], 0.0
    for end, colour in BANDS[theme]:
        stops += [f'<stop offset="{prev}%" stop-color="{colour}"/>', f'<stop offset="{end}%" stop-color="{colour}"/>']
        prev = end
    anim = (
        f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="0 {y1 - y0:.1f}" '
        f'dur="{BAND_SCROLL}s" repeatCount="indefinite"/>' if scroll else ""
    )
    return (
        f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" spreadMethod="repeat" '
        f'x1="0" y1="{y0:.1f}" x2="0" y2="{y1:.1f}">{"".join(stops)}{anim}</linearGradient>'
    )


def wrap(w: int, h: int, label: str, defs: str, css: list[str], body: str, stroke: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="none" '
        f'stroke-linejoin="miter" stroke-miterlimit="2" role="img" aria-label="{label}"{stroke}><defs>{defs}</defs>'
        f'<style>path{{stroke-dasharray:1px}}{"".join(css)}'
        "@media (prefers-reduced-motion:reduce){path{animation:none!important;stroke-dashoffset:0}}</style>"
        f"{body}</svg>\n"
    )


def mark(theme: str) -> str:
    css = [keyframes(f"p{i}", s, d, dr, 7.0, 5.4, 6.2) for i, (_, s, d, dr) in enumerate(MARK)]
    body = "".join(f'<path class="p{i}" pathLength="1" d="{d}"/>' for i, (d, *_) in enumerate(MARK))
    return wrap(1200, 1200, "RD monogram", bands(theme, "bands", 0, 1200, False), css, body,
                ' stroke="url(#bands)" stroke-width="80"')


def headline(theme: str) -> str:
    defs, css, groups, n, letter = [], [], [], 0, 0
    for li, (text, scale, top) in enumerate(LINES):
        assert all(c in GLYPHS for c in text), f"missing glyph in {text!r}"
        width = sum(NARROW.get(c, 4) + GAP for c in text) - GAP
        x0 = (HEAD_W - width * scale) / 2
        assert x0 >= 0, f"line {li} too wide"
        defs.append(bands(theme, f"b{li}", top, top + 6 * scale, True))
        paths, x = [], 0.0
        for c in text:
            strokes = GLYPHS[c]
            for si, pts in enumerate(strokes):
                d = "M" + "L".join(f"{x0 + (x + px) * scale:.1f} {top + py * scale:.1f}" for px, py in pts)
                start = letter * LETTER_STEP + si * LETTER_DUR / len(strokes)
                css.append(keyframes(f"s{n}", start, LETTER_DUR / len(strokes), 1, HEAD_CYCLE, HEAD_HOLD, HEAD_ERASE))
                paths.append(f'<path class="s{n}" pathLength="1" d="{d}"/>')
                n += 1
            if c != " ":
                letter += 1
            x += NARROW.get(c, 4) + GAP
        groups.append(f'<g stroke="url(#b{li})" stroke-width="{STROKE * scale:.1f}">{"".join(paths)}</g>')
    label = html.escape(" ".join(t for t, *_ in LINES))
    return wrap(HEAD_W, HEAD_H, label, "".join(defs), css, "".join(groups), "")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    for theme in BANDS:
        for name, fn in (("mark", mark), ("headline", headline)):
            text = fn(theme)
            ET.fromstring(text)  # self-check: well-formed XML
            (out / f"{name}-{theme}.svg").write_text(text, encoding="utf-8", newline="\n")
            print(f"wrote assets/{name}-{theme}.svg ({len(text) // 1024} KB)")
