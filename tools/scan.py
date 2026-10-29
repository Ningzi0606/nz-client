import re, sys, json, os

p = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\凝紫客户端.exe"
d = open(p, "rb").read()
out = []
out.append("size=%d bytes" % len(d))
# PE machine / subsystem
if d[:2] == b"MZ":
    e_lfanew = int.from_bytes(d[0x3C:0x40], "little")
    if d[e_lfanew:e_lfanew+4] == b"PE\0\0":
        machine = int.from_bytes(d[e_lfanew+4:e_lfanew+6], "little")
        out.append("PE machine=0x%04x" % machine)

strs = set()
for m in re.finditer(rb"[\x20-\x7e]{6,200}", d):
    s = m.group().decode("latin1")
    if any(k in s.lower() for k in ("github", "raw.githubusercontent", "manifest", "update", "http://", "https://", "version", ".json")):
        strs.add(s)

out.append("---- interesting strings ----")
for s in sorted(strs)[:300]:
    out.append(s)

open(r"C:\大肥鱼\scan.txt", "w", encoding="utf-8").write("\n".join(out))
print("OK", len(strs))
