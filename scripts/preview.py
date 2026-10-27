#!/usr/bin/env python3
"""Launch local web server to preview generated SVG assets in preview.html."""

import http.server
import socketserver
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PORT = 3300

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

def main():
    url = f"http://localhost:{PORT}/preview.html"
    print(f"Starting preview server at {url}...")
    webbrowser.open(url)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {ROOT} on {PORT}. Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nPreview server stopped.")

if __name__ == "__main__":
    main()
