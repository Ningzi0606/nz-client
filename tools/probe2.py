import os, shutil, subprocess, time, threading, hashlib, json
from http.server import BaseHTTPRequestHandler, HTTPServer

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
exe = os.path.join(root, "凝紫客户端.exe")
cfg = os.path.join(root, "config.ini")
logp = os.path.join(root, "launcher.log")
reqs = []

logo = open(os.path.join(root, "logo.png"), "rb").read()
sha1 = hashlib.sha1(logo).hexdigest()
manifest = json.dumps({"version": "v1", "files": {"logo.png": {"hash": sha1, "size": len(logo)}}})

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        reqs.append("GET " + self.path + " UA=" + str(self.headers.get("User-Agent")))
        if self.path.rstrip("/") == "/base":
            body = manifest.encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        else:
            body = logo
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

srv = HTTPServer(("127.0.0.1", 8124), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

shutil.copy2(cfg, cfg + ".dshbak")
open(cfg, "w", encoding="utf-8-sig").write("name=FocusontheMilky\npass=\nupdate=http://127.0.0.1:8124/base\n")

before = os.path.getsize(logp) if os.path.exists(logp) else 0
p = subprocess.Popen([exe], cwd=root)
time.sleep(10)
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

cv = os.path.join(root, ".clientver")
cvtext = ""
if os.path.exists(cv):
    cvtext = open(cv, "rb").read().decode("utf-8", "ignore")

open(r"C:\大肥鱼\probe2.txt", "w", encoding="utf-8").write(
    "\n".join(reqs) + "\n---- clientver ----\n" + cvtext + "\n---- log ----\n" + text)
shutil.move(cfg + ".dshbak", cfg)
print("DONE")
