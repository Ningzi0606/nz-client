import re
p = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\凝紫客户端.exe"
d = open(p, "rb").read()
seen = []
for m in re.finditer(rb"(?:[\x20-\x7e]\x00){5,400}", d):
    s = m.group().decode("utf-16le", "ignore")
    if s not in seen:
        seen.append(s)
open(r"C:\大肥鱼\strings.txt", "w", encoding="utf-8").write("\n".join(seen))
print("OK", len(seen))
