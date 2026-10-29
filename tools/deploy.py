import os, shutil, sys

ROOT = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
UPDATER_SRC = r"C:\大肥鱼\build\凝紫客户端.exe"
CORE = os.path.join(ROOT, "凝紫客户端(主程序).exe")
MAIN = os.path.join(ROOT, "凝紫客户端.exe")
INI = os.path.join(ROOT, "updater.ini")
URL = "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/update.json"

log = []
if not os.path.exists(CORE):
    if os.path.exists(MAIN):
        os.rename(MAIN, CORE)
        log.append("renamed launcher -> 凝紫客户端(主程序).exe")
    else:
        log.append("ERROR: no main exe")
else:
    log.append("core already renamed")

shutil.copy2(UPDATER_SRC, MAIN)
log.append("updater installed as 凝紫客户端.exe (%d bytes)" % os.path.getsize(MAIN))

with open(INI, "w", encoding="utf-8") as f:
    f.write("url=" + URL + "\n")
log.append("updater.ini written")

log.append("---- listing ----")
for n in sorted(os.listdir(ROOT)):
    p = os.path.join(ROOT, n)
    log.append("%-30s %10d %s" % (n, os.path.getsize(p) if os.path.isfile(p) else 0, "DIR" if os.path.isdir(p) else ""))

open(r"C:\大肥鱼\deploy.txt", "w", encoding="utf-8").write("\n".join(log))
print("DONE")
