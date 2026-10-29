# -*- coding: utf-8 -*-
"""
修清单：按 dist 里“实际会被下载到的字节”重新算 sha256，并让主程序排在最后。
解决两个问题：
  1) 清单哈希和线上文件不一致 -> 客户端报“校验失败”后整轮中断
  2) 主程序排在 mods 前面 -> 主程序更新失败时 mods 永远轮不到
"""
import json, hashlib, os, datetime

REPO = r"C:\大肥鱼\nz-client"
DIST = os.path.join(REPO, "dist")
UJ = os.path.join(REPO, "update.json")
CORE = "凝紫客户端(主程序).exe"


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main():
    m = json.load(open(UJ, encoding="utf-8"))
    files = m.get("files", {})

    dropped, changed = [], 0
    for rel in list(files):
        p = os.path.join(DIST, rel.replace("/", os.sep))
        if not os.path.exists(p):
            dropped.append(rel)
            files.pop(rel)
            continue
        new = {"sha256": sha256(p), "size": os.path.getsize(p)}
        old = files.get(rel, {})
        if old.get("sha256") != new["sha256"] or old.get("size") != new["size"]:
            changed += 1
        files[rel] = new

    ordered = {k: v for k, v in files.items() if k != CORE}
    if CORE in files:
        ordered[CORE] = files[CORE]

    m["files"] = ordered
    m["version"] = datetime.datetime.now().strftime("%Y%m%d.%H%M")
    with open(UJ, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

    print("修正哈希:", changed)
    print("缺失丢弃:", dropped if dropped else "（无）")
    print("文件数:", len(ordered))
    print("最后一项:", list(ordered)[-1] if ordered else "-")
    print("新版本:", m["version"])


if __name__ == "__main__":
    main()
