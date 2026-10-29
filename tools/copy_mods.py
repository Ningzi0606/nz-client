import os, shutil

ROOT = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\game\mods"
src = r"C:\Users\Administrator\Downloads"
files = ["Quick Skin - Fabric - 26.3-3.1.1.jar", "architectury-fabric-22.0.5.jar"]
out = []
for f in files:
    s = os.path.join(src, f)
    d = os.path.join(ROOT, f)
    shutil.copy2(s, d)
    out.append("%s -> %d bytes" % (f, os.path.getsize(d)))
out.append("mods count: %d" % len([x for x in os.listdir(ROOT) if x.endswith(".jar")]))
open(r"C:\大肥鱼\copymods.txt", "w", encoding="utf-8").write("\n".join(out))
print("DONE")
