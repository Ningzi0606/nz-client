import os, shutil, subprocess, time, threading
from http.server import BaseHTTPRequestHandler, HTTPServer

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
exe = os.path.join(root, "凝紫客户端.exe")
cfg = os.path.join(root, "config.ini")
logp = os.path.join(root, "launcher.log")
reqs = []

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        reqs.append("GET " + self.path + " UA=" + str(self.headers.get("User-Agent")))
        body = b"{}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

srv = HTTPServer(("127.0.0.1", 8123), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

shutil.copy2(cfg, cfg + ".dshbak")
open(cfg, "w", encoding="utf-8-sig").write("name=FocusontheMilky\npass=\nupdate=http://127.0.0.1:8123/base\n")

before = os.path.getsize(logp) if os.path.exists(logp) else 0
p = subprocess.Popen([exe], cwd=root)
time.sleep(9)
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

open(r"C:\大肥鱼\probe.txt", "w", encoding="utf-8").write("\n".join(reqs) + "\n---- log ----\n" + text)
shutil.move(cfg + ".dshbak", cfg)
print("DONE")
