# -*- coding: utf-8 -*-
import os, zipfile

SRC = r"C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\game"
OUT = r"C:\大肥鱼\凝紫-Mac模组包.zip"

README = """凝紫服 · Mac 玩家模组包
================================
这份包给 macOS 玩家用（Windows 玩家请直接用凝紫客户端，别用这个）。

一、准备
1. 装 Java 25（Apple Silicon 选 arm64 版，Intel 选 x64）：
   https://adoptium.net/temurin/releases/?version=25
2. 下载 HMCL 启动器（跨平台 jar）：
   https://hmcl.huangyuhui.net/download
   双击 hmcl.jar 打开（或 java -jar hmcl.jar）

二、装游戏
1. HMCL 左下「版本列表」→ 安装新游戏
2. 游戏版本选 26.3
3. 安装时勾选 Fabric，Loader 选 0.19.5 或更新
4. 装好后进「游戏目录」

三、放模组
1. 把本压缩包里的 mods 文件夹整个放到 游戏目录/.minecraft/mods
   （已存在就把里面的 jar 全复制进去）
2. 把 config 里的 CustomSkinLoader 一并复制到 .minecraft/config/（可选，皮肤以 Quick Skin 为准）

四、启动进服
1. HMCL 里「账户」用离线登录，用户名填你报给管理的名字（大小写一致）
2. 启动游戏 → 多人游戏 → 添加服务器 play.simpfun.cn:14039
3. 第一次进服：
   /register 密码 密码
   /login 密码
   /autologin set 密码   （可选，自动登录）

五、皮肤
进服后按 Esc → Change Skin → 导入 64x64 PNG / 选模型 / 选披风。
必须装 Quick Skin（本包已带），否则看不到别人的皮肤。

六、注意
- 名字就是身份，改名=换号，背包会丢
- 没加白名单会被踢，把准确名字发管理
- Mac 没有自动更新，版本更新时重新拿一份这个包，覆盖 mods 即可
"""

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.exists(OUT):
    os.remove(OUT)

count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    mods = os.path.join(SRC, "mods")
    for fn in sorted(os.listdir(mods)):
        if fn.lower().endswith(".jar"):
            z.write(os.path.join(mods, fn), "mods/" + fn)
            count += 1
    csl = os.path.join(SRC, "config", "CustomSkinLoader", "CustomSkinLoader.json")
    if os.path.exists(csl):
        z.write(csl, "config/CustomSkinLoader/CustomSkinLoader.json")
    z.writestr("Mac进服说明.txt", README)

print("OK", OUT, "%.1f MB" % (os.path.getsize(OUT) / 1048576.0), count, "mods")
