# Profile Development Guide

This repository powers the personal GitHub profile README for **[@rupal2k](https://github.com/rupal2k)**.

---

## 🚀 Quick Start

### 1. Build All Assets
Generate all animated terminal banners, skill radars, and GitHub telemetry cards:
```bash
python scripts/build.py
```

### 2. Live Preview
Launch the local visual preview in your browser:
```bash
python scripts/preview.py
```
Or open [`preview.html`](preview.html) directly in any web browser.

---

## 🛠️ Configuration & Customization

| Component | Config File / Script | Purpose |
| :--- | :--- | :--- |
| **Terminal Banner** | `scripts/banner.py` | Customize boot sequence log lines, system info spec sheet, role, and color themes. |
| **Operational Radar** | `assets/skills.json` | Adjust score values (0–100) and labels for domain & operational competencies. |
| **Technical Radar** | `assets/langmix.json` | Adjust score values (0–100) and labels for languages and infrastructure tooling. |
| **Featured Projects** | `assets/projects.json` | Add or update public featured repositories and showcase descriptions. |
| **Profile Copy & Layout** | `README.md` | Profile sections, career highlights, and enterprise case summaries. |

---

## 🤖 Automated CI/CD
- GitHub Actions (`.github/workflows/charts.yml`) automatically rebuilds telemetry charts and cards **every 2 hours**.
- Pushing changes to `main` targeting `assets/**`, `scripts/**`, or `README.md` automatically triggers an on-demand regeneration and sync.
