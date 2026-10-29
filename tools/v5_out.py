import zipfile, os, shutil, hashlib

SRC = r"C:\大肥鱼\凝紫客户端-完整版-v5.zip"
DST = r"C:\Users\Administrator\Desktop\凝紫客户端-完整版-v5.zip"

out = []
with zipfile.ZipFile(SRC) as z:
    bad = z.testzip()
    out.append("zip entries: %d" % len(z.namelist()))
    out.append("integrity: %s" % ("OK" if bad is None else ("BAD: " + bad)))

if os.path.exists(DST):
    os.remove(DST)
shutil.copy2(SRC, DST)
out.append("copied to: %s" % DST)
out.append("size: %.1f MB" % (os.path.getsize(DST) / 1048576.0))

h = hashlib.sha256()
with open(DST, "rb") as f:
    for chunk in iter(lambda: f.read(4 << 20), b""):
        h.update(chunk)
out.append("sha256: %s" % h.hexdigest())

open(r"C:\大肥鱼\v5_out.txt", "w", encoding="utf-8").write("\n".join(out))
print("DONE")
