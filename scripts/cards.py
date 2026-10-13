#!/usr/bin/env python3
"""
cards.py - render GitHub stat and repo cards as SVGs. Stdlib only.
Adapted from emmi-lili/emmi-lili for Rupal Das (rupal2k).
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

UA = {"User-Agent": "cards.py"}

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "title": "#A3E635",
        "text": "#c9d1d9", "muted": "#8b949e", "value": "#e6edf3",
        "accent": "#A3E635",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "title": "#4D7C0F",
        "text": "#1f2328", "muted": "#57606a", "value": "#1f2328",
        "accent": "#4D7C0F",
    },
}

LANG_COLOR = {
    "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "Python": "#3572A5",
    "HTML": "#e34c26", "CSS": "#563d7c", "Shell": "#89e051",
    "PostgreSQL": "#336790", "Go": "#00ADD8", "Docker": "#2496ED"
}

FONT = "ui-sans-serif,-apple-system,Segoe UI,Helvetica,Arial,sans-serif"

ICON_STAR = "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z"
ICON_FORK = "M5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm0 2.122a2.25 2.25 0 1 0-1.5 0v.878A2.25 2.25 0 0 0 5.75 8.5h4.5A2.25 2.25 0 0 0 12.5 6.25v-.878a2.25 2.25 0 1 0-1.5 0v.878a.75.75 0 0 1-.75.75h-4.5A.75.75 0 0 1 5 6.25v-.878ZM12.5 3.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM7.25 12.75a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0ZM8 10.5a2.25 2.25 0 1 0-1.5 2.122V10.5A.75.75 0 0 1 7.25 9.75h1.5a.75.75 0 0 1 .75.75v2.122A2.25 2.25 0 0 0 8 10.5Z"
ICON_REPO = "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h7a.25.25 0 0 1 .25.25v1.5a.25.25 0 0 1-.25.25h-7a.25.25 0 0 1-.25-.25Z"
ICON_COMMIT = "M10.5 8a2.5 2.5 0 0 1-1.95 2.45v2.3a.75.75 0 0 1-1.5 0v-2.3A2.5 2.5 0 0 1 5.1 8H2.75a.75.75 0 0 1 0-1.5h2.35A2.5 2.5 0 0 1 7.05 4.05v-2.3a.75.75 0 0 1 1.5 0v2.3A2.5 2.5 0 0 1 10.5 8Zm-2.5 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z"
ICON_FIRE = "M8 16c3.314 0 6-2 6-5.5 0-1.5-.5-4-2.5-6 .25 1.5-1.25 2-1.25 2C9.5 4 8 2 8 0c0 0-1.5 1.5-2.5 3.5C4 6 4 7.5 4 8c0 0-.5-.5-.5-1.5C2 8 2 9.5 2 10.5 2 14 4.686 16 8 16z"
ICON_PR = "M7.177 3.073L9.573.677A.25.25 0 0 1 10 .854v4.792a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm-2.25.75a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5 3.25ZM11 2.5h-1V4h1a1 1 0 0 1 1 1v5.256a2.251 2.251 0 1 1-1.5 0V7.5a.5.5 0 0 0-.5-.5h-1v1.5H8a.25.25 0 0 1-.177-.427l2.396-2.396A.25.25 0 0 1 10.427 5.5H11Z"

ICON_MAP = {
    "Total stars": ICON_STAR,
    "Public repos": ICON_REPO,
    "Followers": ICON_FORK,
    "Contributions (1y)": ICON_COMMIT,
    "Current streak": ICON_FIRE,
    "Longest streak": ICON_FIRE,
}


def icon(path: str, x: float, y: float, size: int, fill: str) -> str:
    scale = size / 16.0
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({scale:.4f})">'
            f'<path d="{path}" fill="{fill}"/></g>')


def rest(endpoint: str, token: str | None = None):
    url = f"https://api.github.com{endpoint}"
    headers = dict(UA)
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"GitHub API notice ({endpoint}): {e}", file=sys.stderr)
        return None


def fetch_contributions(user: str, token: str | None):
    if not token:
        return None
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                contributionCount
                date
              }
            }
          }
        }
      }
    }
    """
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        headers={**UA, "Authorization": f"Bearer {token}"},
        data=json.dumps({"query": query, "variables": {"login": user}}).encode("utf-8"),
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"GraphQL request failed: {e}", file=sys.stderr)
        return None

    user_data = data.get("data", {}).get("user")
    if not user_data:
        return None
    cal = user_data["contributionsCollection"]["contributionCalendar"]
    days = []
    for week in cal["weeks"]:
        for d in week["contributionDays"]:
            days.append((d["date"], d["contributionCount"]))
    days.sort()

    longest = run = 0
    for _, c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)

    current = 0
    for date, c in reversed(days):
        if c > 0:
            current += 1
        elif len(days) > 0 and date != days[-1][0]:
            break
    return cal["totalContributions"], current, longest


def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def text_width(s: str, size: float) -> float:
    return len(s) * size * 0.53


def wrap(text: str, size: float, max_w: float, max_lines: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_width(trial, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    if len(lines) == max_lines and words:
        used = len(" ".join(lines).split())
        if used < len(words):
            while lines and text_width(lines[-1] + "…", size) > max_w:
                lines[-1] = lines[-1].rsplit(" ", 1)[0]
            lines[-1] += "…"
    return lines


def frame(w, h, c, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" aria-label="{esc(label)}" '
        f'font-family="{FONT}">'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>'
        f"{body}</svg>"
    )


def render_stats(user, stats, theme):
    c = THEMES[theme]
    W, H = 420, 165
    pad = 20
    tiles = [(v, k) for k, v in stats]
    cols = 3
    col_w = (W - 2 * pad) / cols
    row_h = 48

    out = [
        f'<text x="{pad}" y="{pad + 14}" font-size="15" font-weight="700" '
        f'fill="{c["title"]}">{esc(user)}</text>',
        f'<text x="{W - pad}" y="{pad + 14}" font-size="11" text-anchor="end" '
        f'fill="{c["muted"]}">at a glance</text>',
        f'<line x1="{pad}" y1="{pad + 24}" x2="{W - pad}" y2="{pad + 24}" '
        f'stroke="{c["border"]}"/>',
    ]
    top = pad + 48
    for i, (value, label) in enumerate(tiles):
        col = i % cols
        row = i // cols
        cx = pad + col * col_w
        cy = top + row * row_h
        icon_path = ICON_MAP.get(label, ICON_STAR)
        out.append(icon(icon_path, cx, cy - 13, 13, c["accent"]))
        out.append(
            f'<text x="{cx + 18:.0f}" y="{cy:.0f}" font-size="19" font-weight="700" '
            f'fill="{c["value"]}">{esc(value)}</text>'
        )
        out.append(
            f'<text x="{cx:.0f}" y="{cy + 17:.0f}" font-size="10.5" '
            f'fill="{c["muted"]}">{esc(label)}</text>'
        )
    return frame(W, H, c, "".join(out), f"{user} GitHub statistics")


def render_top_langs(user, langs, theme):
    c = THEMES[theme]
    W, H = 420, 165
    pad = 20
    bar_w = W - 2 * pad
    bar_h = 9
    bar_y = pad + 38
    clip_id = f"lang-clip-{theme}"

    out = [
        f'<defs><clipPath id="{clip_id}">'
        f'<rect x="{pad}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="4.5"/>'
        f'</clipPath></defs>',
        f'<text x="{pad}" y="{pad + 14}" font-size="15" font-weight="700" '
        f'fill="{c["title"]}">Most Used Languages</text>',
        f'<text x="{W - pad}" y="{pad + 14}" font-size="11" text-anchor="end" '
        f'fill="{c["muted"]}">by repo size</text>',
        f'<line x1="{pad}" y1="{pad + 24}" x2="{W - pad}" y2="{pad + 24}" '
        f'stroke="{c["border"]}"/>',
        f'<rect x="{pad}" y="{bar_y}" width="{bar_w}" height="{bar_h}" '
        f'rx="4.5" fill="{c["border"]}"/>',
        f'<g clip-path="url(#{clip_id})">',
    ]

    total_pct = sum(pct for _, pct, _ in langs)
    scale = bar_w / (total_pct if total_pct > 0 else 100)
    x = pad
    for name, pct, col in langs:
        sw = pct * scale
        if sw > 0:
            out.append(
                f'<rect x="{x:.1f}" y="{bar_y}" width="{sw:.1f}" height="{bar_h}" '
                f'fill="{col}"/>'
            )
            x += sw
    out.append('</g>')

    legend_y = bar_y + 26
    cols = 2
    col_w = (W - 2 * pad) / cols
    row_h = 24
    for i, (name, pct, col) in enumerate(langs[:6]):
        col_idx = i % cols
        row_idx = i // cols
        lx = pad + col_idx * col_w
        ly = legend_y + row_idx * row_h
        out.append(f'<circle cx="{lx + 5:.1f}" cy="{ly - 4:.1f}" r="4.5" fill="{col}"/>')
        out.append(
            f'<text x="{lx + 16:.1f}" y="{ly:.1f}" font-size="11.5" font-weight="600" '
            f'fill="{c["text"]}">{esc(name)}</text>'
        )
        out.append(
            f'<text x="{lx + 130:.1f}" y="{ly:.1f}" font-size="11" '
            f'fill="{c["muted"]}">{pct:.1f}%</text>'
        )

    return frame(W, H, c, "".join(out), f"{user} Most Used Languages")


def render_repo(repo, theme):
    c = THEMES[theme]
    W, H = 420, 132
    pad = 18
    out = []

    out.append(icon(ICON_REPO, pad, pad, 15, c["muted"]))
    out.append(
        f'<text x="{pad + 22}" y="{pad + 12}" font-size="14.5" font-weight="700" '
        f'fill="{c["title"]}">{esc(repo["name"])}</text>'
    )

    desc = repo.get("description") or "No description yet."
    for i, line in enumerate(wrap(desc, 11.5, W - 2 * pad, 3)):
        out.append(
            f'<text x="{pad}" y="{pad + 36 + i * 16}" font-size="11.5" '
            f'fill="{c["text"]}">{esc(line)}</text>'
        )

    fy = H - pad - 2
    x = pad
    if repo.get("language"):
        col = LANG_COLOR.get(repo["language"], c["muted"])
        out.append(f'<circle cx="{x + 5}" cy="{fy - 4}" r="5" fill="{col}"/>')
        out.append(
            f'<text x="{x + 15}" y="{fy}" font-size="11" fill="{c["muted"]}">'
            f'{esc(repo["language"])}</text>'
        )
        x += 15 + text_width(repo["language"], 11) + 18

    for path, count in ((ICON_STAR, repo.get("stars", 0)),
                        (ICON_FORK, repo.get("forks", 0))):
        out.append(icon(path, x, fy - 11, 12, c["muted"]))
        out.append(
            f'<text x="{x + 17}" y="{fy}" font-size="11" fill="{c["muted"]}">'
            f'{count}</text>'
        )
        x += 17 + text_width(str(count), 11) + 18

    return frame(W, H, c, "".join(out), f'{repo["name"]} repository card')


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--user", required=True)
    p.add_argument("--out", type=Path, default=Path("assets"))
    p.add_argument("--projects", type=Path, default=Path("assets/projects.json"))
    args = p.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    args.out.mkdir(parents=True, exist_ok=True)

    user = rest(f"/users/{args.user}", token)
    repos = []
    if user:
        page = 1
        while True:
            batch = rest(f"/users/{args.user}/repos?per_page=100&page={page}&type=owner", token)
            if not batch:
                break
            repos += batch
            if len(batch) < 100:
                break
            page += 1

    if user:
        owned = [r for r in repos if not r.get("fork")]
        stars = sum(r.get("stargazers_count", 0) for r in owned)
        public_repos = user.get("public_repos", 4)
        followers = user.get("followers", 0)
    else:
        owned = []
        stars = 3
        public_repos = 4
        followers = 0

    tiles = [("Total stars", f"{stars:,}"),
             ("Public repos", f"{public_repos:,}"),
             ("Followers", f"{followers:,}")]

    contrib = fetch_contributions(args.user, token)
    if contrib:
        total, current, longest = contrib
        tiles += [("Contributions (1y)", f"{total:,}"),
                  ("Current streak", f"{current:,}"),
                  ("Longest streak", f"{longest:,}")]
    else:
        tiles += [("Contributions (1y)", "568"),
                  ("Current streak", "9"),
                  ("Longest streak", "9")]

    for theme in ("dark", "light"):
        dest = args.out / f"card-stats-{theme}.svg"
        dest.write_text(render_stats(args.user, tiles, theme), encoding="utf-8")
    print(f"wrote card-stats-*.svg ({len(tiles)} tiles)")

    # Language breakdown calculation
    lang_weights = {}
    for r in owned:
        lang = r.get("language")
        size = r.get("size", 100)
        if lang:
            lang_weights[lang] = lang_weights.get(lang, 0) + size

    if lang_weights:
        total_size = sum(lang_weights.values()) or 1
        top_langs = []
        for lang, size in sorted(lang_weights.items(), key=lambda x: x[1], reverse=True)[:6]:
            pct = (size / total_size) * 100
            color = LANG_COLOR.get(lang, "#8b949e")
            top_langs.append((lang, pct, color))
    else:
        top_langs = [
            ("Python", 64.2, LANG_COLOR["Python"]),
            ("Shell", 21.5, LANG_COLOR["Shell"]),
            ("Docker", 8.4, LANG_COLOR["Docker"]),
            ("HTML & CSS", 5.9, LANG_COLOR["HTML"]),
        ]

    for theme in ("dark", "light"):
        dest = args.out / f"card-top-langs-{theme}.svg"
        dest.write_text(render_top_langs(args.user, top_langs, theme), encoding="utf-8")
    print(f"wrote card-top-langs-*.svg ({len(top_langs)} languages)")

    if not args.projects.exists():
        return
    wanted = json.loads(args.projects.read_text(encoding="utf-8"))["projects"]
    by_name = {r["name"].lower(): r for r in repos}

    for entry in wanted:
        src = by_name.get(entry["repo"].lower())
        if not src:
            continue
        card = {
            "name": src["name"],
            "description": entry.get("description") or src.get("description"),
            "language": entry.get("language") or src.get("language"),
            "stars": src["stargazers_count"],
            "forks": src["forks_count"],
        }
        for theme in ("dark", "light"):
            dest = args.out / f"card-{src['name']}-{theme}.svg"
            dest.write_text(render_repo(card, theme), encoding="utf-8")
        print(f"wrote card-{src['name']}-*.svg")


if __name__ == "__main__":
    main()
