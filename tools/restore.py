import os, shutil, zipfile, json

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
zip_path = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4.zip"
info = []

bak = os.path.join(root, "config.ini.dshbak")
cfg = os.path.join(root, "config.ini")
if os.path.exists(bak):
    shutil.move(bak, cfg)
    info.append("config restored")

# restore logo.png from the original zip
target = os.path.join(root, "logo.png")
with zipfile.ZipFile(zip_path) as z:
    names = [n for n in z.namelist() if n.endswith("logo.png") and n.count("/") == 1]
    info.append("zip logo entries: %s" % names)
    if names:
        data = z.read(names[0])
        with open(target, "wb") as f:
            f.write(data)
        info.append("logo.png restored %d bytes" % len(data))

info.append("---- root listing ----")
for n in sorted(os.listdir(root)):
    p = os.path.join(root, n)
    info.append("%-28s %10d %s" % (n, os.path.getsize(p) if os.path.isfile(p) else 0, "DIR" if os.path.isdir(p) else ""))

for n in (".clientver", "config.ini"):
    p = os.path.join(root, n)
    if os.path.exists(p):
        with open(p, "rb") as f:
            info.append("---- %s ----\n%s" % (n, f.read().decode("utf-8", "ignore")))

open(r"C:\大肥鱼\restore.txt", "w", encoding="utf-8").write("\n".join(info))
print("DONE")
