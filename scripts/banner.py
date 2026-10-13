#!/usr/bin/env python3
"""
banner.py - generate animated terminal profile banner SVG for dark and light modes.
Stdlib only. Inspired by emmi-lili/emmi-lili.
"""

from __future__ import annotations

import html
import math
from pathlib import Path

W, H = 1180, 610

ROWS = [
    ("Subject", "Rupal Das"),
    ("Role", "Client Success & Technical Operations Lead"),
    ("Company", "Vantage Circle"),
    ("Origin", "Kolkata, India"),
    ("Education", "IIM Lucknow (Executive AI) · WBUT"),
    ("Status", "Building + Scaling + Deploying"),
    ("ToolChain", "Docker · Jenkins · Postman · Linux"),
    ("Core.AI", "Agentic AI · XGBoost · Optuna · MLflow"),
    ("Core.Backend", "Python · FastAPI · PostgreSQL"),
    ("Core.Analytics", "SQL Telemetry · Streamlit · SHAP"),
    ("Core.Automate", "REST APIs · Webhooks · Jenkins · Bash"),
    ("Grid.LinkedIn", "/in/rupal-das-03ba082a"),
    ("Grid.Portfolio", "rupalportfolio.vercel.app"),
    ("Grid.GitHub", "rupal2k"),
    ("Grid.Mail", "rupal2k@gmail.com"),
]

THEMES = {
    "dark": {
        "bg": "#0A101F",
        "panel": "#0D1628",
        "panel2": "#101B30",
        "line": "#25344C",
        "muted": "#8291A8",
        "text": "#DDE7F5",
        "accent": "#F15162",
        "chrome": "#F15162",
        "status": "#10B981",
        "shadow": "#000000",
        "radar_fill": "rgba(241, 81, 98, 0.12)",
    },
    "light": {
        "bg": "#F6F8FA",
        "panel": "#FFFFFF",
        "panel2": "#F3F5F8",
        "line": "#D0D7DE",
        "muted": "#57606A",
        "text": "#1F2328",
        "accent": "#D83A52",
        "chrome": "#D83A52",
        "status": "#1A7F37",
        "shadow": "#D0D7DE",
        "radar_fill": "rgba(216, 58, 82, 0.08)",
    },
}


def dotted_leader(x0: float, x1: float, y: float, step: float = 5.0) -> str:
    if x1 <= x0:
        return ""
    dots = []
    x = x0
    while x <= x1:
        dots.append(f"M{x:.2f} {y:.0f}h1")
        x += step
    return "".join(dots)


def text_width(s: str, font_size: float = 14) -> float:
    # Monospace advance is ~0.60 * font_size
    return len(s) * font_size * 0.60


def render_banner(theme_name: str) -> str:
    t = THEMES[theme_name]
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">Rupal Das - Live System Profile</title>',
        f'<desc id="desc">Terminal telemetry profile dashboard for Rupal Das.</desc>',
        '<defs>',
        f'<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">',
        f'<feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="{t["shadow"]}" flood-opacity=".28"/>',
        '</filter>',
        f'<filter id="glow" x="-100%" y="-100%" width="300%" height="300%">',
        f'<feGaussianBlur stdDeviation="3" result="b"/><feFlood flood-color="{t["chrome"]}" flood-opacity=".45"/><feComposite in2="b" operator="in"/>',
        '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>',
        '</filter>',
        '<clipPath id="radarClip"><rect x="49" y="124" width="390" height="414" rx="4"/></clipPath>',
        '</defs>',
        # Main background & Window Frame
        f'<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>',
        f'<rect x="13" y="13" width="1154" height="584" rx="13" fill="{t["panel"]}" stroke="{t["line"]}" filter="url(#shadow)"/>',
        f'<path d="M13 62H1167" stroke="{t["line"]}"/>',
        # Traffic Lights
        '<circle cx="38" cy="38" r="6" fill="#FF5F57"/>',
        '<circle cx="59" cy="38" r="6" fill="#FEBC2E"/>',
        '<circle cx="80" cy="38" r="6" fill="#28C840"/>',
        # Terminal Title
        f'<text x="590" y="43" text-anchor="middle" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" letter-spacing=".4">rupal.sh --live</text>',
        
        # LEFT PANEL: TELEMETRY / RADAR
        f'<rect x="35" y="88" width="418" height="472" rx="6" fill="{t["panel2"]}" stroke="{t["line"]}"/>',
        f'<path d="M35 124H453" stroke="{t["line"]}"/>',
        f'<text x="49" y="111" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" letter-spacing="1.2">SYS.TELEMETRY</text>',
        f'<text x="438" y="111" text-anchor="end" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">NODE: IND-CCU</text>',
        # Radar Crosshairs Corners
        f'<path d="M49 141h12M49 141v12M439 141h-12M439 141v12M49 539h12M49 539v-12M439 539h-12M439 539v-12" fill="none" stroke="{t["chrome"]}" opacity=".55"/>',
        
        # Inside Left Visual
        '<g clip-path="url(#radarClip)">',
        # Radar circles
        f'<circle cx="244" cy="270" r="110" fill="none" stroke="{t["line"]}" stroke-dasharray="4,4"/>',
        f'<circle cx="244" cy="270" r="80" fill="none" stroke="{t["line"]}"/>',
        f'<circle cx="244" cy="270" r="50" fill="none" stroke="{t["line"]}" stroke-dasharray="3,3"/>',
        f'<circle cx="244" cy="270" r="20" fill="none" stroke="{t["line"]}"/>',
        f'<line x1="120" y1="270" x2="368" y2="270" stroke="{t["line"]}" stroke-width="1"/>',
        f'<line x1="244" y1="146" x2="244" y2="394" stroke="{t["line"]}" stroke-width="1"/>',
        # Radar Sweep Animation
        '<g>',
        f'<path d="M244 270 L344 200 A110 110 0 0 0 244 160 Z" fill="{t["radar_fill"]}"/>',
        f'<line x1="244" y1="270" x2="344" y2="200" stroke="{t["chrome"]}" stroke-width="1.8"/>',
        '<animateTransform attributeName="transform" type="rotate" from="0 244 270" to="360 244 270" dur="4s" repeatCount="indefinite"/>',
        '</g>',
        # Targets on radar
        f'<circle cx="290" cy="220" r="3.5" fill="{t["accent"]}"><animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>',
        f'<circle cx="190" cy="310" r="3" fill="{t["chrome"]}"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.5s" repeatCount="indefinite"/></circle>',
        f'<circle cx="270" cy="330" r="3" fill="{t["status"]}"><animate attributeName="opacity" values="0.8;0.2;0.8" dur="1.8s" repeatCount="indefinite"/></circle>',
        '</g>',
        
        # Telemetry metrics under radar
        f'<text x="58" y="420" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">STREAM: /telemetry/enterprise</text>',
        f'<text x="58" y="440" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">SLA COMPLIANCE: 99.8%  [+20% UPLIFT]</text>',
        f'<text x="58" y="460" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">GO-LIVE DELIVERIES: 15+ [0 MISSED]</text>',
        f'<text x="58" y="480" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">AI L&amp;D REDUCTION: ~40% CYCLE TIME</text>',
        f'<text x="58" y="500" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">AGENT STATUS: DISPATCHED &amp; ACTIVE</text>',
        f'<text x="58" y="520" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">COORDINATES: 22.5726° N, 88.3639° E</text>',
        f'<text x="58" y="551" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10">SYS-VER 2.4.0 · ENTERPRISE KERNEL</text>',

        # RIGHT PANEL: SYSTEM.INFO
        f'<rect x="474" y="88" width="672" height="472" rx="6" fill="{t["panel2"]}" stroke="{t["line"]}"/>',
        f'<path d="M474 124H1146" stroke="{t["line"]}"/>',
        f'<text x="490" y="111" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" letter-spacing="1.2">SYSTEM.INFO</text>',
        # LIVE pulse & @rupal2k pill
        '<g filter="url(#glow)"><circle cx="915" cy="106" r="4" fill="#FF4D5A"><animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></circle></g>',
        '<text x="927" y="111" fill="#FF4D5A" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700">LIVE</text>',
        f'<rect x="982" y="94" width="146" height="24" rx="12" fill="{t["chrome"]}" opacity=".16" stroke="{t["chrome"]}"/>',
        f'<text x="1055" y="111" text-anchor="middle" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" font-weight="700">@rupal2k</text>',
    ]

    value_right = 1127.0
    row_y = 153.0
    for label, value in ROWS:
        value_len = text_width(value, 14)
        label_len = text_width(label, 14)
        leader_start = 491 + label_len + 12
        leader_end = value_right - value_len - 12
        leader_d = dotted_leader(leader_start, leader_end, row_y - 4)
        parts.extend([
            f'<text x="491" y="{row_y:.0f}" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14">{html.escape(label)}</text>',
            f'<path d="{leader_d}" fill="none" stroke="{t["line"]}" stroke-width="1" shape-rendering="crispEdges"/>',
            f'<text x="{value_right:.0f}" y="{row_y:.0f}" text-anchor="end" fill="{t["text"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" textLength="{value_len:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(value)}</text>',
        ])
        row_y += 24.5

    parts.extend([
        f'<path d="M490 530H1130" stroke="{t["line"]}"/>',
        f'<text x="491" y="548" fill="{t["status"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">● ALL SYSTEMS NOMINAL</text>',
        f'<text x="1128" y="548" text-anchor="end" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">UTC+5:30 · INDIA NODE</text>',
        '</svg>',
    ])
    return "".join(parts)


def main():
    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        dest = out_dir / f"banner-{theme}.svg"
        dest.write_text(render_banner(theme), encoding="utf-8")
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
