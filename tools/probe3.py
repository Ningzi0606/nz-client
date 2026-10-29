import os, shutil, subprocess, time, threading, hashlib, json
from http.server import BaseHTTPRequestHandler, HTTPServer

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
exe = os.path.join(root, "凝紫客户端.exe")
cfg = os.path.join(root, "config.ini")
logp = os.path.join(root, "launcher.log")
reqs = []

payload = b"PROBE3-CONTENT-" * 8
h = hashlib.sha1(payload).hexdigest()
manifest = json.dumps({
    "version": "v-probe3",
    "files": {
        "probe3.txt": {"hash": h, "size": len(payload)},
        "logo.png": {"hash": "0" * 40, "size": 13069},
    },
    "remove": ["probe3_remove_me.txt"],
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

srv = HTTPServer(("127.0.0.1", 8125), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

shutil.copy2(cfg, cfg + ".dshbak")
open(cfg, "w", encoding="utf-8-sig").write("name=FocusontheMilky\npass=\nupdate=http://127.0.0.1:8125/base\n")

# make a removable file to test "remove"
with open(os.path.join(root, "probe3_remove_me.txt"), "w") as f:
    f.write("x")

before = os.path.getsize(logp) if os.path.exists(logp) else 0
p = subprocess.Popen([exe], cwd=root)
time.sleep(12)
subprocess.run(["taskkill", "/f", "/t", "/pid", str(p.pid)], capture_output=True)
time.sleep(1)
srv.shutdown()

data = b""
if os.path.exists(logp):
    with open(logp, "rb") as f:
        f.seek(before)
        data = f.read()
try:
    text = data.decode("utf-8")
except Exception:
    text = data.decode("gbk", "ignore")

info = []
for n in ("probe3.txt", "probe3_remove_me.txt"):
    p2 = os.path.join(root, n)
    info.append("%s exists=%s size=%s" % (n, os.path.exists(p2), os.path.getsize(p2) if os.path.exists(p2) else "-"))

open(r"C:\大肥鱼\probe3.txt", "w", encoding="utf-8").write(
    "\n".join(reqs) + "\n---- files ----\n" + "\n".join(info) + "\n---- log ----\n" + text)
shutil.move(cfg + ".dshbak", cfg)
print("DONE")
