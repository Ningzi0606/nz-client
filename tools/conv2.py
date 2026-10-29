raw = open(r"C:\大肥鱼\env.txt", "rb").read()
for enc in ("utf-8", "gbk", "latin1"):
    try:
        t = raw.decode(enc)
        break
    except Exception:
        t = None
open(r"C:\大肥鱼\env_utf8.txt", "w", encoding="utf-8").write(t or "")
print("OK")
