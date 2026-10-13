#!/usr/bin/env python3
"""
banner.py - generate animated terminal profile banner SVG for dark and light modes.
Stdlib only.
Features an authentic live terminal computer boot sequence animation on the left panel
and a stable, glowing live system spec sheet on the right panel.
"""

from __future__ import annotations

import html
from pathlib import Path

W, H = 1180, 610
BOOT_DUR = 16.0  # seconds per loop

ROWS = [
    ("Subject", "Rupal Das"),
    ("Role", "Client Success & Technical Operations Lead"),
    ("Company", "Vantage Circle"),
    ("Origin", "Kolkata, India"),
    ("Education", "IIM Lucknow (Executive) · WBUT"),
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

BOOT_LOGS = [
    (0.2, "dim", "> BOOT ROM v4.18 (x86_64 UEFI) ... OK"),
    (0.5, "dim", "> MEMORY: 64 GB ECC DDR5 ... VERIFIED"),
    (0.8, "text", "> KERNEL: Linux 6.8.0-telemetry-x86_64"),
    (1.1, "dim", "> NVMe ROOT FS [/dev/nvme0n1p2] ... MOUNTED"),
    (1.5, "cyan", "> INITIALIZING SYSTEM DAEMONS:"),
    (1.9, "ok", "systemd-networkd.service (dual-stack)"),
    (2.3, "ok", "pinet-edge-telemetry.service"),
    (2.7, "ok", "aegis-ml-pipeline.service [FastAPI]"),
    (3.1, "ok", "postgresql-cluster.service [pg16]"),
    (3.5, "ok", "jenkins-webhook-agent.service"),
    (3.9, "ok", "rest-api-gateway.service (:443 TLS)"),
    (4.4, "dim", "> NODE: IND-CCU [22.57°N, 88.36°E]"),
    (4.9, "cyan", "> RUNLEVEL: 5 · MULTI-USER TARGET READY"),
    (5.4, "prompt", "rupal2k@enterprise:~$ ./init_ops.sh"),
    (6.0, "accent", "↳ SLA ENFORCEMENT: 99.8% [ACTIVE]"),
    (6.5, "accent", "↳ P1/P2 ESCALATION MONITOR: ONLINE"),
    (7.0, "online", "● ALL SYSTEMS NOMINAL · RUNNING"),
]

THEMES = {
    "dark": {
        "bg": "#0A101F",
        "panel": "#0D1628",
        "panel2": "#101B30",
        "line": "#25344C",
        "muted": "#8291A8",
        "text": "#DDE7F5",
        "accent": "#A3E635",
        "chrome": "#A3E635",
        "status": "#A3E635",
        "cyan": "#38BDF8",
        "shadow": "#000000",
    },
    "light": {
        "bg": "#F6F8FA",
        "panel": "#FFFFFF",
        "panel2": "#F3F5F8",
        "line": "#D0D7DE",
        "muted": "#57606A",
        "text": "#1F2328",
        "accent": "#4D7C0F",
        "chrome": "#4D7C0F",
        "status": "#15803D",
        "cyan": "#0969DA",
        "shadow": "#D0D7DE",
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
    return len(s) * font_size * 0.60


def render_banner(theme_name: str) -> str:
    t = THEMES[theme_name]
    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
        f'<title id="title">Rupal Das - Live System Profile</title>',
        f'<desc id="desc">Terminal boot and telemetry profile dashboard for Rupal Das.</desc>',
        '<defs>',
        f'<filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">',
        f'<feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="{t["shadow"]}" flood-opacity=".28"/>',
        '</filter>',
        f'<filter id="glow" x="-100%" y="-100%" width="300%" height="300%">',
        f'<feGaussianBlur stdDeviation="3" result="b"/><feFlood flood-color="{t["chrome"]}" flood-opacity=".45"/><feComposite in2="b" operator="in"/>',
        '<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>',
        '</filter>',
        '<clipPath id="bootClip"><rect x="49" y="124" width="390" height="426" rx="4"/></clipPath>',
        '<pattern id="scanlines" width="100%" height="4" patternUnits="userSpaceOnUse">',
        '<line x1="0" y1="0" x2="100%" y2="0" stroke="#000000" stroke-width="1" opacity="0.08"/>',
        '</pattern>',
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

        # LEFT PANEL: TERMINAL BOOT SEQUENCE
        f'<rect x="35" y="88" width="418" height="472" rx="6" fill="{t["panel2"]}" stroke="{t["line"]}"/>',
        f'<rect x="35" y="88" width="418" height="472" rx="6" fill="url(#scanlines)" pointer-events="none"/>',
        f'<path d="M35 124H453" stroke="{t["line"]}"/>',
        f'<text x="49" y="111" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" letter-spacing="1.2">SYS.BOOT_LOG</text>',
        f'<text x="438" y="111" text-anchor="end" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">TTY: /dev/tty0</text>',

        # Terminal Corner Accents
        f'<path d="M49 135h10M49 135v10M439 135h-10M439 135v10M49 548h10M49 548v-10M439 548h-10M439 548v-10" fill="none" stroke="{t["chrome"]}" opacity=".55"/>',

        # Animated Boot Progress Bar (top of left terminal screen)
        f'<rect x="52" y="133" width="384" height="3" rx="1.5" fill="{t["line"]}"/>',
        f'<rect x="52" y="133" height="3" rx="1.5" fill="{t["chrome"]}">'
        f'<animate attributeName="width" values="0;120;260;384;384;0" keyTimes="0;0.20;0.45;0.70;0.95;1" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
        '</rect>',

        # Terminal lines clipped inside screen
        '<g clip-path="url(#bootClip)">',
    ]

    y_pos = 154.0
    line_h = 22.8
    for start_t, style, text in BOOT_LOGS:
        t0 = round(start_t / BOOT_DUR, 3)
        t1 = round(min(0.95, (start_t + 0.08) / BOOT_DUR), 3)
        key_times = f"0;{t0};{t1};0.95;1"

        if style == "ok":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'<tspan fill="{t["status"]}" font-weight="700">[  OK  ]</tspan>'
                f'<tspan fill="{t["text"]}"> {html.escape(text)}</tspan>'
                f'</text>'
            )
        elif style == "dim":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'{html.escape(text)}'
                f'</text>'
            )
        elif style == "cyan":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" fill="{t["cyan"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" font-weight="600" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'{html.escape(text)}'
                f'</text>'
            )
        elif style == "accent":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" fill="{t["accent"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" font-weight="600" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'{html.escape(text)}'
                f'</text>'
            )
        elif style == "prompt":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'<tspan fill="{t["chrome"]}" font-weight="700">rupal2k@enterprise</tspan>'
                f'<tspan fill="{t["muted"]}">:~$</tspan>'
                f'<tspan fill="{t["text"]}"> ./init_ops.sh</tspan>'
                f'</text>'
            )
        elif style == "online":
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" font-weight="700" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'<tspan fill="{t["status"]}">● ALL SYSTEMS NOMINAL</tspan>'
                f'<tspan fill="{t["muted"]}"> · RUNNING</tspan>'
                f'</text>'
            )
        else:
            line_markup = (
                f'<text x="56" y="{y_pos:.1f}" fill="{t["text"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11.5" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{key_times}" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
                f'{html.escape(text)}'
                f'</text>'
            )
        parts.append(line_markup)
        y_pos += line_h

    # Blinking block cursor after last line
    cursor_t0 = round(7.0 / BOOT_DUR, 3)
    parts.extend([
        f'<text x="315" y="{y_pos - line_h:.1f}" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" opacity="0">'
        f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{cursor_t0};{cursor_t0 + 0.01};0.95;1" dur="{BOOT_DUR}s" repeatCount="indefinite"/>'
        '█'
        '</text>',
        '</g>',  # close clip
    ])

    # RIGHT PANEL: SYSTEM.INFO
    parts.extend([
        f'<rect x="474" y="88" width="672" height="472" rx="6" fill="{t["panel2"]}" stroke="{t["line"]}"/>',
        f'<path d="M474 124H1146" stroke="{t["line"]}"/>',
        f'<text x="490" y="111" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" letter-spacing="1.2">SYSTEM.INFO</text>',

        # LIVE pulse & @rupal2k pill
        f'<g filter="url(#glow)">',
        f'<circle cx="915" cy="106" r="3.5" fill="{t["chrome"]}"/>',
        f'<circle cx="915" cy="106" r="3.5" fill="{t["chrome"]}">'
        f'<animate attributeName="r" values="3.5;7.5;3.5" dur="2.2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.8;0;0.8" dur="2.2s" repeatCount="indefinite"/>'
        f'</circle>',
        f'</g>',
        f'<text x="927" y="111" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700">LIVE</text>',
        f'<rect x="982" y="94" width="146" height="24" rx="12" fill="{t["chrome"]}" fill-opacity=".12" stroke="{t["chrome"]}" stroke-width="1.2"/>',
        f'<text x="1055" y="111" text-anchor="middle" fill="{t["chrome"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" font-weight="700">@rupal2k</text>',
    ])

    value_right = 1127.0
    row_y = 153.0
    for label, value in ROWS:
        value_len = text_width(value, 14)
        label_len = text_width(label, 14)
        leader_start = 491 + label_len + 12
        leader_end = value_right - value_len - 12
        leader_d = dotted_leader(leader_start, leader_end, row_y - 4)

        parts.extend([
            f'<g>',
            f'<text x="491" y="{row_y:.0f}" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14">{html.escape(label)}</text>',
            f'<path d="{leader_d}" fill="none" stroke="{t["line"]}" stroke-width="1" shape-rendering="crispEdges"/>',
            f'<text x="{value_right:.0f}" y="{row_y:.0f}" text-anchor="end" fill="{t["text"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" textLength="{value_len:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(value)}</text>',
            f'</g>',
        ])
        row_y += 24.5

    parts.extend([
        f'<path d="M490 530H1130" stroke="{t["line"]}"/>',
        f'<g>',
        f'<circle cx="496" cy="544" r="3.5" fill="{t["status"]}"/>',
        f'<circle cx="496" cy="544" r="3.5" fill="{t["status"]}">'
        f'<animate attributeName="r" values="3.5;6.5;3.5" dur="2s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite"/>'
        f'</circle>',
        f'<text x="508" y="548" fill="{t["status"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11" font-weight="600">ALL SYSTEMS NOMINAL · RUNNING</text>',
        f'<text x="1128" y="548" text-anchor="end" fill="{t["muted"]}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">UTC+5:30 · INDIA NODE</text>',
        f'</g>',
        '</svg>',
    ])
    return "".join(parts)


def main():
    out_dir = Path("assets")
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        dest = out_dir / f"banner-{theme}.svg"
        dest.write_text(render_banner(theme) + "\n", encoding="utf-8")
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
