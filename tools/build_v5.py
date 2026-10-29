# -*- coding: utf-8 -*-
"""构建 v5 完整客户端包：清理 → 写文档 → 打包"""
import os, shutil, zipfile, time

SRC = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4"
OUT = r"C:\大肥鱼\凝紫客户端-完整版-v5.zip"
LOG = r"C:\大肥鱼\build_v5.txt"

lines = []
def log(s):
    lines.append(s)
    print(s)

# 1. 清理
targets = [
    r"game\mods\jei-26.3-fabric-31.17.0.94.jar",   # 重复 JEI，保留 .95
    r"game\logs",
    r"game\temp",
    r"game\crash-reports",
    ".clientver",
    "updater.log",
    "launcher.log",
    "error.log",
]
for t in targets:
    p = os.path.join(SRC, t)
    try:
        if os.path.isdir(p):
            shutil.rmtree(p)
            log("删除目录 " + t)
        elif os.path.exists(p):
            os.remove(p)
            log("删除文件 " + t)
    except Exception as e:
        log("清理失败 %s: %s" % (t, e))

# 2. 重置玩家名
with open(os.path.join(SRC, "config.ini"), "w", encoding="utf-8-sig") as f:
    f.write("name=\npass=\n")
log("重置 config.ini")

# 3. 文档
usem = """凝紫服务器 二周目 - 独立客户端 v5
====================================

一、怎么用
1. 解压整个文件夹（不要只解压 exe）
2. 双击 凝紫客户端.exe
3. 填玩家名（3-16 位字母/数字/下划线，这就是你的身份，定了别改）
4. 点「启动游戏」，会自动解压资源并直接进服

二、第一次进服（只需一次）
1. 进服后聊天栏输入：/register 你的密码 你的密码
2. 再输入：/login 你的密码
3. 想以后自动登录：/autologin set 你的密码

三、自动更新（v5 新增）
每次打开 凝紫客户端.exe，会先检查 GitHub 上的更新清单，
只下载变化的文件并校验，再启动游戏。
断网时会跳过更新直接进服，不影响玩。

四、皮肤（v5 已配好）
1. 打开 littleskin.cn 注册（邮箱即可）
2. 「角色管理」新建角色，名字 = 你的游戏名
3. 「皮肤库」上传皮肤 PNG（64x64）
4. 回游戏重进；没变化就删掉 game\\CustomSkinLoader\\caches 再开

五、进不去游戏？
- 提示 You are not white-listed → 把准确名字发给管理员加白名单
- 提示版本不符 → 别自己加模组，用群里发的完整客户端
- 启动器报错 → 把客户端目录里的 updater.log / launcher.log 发给管理员
"""

update = """v5（2026-10-28）
====================================
1. 新增自动更新器：打开客户端先检查 GitHub 清单，只下载变了的文件，
   校验 sha256 后覆盖，然后启动游戏。以后改配置/改皮肤/改界面，不用再重下 600MB。
2. 修复皮肤：优先从 LittleSkin 拉皮肤（同名角色），不再被正版撞名顶掉。
3. 清理重复的 JEI（原来多装了一个版本）。
4. 老玩家升级说明：原来的启动器已改名为 凝紫客户端(主程序).exe，
   新的 凝紫客户端.exe 是更新器，桌面快捷方式照旧能用。

v4（2026-10-28 凌晨）
- 修复界面比例（125%/150%/200% 缩放不再截断）
- 首次启动自动创建桌面快捷方式
- 日志：launcher.log / java-launcher.log / error.log
"""
with open(os.path.join(SRC, "使用说明.txt"), "w", encoding="utf-8") as f:
    f.write(usem)
with open(os.path.join(SRC, "更新说明.txt"), "w", encoding="utf-8") as f:
    f.write(update)
log("写入说明书")

# 4. 打包
if os.path.exists(OUT):
    os.remove(OUT)
t0 = time.time()
count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
    for dirpath, dirnames, filenames in os.walk(SRC):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, SRC)
            low = rel.lower()
            skip = ("game\\saves", "game\\logs", "game\\temp", "game\\crash-reports",
                    "game\\assets", "game\\xaero", "game\\journeymap",
                    "game\\customskinloader\\caches", "game\\downloads")
            if any(low.startswith(s) for s in skip):
                continue
            try:
                z.write(full, os.path.join("凝紫客户端-完整版-v5", rel))
            except Exception as e:
                log("跳过（无法读取）%s : %s" % (rel, e))
            count += 1
            if count % 1000 == 0:
                log("已打包 %d 个文件..." % count)
log("完成：%s  %.1f MB  %d 个文件  用时 %.0f 秒" % (OUT, os.path.getsize(OUT) / 1048576.0, count, time.time() - t0))

open(LOG, "w", encoding="utf-8").write("\n".join(lines))
print("DONE")
