# -*- coding: utf-8 -*-
"""生成 macOS 版客户端：Prism 实例 + 双击启动器（含自动更新）"""
import os, shutil, zipfile, stat

WS = r"C:\大肥鱼"
SRC_GAME = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\game"
OUT_DIR = os.path.join(WS, "mac-build", "凝紫客户端-Mac")
ZIP_PATH = os.path.join(WS, "凝紫客户端-Mac.zip")
INST = "凝紫服"

shutil.rmtree(os.path.join(WS, "mac-build"), ignore_errors=True)
os.makedirs(os.path.join(OUT_DIR, "实例", INST, ".minecraft", "mods"))
os.makedirs(os.path.join(OUT_DIR, "实例", INST, ".minecraft", "config"))

# mods
n = 0
for fn in sorted(os.listdir(os.path.join(SRC_GAME, "mods"))):
    if fn.lower().endswith(".jar"):
        shutil.copy2(os.path.join(SRC_GAME, "mods", fn),
                     os.path.join(OUT_DIR, "实例", INST, ".minecraft", "mods", fn))
        n += 1

# 皮肤配置（可选）
csl = os.path.join(SRC_GAME, "config", "CustomSkinLoader", "CustomSkinLoader.json")
if os.path.exists(csl):
    d = os.path.join(OUT_DIR, "实例", INST, ".minecraft", "config", "CustomSkinLoader")
    os.makedirs(d, exist_ok=True)
    shutil.copy2(csl, os.path.join(d, "CustomSkinLoader.json"))

with open(os.path.join(OUT_DIR, "实例", INST, "instance.cfg"), "w", encoding="utf-8", newline="\n") as f:
    f.write("InstanceType=OneSix\nname=%s\niconKey=default\nJavaPath=\nMaxMemAlloc=4096\nMinMemAlloc=1024\n" % INST)

import json
pack = {
    "formatVersion": 1,
    "components": [
        {"uid": "net.minecraft", "version": "26.3", "important": True},
        {"uid": "net.fabricmc.fabric-loader", "version": "0.19.5"},
    ],
}
with open(os.path.join(OUT_DIR, "实例", INST, "mmc-pack.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(pack, f, ensure_ascii=False, indent=2)

JXA = r'''
ObjC.import("Foundation");
function read(p){ return $.NSString.stringWithContentsOfFileEncodingError(p, $.NSUTF8StringEncoding, null).js; }
function run(argv){
  var raw = read(argv[0]);
  var m = JSON.parse(raw);
  var base = m.base || "";
  var lines = [];
  for (var k in m.files) {
    var segs = k.split("/").map(encodeURIComponent);
    lines.push(k + "\t" + m.files[k].sha256 + "\t" + base + segs.join("/"));
  }
  var rm = (m.remove || []).join("\n");
  return m.version + "\n" + lines.join("\n") + "\n@@REMOVE@@\n" + rm;
}
'''

LAUNCHER = r'''#!/bin/bash
# 凝紫服 macOS 启动器：检查更新 -> 同步 mod -> 启动 Prism
set -u
cd "$(dirname "$0")" || exit 1
LOG="$PWD/启动器日志.txt"
exec >>"$LOG" 2>&1
echo "===== $(date) ====="

URL="https://raw.githubusercontent.com/Ningzi0606/nz-client/main/update.json"
INST_NAME="凝紫服"
PRISM_SUPPORT="$HOME/Library/Application Support/PrismLauncher"
INST_DIR="$PRISM_SUPPORT/instances/$INST_NAME"
SHIP_INST="$PWD/实例/$INST_NAME"

# 1. 首次运行：把实例装进 Prism
if [ ! -d "$INST_DIR" ]; then
  echo "首次运行，安装实例到 $INST_DIR"
  mkdir -p "$PRISM_SUPPORT/instances"
  cp -R "$SHIP_INST" "$INST_DIR" || { echo "复制实例失败"; osascript -e 'display dialog "安装实例失败，请把日志发给管理" buttons {"好"}'; exit 1; }
fi

MC="$INST_DIR/.minecraft"
VER_FILE="$INST_DIR/.clientver"

# 2. 拉清单
TMP="$(mktemp -t nz)"
if ! curl -fsSL --max-time 20 "$URL" -o "$TMP"; then
  echo "拉取清单失败，跳过更新"
  rm -f "$TMP"
else
  JXA_FILE="$PWD/.parse.js"
  cat > "$JXA_FILE" <<'JXAEOF'
__JXA__
JXAEOF
  PARSED="$(osascript -l JavaScript "$JXA_FILE" "$TMP" 2>>"$LOG")"
  rm -f "$TMP"
  if [ -z "$PARSED" ]; then
    echo "解析清单失败，跳过更新"
  else
    VERSION="$(printf '%s\n' "$PARSED" | head -n1)"
    LOCAL="$(cat "$VER_FILE" 2>/dev/null || true)"
    echo "本地 [$LOCAL] -> 远端 [$VERSION]"
    if [ "$VERSION" != "$LOCAL" ]; then
      printf '%s\n' "$PARSED" | tail -n +2 | while IFS=$'\t' read -r rel sha url; do
        [ "$rel" = "@@REMOVE@@" ] && break
        [ -z "$rel" ] && continue
        case "$rel" in
          game/*) target="$MC/${rel#game/}" ;;
          *) target="$INST_DIR/$rel" ;;
        esac
        need=1
        if [ -f "$target" ]; then
          have="$(shasum -a 256 "$target" | awk '{print $1}')"
          [ "$have" = "$sha" ] && need=0
        fi
        if [ "$need" = "1" ]; then
          echo "下载 $rel"
          mkdir -p "$(dirname "$target")"
          if curl -fsSL --max-time 120 "$url" -o "$target.download"; then
            if [ "$(shasum -a 256 "$target.download" | awk '{print $1}')" = "$sha" ]; then
              mv -f "$target.download" "$target"
            else
              echo "校验失败 $rel"; rm -f "$target.download"
            fi
          else
            echo "下载失败 $rel"
          fi
        fi
      done
      printf '%s' "$VERSION" > "$VER_FILE"
      echo "更新完成：$VERSION"
    else
      echo "已是最新版本"
    fi
  fi
fi

# 3. 启动 Prism
PRISM_BIN="/Applications/Prism Launcher.app/Contents/MacOS/prismlauncher"
if [ -x "$PRISM_BIN" ]; then
  echo "启动 Prism 实例：$INST_NAME"
  "$PRISM_BIN" --launch "$INST_NAME" &
else
  echo "未找到 Prism，改为打开应用"
  open -a "Prism Launcher"
fi
exit 0
'''
LAUNCHER = LAUNCHER.replace("__JXA__", JXA.strip())

cmd_path = os.path.join(OUT_DIR, "凝紫启动器.command")
with open(cmd_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(LAUNCHER)
os.chmod(cmd_path, 0o755)

README = """凝紫服 · macOS 客户端
================================
1. 安装 Prism Launcher（https://prismlauncher.org/download/macOS）
   第一次打开会要求选择 Java：装一个 Java 25（adoptium.net，Apple 芯片选 aarch64，Intel 选 x64）
2. 双击「凝紫启动器.command」
   - 如果提示无法打开：右键 → 打开 → 仍要打开；或终端执行 chmod +x 凝紫启动器.command
   - 首次会把「凝紫服」实例装进 Prism
3. 之后每次想玩，双击这个 .command 就行：
   它会先检查更新（只下变了的 mod/配置），再自动启动游戏
4. 进服后：/register 密码 密码 → /login 密码 → /autologin set 密码

说明
- 实例名：凝紫服（服务器 play.simpfun.cn:14039 已写进实例）
- 皮肤：包内已带 Quick Skin，进游戏按 Esc → Change Skin
- 日志：启动器日志.txt（有问题发给管理）
- 想手动管：Prism 里能看到「凝紫服」实例，右键可编辑
"""
with open(os.path.join(OUT_DIR, "安装说明.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(README)

# 打包（保留 .command 可执行权限）
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for dirpath, _, files in os.walk(OUT_DIR):
        for fn in files:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, OUT_DIR)
            info = zipfile.ZipInfo(os.path.join("凝紫客户端-Mac", rel))
            info.compress_type = zipfile.ZIP_DEFLATED
            mode = 0o755 if fn.endswith(".command") else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            with open(full, "rb") as f:
                z.writestr(info, f.read())

print("OK", ZIP_PATH, "%.1f MB" % (os.path.getsize(ZIP_PATH) / 1048576.0), n, "mods")
