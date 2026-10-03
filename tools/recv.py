"""Tiny local receiver: the page POSTs a blob to http://127.0.0.1:18765/<name>; saved into _variants/recv/<name>."""
import http.server, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_variants", "recv")
os.makedirs(OUT, exist_ok=True)
class H(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); data = self.rfile.read(n)
        name = os.path.basename(self.path.strip("/")) or "blob.bin"
        open(os.path.join(OUT, name), "wb").write(data)
        self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 18765), H).serve_forever()
