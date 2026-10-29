import re

p = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\凝紫客户端.exe"
d = open(p, "rb").read()
out = []

def add(title, items, limit=200):
    out.append("==== %s (%d) ====" % (title, len(items)))
    for s in items[:limit]:
        out.append(s)

# UTF-16LE strings
u16 = set()
for m in re.finditer(rb"(?:[\x20-\x7e]\x00){4,200}", d):
    s = m.group().decode("utf-16le", "ignore")
    u16.add(s)

urls = sorted({s for s in u16 if "http" in s.lower() or "github" in s.lower() or ".json" in s.lower()})
add("urls/json", urls)

keys = ("update", "version", "manifest", "repo", "client", "mods", "download", "hash", "sha", "patch")
hits = sorted({s for s in u16 if len(s) < 120 and any(k in s.lower() for k in keys)})
add("keywords", hits)

# assembly / framework hints
hints = sorted({s for s in u16 if "System." in s or "netframework" in s.lower() or "netcore" in s.lower()})
add("assembly", hints, 60)

open(r"C:\大肥鱼\scan2.txt", "w", encoding="utf-8").write("\n".join(out))
print("OK", len(u16), len(urls))
