import os, shutil, subprocess, time

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
exe = os.path.join(root, "凝紫客户端.exe")
cfg = os.path.join(root, "config.ini")
logp = os.path.join(root, "launcher.log")

shutil.copy2(cfg, cfg + ".dshbak")
open(cfg, "w", encoding="utf-8-sig").write("name=FocusontheMilky\npass=\nupdate=http://127.0.0.1:9/upd\n")

before = os.path.getsize(logp) if os.path.exists(logp) else 0
p = subprocess.Popen([exe], cwd=root)
time.sleep(7)
subprocess.run(["taskkill", "/f", "/t", "/pid", str(p.pid)], capture_output=True)
time.sleep(1)

data = b""
if os.path.exists(logp):
    with open(logp, "rb") as f:
        f.seek(before)
        data = f.read()
try:
    text = data.decode("utf-8")
except Exception:
    text = data.decode("gbk", "ignore")

open(r"C:\大肥鱼\updatetest.txt", "w", encoding="utf-8").write(text)
shutil.move(cfg + ".dshbak", cfg)
print("DONE")
