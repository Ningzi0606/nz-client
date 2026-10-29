import os, shutil, subprocess, time, threading, hashlib, json
from http.server import BaseHTTPRequestHandler, HTTPServer

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
exe = os.path.join(root, "凝紫客户端.exe")
cfg = os.path.join(root, "config.ini")
logp = os.path.join(root, "launcher.log")
reqs = []

payload = b"PROBE6-LOGO-" * 20
h = hashlib.sha1(payload).hexdigest()
manifest = json.dumps({
    "version": "2",
    "files": {"logo.png": {"hash": h, "size": len(payload)}},
})

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        reqs.append("GET " + self.path)
        if self.path.rstrip("/") == "/base":
            body = manifest.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            body = payload
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

srv = HTTPServer(("127.0.0.1", 8128), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

logo_path = os.path.join(root, "logo.png")
shutil.copy2(logo_path, r"C:\大肥鱼\logo_backup2.png")
shutil.copy2(cfg, cfg + ".dshbak")
with open(os.path.join(root, ".clientver"), "w") as f:
    f.write("1")
open(cfg, "w", encoding="utf-8-sig").write("name=FocusontheMilky\npass=\nupdate=http://127.0.0.1:8128/base\n")

before = os.path.getsize(logp) if os.path.exists(logp) else 0
p = subprocess.Popen([exe], cwd=root)
time.sleep(14)
subprocess.run(["taskkill", "/f", "/t", "/pid", str(p.pid)], capture_output=True)
time.sleep(1)
srv.shutdown()

with open(logo_path, "rb") as f:
    now = f.read()
data = b""
if os.path.exists(logp):
    with open(logp, "rb") as f:
        f.seek(before)
        data = f.read()
try:
    text = data.decode("utf-8")
except Exception:
    text = data.decode("gbk", "ignore")

out = ["\n".join(reqs), "---- logo size now: %d ----" % len(now), text]
open(r"C:\大肥鱼\probe6.txt", "w", encoding="utf-8").write("\n".join(out))
shutil.move(cfg + ".dshbak", cfg)
print("DONE")
