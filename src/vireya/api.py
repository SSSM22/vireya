from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vireya.app import run_demo
from vireya.auth import AuthService
from vireya.storage import JsonStore


class VireyaHandler(BaseHTTPRequestHandler):
    auth = AuthService()
    store = JsonStore("data/vireya.json")

    def _send(self, payload: Any, status: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send({"status": "ok"})
            return
        if self.path == "/demo":
            self._send(run_demo())
            return
        self._send({"error": "not found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path == "/login":
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            user = self.auth.authenticate(data.get("username", ""), data.get("password", ""))
            if user is None:
                self._send({"error": "invalid credentials"}, status=401)
                return
            session = self.auth.create_session(user.username)
            self._send({"token": session, "role": user.role})
            return
        self._send({"error": "not found"}, status=404)


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = HTTPServer((host, port), VireyaHandler)
    print(f"Serving Vireya API on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
