import os, shutil, subprocess, threading, time, hashlib, json
from http.server import BaseHTTPRequestHandler, HTTPServer

WS = r"C:\大肥鱼"
T = os.path.join(WS, "testclient")
shutil.rmtree(T, ignore_errors=True)
os.makedirs(os.path.join(T, "data"))
shutil.rmtree(os.path.join(WS, "testdist"), ignore_errors=True)
os.makedirs(os.path.join(WS, "testdist"))

shutil.copy2(r"C:\Windows\System32\hostname.exe", os.path.join(T, "凝紫客户端(主程序).exe"))
shutil.copy2(os.path.join(WS, "build", "凝紫客户端.exe"), os.path.join(T, "凝紫客户端.exe"))

old = b"OLD-CONTENT"
new = b"NEW-CONTENT-2026-10-28\n" * 3
open(os.path.join(T, "data", "a.txt"), "wb").write(old)
open(os.path.join(WS, "testdist", "a.txt"), "wb").write(new)

sha = hashlib.sha256(new).hexdigest()
port = 8131
manifest = {
    "version": "test-2",
    "base": "http://127.0.0.1:%d/dist/" % port,
    "files": {"data/a.txt": {"sha256": sha, "size": len(new)}},
    "remove": ["data/gone.txt"],
}
open(os.path.join(WS, "testdist", "update.json"), "w", encoding="utf-8").write(json.dumps(manifest))
open(os.path.join(T, "updater.ini"), "w", encoding="utf-8").write("url=http://127.0.0.1:%d/dist/update.json\n" % port)
open(os.path.join(T, "data", "gone.txt"), "w").write("x")

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/dist/update.json":
            data = open(os.path.join(WS, "testdist", "update.json"), "rb").read()
        elif path == "/dist/data/a.txt":
            data = new
        else:
            self.send_response(404); self.end_headers(); return
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass

srv = HTTPServer(("127.0.0.1", port), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

p = subprocess.Popen([os.path.join(T, "凝紫客户端.exe")], cwd=T)
time.sleep(9)

res = []
ap = os.path.join(T, "data", "a.txt")
a = open(ap, "rb").read() if os.path.exists(ap) else b""
res.append("a.txt updated: %s" % (a == new))
res.append("gone removed: %s" % (not os.path.exists(os.path.join(T, "data", "gone.txt"))))
cv = os.path.join(T, ".clientver")
res.append("clientver: %s" % (open(cv, encoding="utf-8").read().strip() if os.path.exists(cv) else "-"))
ulog = os.path.join(T, "updater.log")
if os.path.exists(ulog):
    res.append("---- updater.log ----")
    res.append(open(ulog, encoding="utf-8", errors="ignore").read())
open(os.path.join(WS, "updatetest_result.txt"), "w", encoding="utf-8").write("\n".join(res))
srv.shutdown()
print("OK")
