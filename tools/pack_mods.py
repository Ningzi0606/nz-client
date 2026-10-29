# -*- coding: utf-8 -*-
import os, zipfile, shutil

SRC = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\game\mods"
OUT = r"C:\大肥鱼\凝紫v5-模组包.zip"
DESK = r"C:\Users\Administrator\Desktop"

jars = sorted(f for f in os.listdir(SRC) if f.lower().endswith(".jar"))

listing = ["凝紫服 v5 客户端模组清单（Minecraft 26.3 / Fabric 0.19.5）", "=" * 52]
for i, f in enumerate(jars, 1):
    size = os.path.getsize(os.path.join(SRC, f))
    listing.append("%2d. %s  (%.2f MB)" % (i, f, size / 1048576.0))
listing.append("")
listing.append("用法：把 mods 里的 jar 全部放进 .minecraft/mods（需要 Fabric 环境）")
listing.append("服务器：play.simpfun.cn:14039")

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for f in jars:
        z.write(os.path.join(SRC, f), "mods/" + f)
    z.writestr("模组清单.txt", "\n".join(listing))

shutil.copy2(OUT, os.path.join(DESK, "凝紫v5-模组包.zip"))
print("OK", OUT, "%.1f MB" % (os.path.getsize(OUT) / 1048576.0), len(jars), "mods")
