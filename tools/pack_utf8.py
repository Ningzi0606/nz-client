# -*- coding: utf-8 -*-
import os
import zipfile

SRC = r"C:\Users\Administrator\Desktop\凝紫客户端-完整版-v5\凝紫客户端-完整版-v5"
OUT = r"C:\大肥鱼\凝紫启动器-v5.3.zip"


def main():
    if os.path.exists(OUT):
        os.remove(OUT)
    n = 0
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
        for root, dirs, files in os.walk(SRC):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, SRC)
                z.write(full, rel)
                n += 1
                if n % 200 == 0:
                    print("packed", n, flush=True)
    print("DONE", n, "files", os.path.getsize(OUT) // 1024, "KB")


main()
