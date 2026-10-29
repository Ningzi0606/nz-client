import os, shutil, subprocess, time

WS = r"C:\大肥鱼"
T = os.path.join(WS, "testinst")
shutil.rmtree(T, ignore_errors=True)
os.makedirs(os.path.join(T, "game"))
shutil.copy2(r"C:\Windows\System32\hostname.exe", os.path.join(T, "凝紫客户端.exe"))
shutil.copy2(os.path.join(WS, "build", "凝紫客户端v5升级器.exe"), os.path.join(T, "凝紫客户端v5升级器.exe"))

p = subprocess.Popen([os.path.join(T, "凝紫客户端v5升级器.exe")], cwd=T)
time.sleep(4)
subprocess.run(["taskkill", "/f", "/im", "凝紫客户端v5升级器.exe"], capture_output=True)
time.sleep(1)

res = []
for n in sorted(os.listdir(T)):
    p2 = os.path.join(T, n)
    res.append("%-30s %s" % (n, os.path.getsize(p2) if os.path.isfile(p2) else "DIR"))
ini = os.path.join(T, "updater.ini")
if os.path.exists(ini):
    res.append("---- updater.ini ----")
    res.append(open(ini, encoding="utf-8").read())
main = os.path.join(T, "凝紫客户端.exe")
res.append("updater size: %d" % (os.path.getsize(main) if os.path.exists(main) else -1))
open(os.path.join(WS, "testinst.txt"), "w", encoding="utf-8").write("\n".join(res))
print("OK")
