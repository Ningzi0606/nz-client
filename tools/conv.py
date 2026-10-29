import io
src = r"C:\大肥鱼\build.log"
dst = r"C:\大肥鱼\build_utf8.txt"
raw = open(src, "rb").read()
txt = raw.decode("gbk", "ignore")
open(dst, "w", encoding="utf-8").write(txt)
print(len(txt))
