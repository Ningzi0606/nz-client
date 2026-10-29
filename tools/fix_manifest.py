# -*- coding: utf-8 -*-
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
            print("REHASH", rel)
        files[rel] = new

    ordered = {k: v for k, v in files.items() if k != CORE}
    if CORE in files:
        ordered[CORE] = files[CORE]

    m["files"] = ordered
    m["version"] = datetime.datetime.now().strftime("%Y%m%d.%H%M")
    with open(UJ, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)

    print("changed:", changed)
    print("dropped:", dropped if dropped else "-")
    print("files:", len(ordered))
    print("last:", list(ordered)[-1] if ordered else "-")
    print("version:", m["version"])


if __name__ == "__main__":
    main()
