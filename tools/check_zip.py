import zipfile, os
p = r"C:\大肥鱼\凝紫客户端-完整版-v5.zip"
z = zipfile.ZipFile(p)
names = z.namelist()
out = ["entries=%d size=%.1fMB" % (len(names), os.path.getsize(p) / 1048576.0)]
top = [n for n in names if n.count("/") == 1]
out.append("---- top ----")
out += sorted(top)
for key in ("updater.ini", "凝紫客户端.exe", "凝紫客户端(主程序).exe", "使用说明.txt"):
    full = "凝紫客户端-完整版-v5/" + key
    if full in names:
        out.append("%s size=%d" % (key, z.getinfo(full).file_size))
    else:
        out.append("%s MISSING" % key)
out.append("has game/assets: %s" % any("/game/assets/" in n for n in names))
out.append("has game/xaero: %s" % any("/game/xaero/" in n for n in names))
out.append("has game/logs: %s" % any("/game/logs/" in n for n in names))
open(r"C:\大肥鱼\zipcheck.txt", "w", encoding="utf-8").write("\n".join(out))
print("OK")
