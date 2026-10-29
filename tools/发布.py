# -*- coding: utf-8 -*-
"""
凝紫客户端 发布工具
用法: python 发布.py [版本号]
  - 扫描客户端目录里需要下发的文件，生成 release/update.json 和 release/dist/ 镜像
  - 把 release/dist 和 update.json 提交到 GitHub 仓库即可
默认版本号 = 日期.时分（如 20261028.1315）
"""
import os, sys, json, hashlib, shutil, zipfile, datetime

ROOT = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
OUT = r"C:\大肥鱼\release"
BASE = "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/dist/"

# 需要随更新下发的文件（相对路径，支持通配）
INCLUDE = [
    "凝紫客户端(主程序).exe",
    "logo.png",
    "app.ico",
    "manifest.json",
    "使用说明.txt",
    "更新说明.txt",
    "game/config/CustomSkinLoader/CustomSkinLoader.json",
    "game/CustomSkinLoader/CustomSkinLoader.json",
    "game/mods/Quick Skin - Fabric - 26.3-3.1.1.jar",
    "game/mods/architectury-fabric-22.0.5.jar",
]

def match(rel):
    import fnmatch
    return any(fnmatch.fnmatch(rel, pat) for pat in INCLUDE)

def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            if match(rel):
                yield rel, full

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    version = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now().strftime("%Y%m%d.%H%M")
    update_json = os.path.join(OUT, "update.json")
    old = {}
    if os.path.exists(update_json):
        try:
            old = json.load(open(update_json, encoding="utf-8")).get("files", {})
        except Exception:
            old = {}

    files = {}
    changed = []
    for rel, full in walk():
        h = sha256(full)
        files[rel] = {"sha256": h, "size": os.path.getsize(full)}
        dst = os.path.join(OUT, "dist", rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if not os.path.exists(dst) or sha256(dst) != h:
            shutil.copy2(full, dst)
            changed.append(rel)

    removed = [p for p in old if p not in files]
    for p in removed:
        dst = os.path.join(OUT, "dist", p.replace("/", os.sep))
        if os.path.exists(dst):
            os.remove(dst)

    manifest = {"version": version, "base": BASE, "files": files, "remove": removed}
    os.makedirs(OUT, exist_ok=True)
    with open(update_json, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("版本:", version)
    print("文件数:", len(files))
    print("本次变化:", ", ".join(changed) if changed else "（无）")
    print("删除:", ", ".join(removed) if removed else "（无）")
    print("输出目录:", OUT)
    print("下一步: 把 release/update.json 和 release/dist/ 上传到 GitHub 仓库 main 分支")

if __name__ == "__main__":
    main()
