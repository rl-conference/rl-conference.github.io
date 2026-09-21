#!/usr/bin/env python3
"""Simple static preview server for the RLC website.

Usage:
    python3 preview.py            # serve on http://localhost:8000
    python3 preview.py 5000       # serve on http://localhost:5000
    python3 preview.py --no-open  # don't auto-open the browser
"""

import argparse
import contextlib
import functools
import http.server
import os
import socket
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serve files from the repo root, defaulting bare paths to index.html."""

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".css": "text/css",
        ".svg": "image/svg+xml",
        ".webmanifest": "application/manifest+json",
        ".json": "application/json",
        ".webp": "image/webp",
    }

    def end_headers(self):
        # Disable caching so edits show up on refresh.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def find_open_port(preferred):
    """Return the preferred port if free, otherwise the next available one."""
    for port in range(preferred, preferred + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if sock.connect_ex(("127.0.0.1", port)) != 0:
                return port
    raise SystemExit(f"No free port found in range {preferred}-{preferred + 49}")


def main():
    parser = argparse.ArgumentParser(description="Preview the RLC static site locally.")
    parser.add_argument("port", nargs="?", type=int, default=8000, help="Port to serve on (default: 8000)")
    parser.add_argument("--host", default="localhost", help="Host to bind (default: localhost)")
    parser.add_argument("--no-open", action="store_true", help="Do not open a browser automatically")
    args = parser.parse_args()

    port = find_open_port(args.port)
    handler = functools.partial(Handler, directory=ROOT)

    with http.server.ThreadingHTTPServer((args.host, port), handler) as httpd:
        url = f"http://{args.host}:{port}/index.html"
        print(f"Serving {ROOT}")
        print(f"Preview at {url}  (schedule: http://{args.host}:{port}/2026/schedule.html)")
        print("Press Ctrl+C to stop.")

        if not args.no_open:
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()

        with contextlib.suppress(KeyboardInterrupt):
            httpd.serve_forever()
        print("\nStopped.")


if __name__ == "__main__":
    main()
