# 交接文档（给下一个 DSH / 管理员）

> 最后更新：2026-10-28 23:55（Asia/Shanghai）
> 服务器：`play.simpfun.cn:14039`（MC 26.3 / Fabric / 离线模式）
> 仓库：`https://github.com/Ningzi0606/nz-client`（public，main）
> 客户端清单版本：`20261028.2341`（v5.1）

---

## 0. 一句话现状

Windows 玩家双击 `凝紫客户端.exe` → 自动检查 GitHub 清单 → 增量更新 → 进游戏；
白名单按名字（EasyWhitelist）；登录 EasyAuth；皮肤 Quick Skin（服务端同步）；
Mac 玩家用独立包 + `.command` 脚本；发版双击 `一键发布.bat`。

**v5.1（2026-10-28 晚，清单 `20261028.2341`）**：修了「点启动游戏后永远卡在 `检查 mod N/18`」——
主程序 `UpdateMods()` 请求 Modrinth 时没有超时。现在所有网络请求 12 秒超时，
且 `game\mods` 里的 jar 数 ≥ 清单 mod 数时直接跳过联网检查（强制检查：`config.ini` 加 `modupdate=1`）。
排查玩家「进不去游戏」时先看 `launcher.log` 最后一行：停在 `玩家名: xxx` 就是老版本，让他更新一次即可。

---

## 1. 环境与访问

| 项 | 值 |
|---|---|
| GitHub 账号 | `Ningzi0606`（本机 git 凭据已缓存，`git push` 直接可用） |
| 仓库 | `github.com/Ningzi0606/nz-client`，main |
| 服务器面板 | `https://simpfun.cn/console/ins/892295`（简幻欢 V4，Edge 已登录） |
| 服务器容器路径 | `/home/container`（`mods/`、`config/`、`NZ WD/` 世界、`EasyAuth/`、`start.sh`） |
| 本机工作区 | `C:\大肥鱼\`（所有脚本、构建产物、文档） |
| 客户端目录 | `C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\`（已升级成 v5 结构） |
| Java（本机） | `C:\Python314` 是 Python；Java 用客户端自带 `runtime\bin\java.exe`（25.0.1） |

> 注意：DSH 自带 shell 在这台机器上起不来（`pwsh` 退出码 0xC0000142），
> 需要命令行时用 `open_application cmd` 打开 Git CMD 窗口，用 `computer` 工具敲命令。
> 中文输出会乱码，重要结果重定向到文件再用 `read` 读，或改用 ASCII 输出。

---

## 2. 服务器端现状

### 2.1 mods（`/home/container/mods`，12 个）

```
Chunky-Fabric-1.5.3.jar
architectury-fabric-22.0.5.jar      ← 新增（Quick Skin 依赖）
easyauth.jar                        ← 登录插件
easyauth 数据库：/home/container/EasyAuth/easyauth.db
easywhitelist-1.1.4.jar             ← 新增（名字白名单）
fabric-api-0.165.0+26.3.jar
ferritecore-9.0.0-fabric.jar
krypton-0.3.2.jar
lithium-fabric-0.26.2+mc26.3.jar
Quick Skin - Fabric - 26.3-3.1.1.jar ← 新增（皮肤）
skinrestorer-2.11.0+26.3-fabric.jar  ← 新增（皮肤命令）
spark-1.10.187-fabric.jar
```

### 2.2 启动脚本 `start.sh`

```
#!/bin/bash
cd /home/container; java -cp /home/container Migrate; java -cp /home/container Verify; echo $FINAL; exec java -Xmx7000M -jar fabric-server-mc.26.3-loader.0.20.1-launcher.1.1.2.jar nogui
```

- `Migrate`：把 whitelist/usercache/ops 里的正版 UUID 换成离线 UUID，并重命名 playerdata；
- `Verify`：体检（孤儿档、无档玩家、`whitelist stale uuid`）；
- 两者源码在容器根目录（`Migrate.java` / `Verify.java` / `Fix.java`），改完用 `java -cp /home/container Migrate` 再跑；
- **Migrate 每次启动都跑**，会重写 3 个 JSON、移动 500+ 数据文件；不需要就删掉这一行。

### 2.3 关键配置

- `server.properties`：`online-mode=false`、`white-list=true`、`enforce-whitelist=true`、`level-name=NZ WD`、`max-players=20`；
- `config/quickskin-server.json`：纹理上限 `maxTextureUploadKilobytes`（默认 16384 KiB），`shareAccountSkinWithVanillaClients`（默认 false）；
- `config/skinrestorer/`：皮肤缓存；`/skin set web` 走 MineSkin，无 API key（可选申请）。

### 2.4 常用服务器命令（面板控制台，**不需要打斜杠**）

```
easywhitelist add 名字 / remove 名字     加/删白名单（区分大小写，即时生效）
easyop 名字 / easydeop 名字              给/取消 OP
easyban 名字 / easypardon 名字           封禁/解封
list                                    在线玩家
say 内容                                广播
stop                                    关服（或面板右上角 ⓧ）
```

玩家侧（游戏内，带斜杠）：

```
/register 密码 密码     注册（EasyAuth）
/login 密码             登录
/autologin set 密码     自动登录（客户端 auto-login mod）
/skin set mojang <ID>   从正版名取皮肤
/skin set web classic "<图片URL>"
/skin refresh | /skin reset | /skin clear
```

---

## 3. 发布流程（改客户端后）

1. 改 `C:\Users\Administrator\Downloads\凝紫客户端-完整版-v4\` 里对应文件；
2. 双击 **`C:\大肥鱼\一键发布.bat`**（= `发布.py` 生成 `release/` → 同步进 `C:\大肥鱼\nz-client` → commit → push）；
3. 玩家下次打开客户端自动更新。

`发布.py` 只扫 `INCLUDE` 列表（主程序、logo、ico、manifest.json、说明书、CSL 配置、2 个皮肤 mod）；
**不要**把 `config.ini`（玩家名/密码）、`game/saves`、`options.txt`、`game/logs`、资源 zip 加进去。

- GitHub raw 有 30 秒~几分钟 CDN 缓存，push 完别拿旧客户端立刻验证；
- 单个文件别超 50MB；
- 回滚：`dist/` 换回旧文件 + `update.json` version 改新的，再 push。

---

## 4. 本机脚本清单（`C:\大肥鱼\`）

| 文件 | 作用 |
|---|---|
| `updater.cs` | 客户端更新器源码（C#，.NET Framework 4.x） |
| `installer.cs` | 老玩家一键升级器源码（内嵌 updater，自动找客户端目录） |
| `发布.py` | 生成 update.json + dist 镜像，检测变化/删除 |
| `一键发布.bat` | 发布 → 复制进仓库 → commit → push |
| `build_v5.py` | 清理 + 写说明书 + 打 v5 完整包（排除 assets/xaero/logs/saves） |
| `v5_out.py` | 校验 zip、复制到桌面、算 sha256 |
| `make_patch.py` / `make_mac_pack.py` / `build_mac.py` / `pack_mods.py` | 升级包 / Mac 模组包 / Mac 客户端 / 纯模组包 |
| `export_tutorial.py` | 教程转纯文本版到桌面 |
| `check_zip.py` | 检查 zip 顶层结构与体积 |

编译更新器/升级器（本机没装 .NET SDK，用的是系统自带 csc）：

```
C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe /nologo /target:winexe ^
  /out:"C:\大肥鱼\build\凝紫客户端.exe" ^
  /r:System.Windows.Forms.dll /r:System.Drawing.dll /r:System.Web.Extensions.dll ^
  "C:\大肥鱼\updater.cs"
```

升级器要带资源：

```
/resource:"C:\大肥鱼\build\凝紫客户端.exe",updater.bin /r:Microsoft.CSharp.dll
```

---

## 5. 清单格式（update.json）

```json
{
  "version": "20261028.1350",
  "base": "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/dist/",
  "files": {
    "使用说明.txt": {"sha256": "…", "size": 1323},
    "game/mods/Quick Skin - Fabric - 26.3-3.1.1.jar": {"sha256": "…", "size": 5515108}
  },
  "remove": []
}
```

- 路径相对客户端根目录；
- 更新器会 `Uri.EscapeDataString` 逐段编码（中文/空格文件名的 raw 链接已验证 200）；
- Mac 脚本复用同一份清单：`game/mods/...` → 实例 `.minecraft/mods`，`game/config/...` → `.minecraft/config`，其它放实例根。

---

## 6. 产物位置

| 产物 | 路径 |
|---|---|
| Windows 完整包 | `C:\大肥鱼\凝紫客户端-完整版-v5.zip`（661.8MB / 447 文件 / sha256 `3ead9ec4…`，桌面有副本） |
| 老玩家升级器 | `C:\大肥鱼\build\凝紫客户端v5升级器.exe`（仓库根也有） |
| Mac 客户端 | `C:\大肥鱼\凝紫客户端-Mac.zip`（33.6MB，桌面有副本） |
| Mac 教程 | `C:\大肥鱼\凝紫服-Mac玩家进服教程.md/.txt`（桌面有副本） |
| Windows 教程 | `C:\大肥鱼\凝紫服-进服教程-v5.md` |
| 纯模组包 | `C:\大肥鱼\凝紫v5-模组包.zip`（21 jar + 清单） |

---

## 7. 待办 / 风险

1. **Mac 包未真机验证**：`凝紫启动器.command` 用 `curl` / `shasum` / `osascript`，Prism 的 `--launch` 也要试；
   第一个 Mac 玩家跑完收 `启动器日志.txt`，再决定是否群发。
2. **服务端 mods 与客户端 mods 要同步**：Quick Skin / Architectury / fabric-api 两边版本必须一致，否则皮肤不同步。
3. `start.sh` 的 Migrate 建议择机删掉（现在每次启动都跑）。
4. 旧世界里的模组物品（旅行背包、深暗、农夫乐事）在 26.3 解码失败，尚未处理。
5. 备份：重要改动前先面板「备份」，或在容器里 `cp -r "NZ WD" "NZ WD.bak-$(date +%m%d)"`。
6. 面板文件管理器在服务器运行时只读，改 `start.sh`/`server.properties` 必须先关服。
