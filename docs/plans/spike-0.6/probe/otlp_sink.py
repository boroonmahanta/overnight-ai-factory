#!/usr/bin/env python3
"""A tiny OTLP/HTTP receiver for spike 0.6 (ADO 2451) and 0.20 (ADO 2738).

Stands in for a collector in the job, since Application Insights does not exist
yet. Listens on 127.0.0.1 only. Every POST to /v1/traces, /v1/metrics or
/v1/logs is written to one JSON line in --out: the path, the content type and
the body (parsed JSON for http/json, base64 for anything else). It answers 200
with an empty JSON object, which is what an OTLP/HTTP exporter expects.

Standard library only. Never logs headers (an exporter may send auth headers).

  python3 -I probe/otlp_sink.py --port 4318 --out sink.jsonl &
"""
import argparse
import base64
import gzip
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOCK = threading.Lock()


def make_handler(out_path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):  # quiet: no request lines in the job log
            pass

        def read_body(self):
            # VS Code's Copilot Chat exporter sends chunked bodies with no Content-Length
            # (spike 0.20): read both ways, then undo gzip if the sender says so.
            if "chunked" in (self.headers.get("Transfer-Encoding") or "").lower():
                parts = []
                while True:
                    size = int(self.rfile.readline().split(b";")[0].strip() or b"0", 16)
                    if size == 0:
                        self.rfile.readline()
                        break
                    parts.append(self.rfile.read(size))
                    self.rfile.readline()
                body = b"".join(parts)
            else:
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
            if (self.headers.get("Content-Encoding") or "").lower() == "gzip" and body:
                body = gzip.decompress(body)
            return body

        def do_POST(self):
            body = self.read_body()
            ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip()
            rec = {"path": self.path, "content_type": ctype, "bytes": len(body),
                   "encoding": self.headers.get("Content-Encoding"),
                   "transfer": self.headers.get("Transfer-Encoding"),
                   "agent": (self.headers.get("User-Agent") or "")[:80]}
            if ctype == "application/json":
                try:
                    rec["json"] = json.loads(body.decode("utf-8"))
                except ValueError:
                    rec["base64"] = base64.b64encode(body).decode("ascii")
            else:
                rec["base64"] = base64.b64encode(body).decode("ascii")
            with LOCK, open(out_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")
            reply = b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(reply)))
            self.end_headers()
            self.wfile.write(reply)

        def do_GET(self):  # a health check for the job
            self.send_response(200)
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"ok")

    return Handler


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=4318)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), make_handler(a.out))
    print(f"otlp sink on 127.0.0.1:{a.port} -> {a.out}", file=sys.stderr, flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
