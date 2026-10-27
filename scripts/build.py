#!/usr/bin/env python3
"""Build & render all SVG cards, banners, and radars locally."""

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def run(*cmd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=ROOT, check=True)

def main():
    print("=" * 60)
    print("Building Rupal Das GitHub Profile Assets")
    print("=" * 60)

    # 1. Terminal banner
    print("\n[1/3] Rendering Terminal Banner...")
    run(sys.executable, "scripts/banner.py")

    # 2. Competencies & Tooling Radars
    print("\n[2/3] Rendering Skill & Domain Radars...")
    run(sys.executable, "scripts/radar.py", "--data", "assets/skills.json", "-o", "assets/radar")
    run(sys.executable, "scripts/radar.py", "--data", "assets/langmix.json", "-o", "assets/radar-langs")

    # 3. GitHub Cards & Statistics
    print("\n[3/3] Rendering GitHub Telemetry & Project Cards...")
    run(sys.executable, "scripts/cards.py", "--user", "rupal2k", "--projects", "assets/projects.json", "--out", "assets")

    print("\n" + "=" * 60)
    print("All profile assets rendered successfully in assets/")
    print("To preview: run `python scripts/preview.py` or open preview.html")
    print("=" * 60)

if __name__ == "__main__":
    main()
