import os, json, io

root = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
out = []

out.append("=== dir /a ===")
for n in sorted(os.listdir(root)):
    p = os.path.join(root, n)
    try:
        st = os.stat(p)
        out.append("%-40s %10d %s" % (n, st.st_size, "DIR" if os.path.isdir(p) else "FILE"))
    except Exception as e:
        out.append("%s ERR %s" % (n, e))

def dump(name, maxlen=4000):
    p = os.path.join(root, name)
    out.append("\n=== %s ===" % name)
    if not os.path.exists(p):
        out.append("(missing)")
        return
    raw = open(p, "rb").read()
    for enc in ("utf-8-sig", "utf-8", "gbk", "latin1"):
        try:
            t = raw.decode(enc)
            out.append("[enc=%s len=%d]" % (enc, len(raw)))
            break
        except Exception:
            continue
    out.append(t[:maxlen])

for n in ("config.ini", ".clientver", "manifest.json", "fabric-server-launcher.properties"):
    dump(n)

p = os.path.join(root, "launcher.log")
if os.path.exists(p):
    raw = open(p, "rb").read()[-6000:]
    for enc in ("utf-8", "gbk", "latin1"):
        try:
            t = raw.decode(enc)
            break
        except Exception:
            continue
    out.append("\n=== launcher.log tail ===")
    out.append(t)

open(r"C:\大肥鱼\clientinfo.txt", "w", encoding="utf-8").write("\n".join(out))
print("OK")
