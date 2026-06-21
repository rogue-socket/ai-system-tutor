#!/usr/bin/env python3
"""Launch the workspace viewer with one command."""

from __future__ import annotations

import argparse
import os
import socket
import sys
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local AI systems workspace viewer.")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--open", action="store_true", help="Open the page in your browser automatically.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    index = root / "index.html"
    manifest = root / "manifest.json"

    if not index.exists() or not manifest.exists():
        print("WARN: index.html or manifest.json missing from this directory.")
        print("Expected workspace root to contain both files.")

    if not _port_available(args.host, args.port):
        print(f"WARN: port {args.port} is already in use.")
        print("Try: python viewer.py --port 8001")
        return 1

    os.chdir(root)
    url = f"http://{args.host}:{args.port}"
    print(f"Serving workspace viewer from: {root}")
    print(f"Open: {url}")
    if args.open:
        webbrowser.open(url)

    with ThreadingHTTPServer((args.host, args.port), SimpleHTTPRequestHandler) as httpd:
        print("Press Ctrl-C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nViewer stopped.")
        return 0


def _port_available(host: str, port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            return True
    except OSError:
        return False


if __name__ == "__main__":
    sys.exit(main())
