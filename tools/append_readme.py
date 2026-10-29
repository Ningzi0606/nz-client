p = r"C:\大肥鱼\nz-client\README.md"
t = open(p, encoding="utf-8").read()
add = "\n\n---\n\n## 相关文档\n\n- `CHANGELOG.md` — v5 更新日志（这次做了什么、为什么这么做）\n- `HANDOVER.md` — 交接文档（环境、路径、服务器命令、发布流程、待办）\n"
if "相关文档" not in t:
    t = t.rstrip() + add
    open(p, "w", encoding="utf-8").write(t)
    print("appended")
else:
    print("exists")
