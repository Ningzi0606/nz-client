# 凝紫客户端 · 自动更新发布说明

> 仓库：https://github.com/Ningzi0606/nz-client （public，main 分支）
> 清单地址：`https://raw.githubusercontent.com/Ningzi0606/nz-client/main/update.json`
> 文件镜像：`https://raw.githubusercontent.com/Ningzi0606/nz-client/main/dist/`

## 一、它是怎么跑的

```
玩家双击 凝紫客户端.exe（更新器，约 30KB）
        │
        ├─ 读 updater.ini 里的 url=
        ├─ GET update.json，比较 version 和本地 .clientver
        ├─ 有差异 → 逐个文件比对 sha256 → 只下载变了的 → 校验 → 覆盖
        ├─ 写 .clientver
        └─ 启动 凝紫客户端(主程序).exe（原来的启动器，界面/登录/启动游戏都不变）
```

- 断网 / GitHub 抽风 → 记一行 `updater.log`，然后照常启动游戏，不会卡住玩家；
- 更新器自己不在清单里（运行中的 exe 无法覆盖），要改更新器就得发新包；
- 主程序启动后仍会自己做 mod 更新（Modrinth）和资源解压，互不影响。

## 二、清单格式

`update.json`：

```json
{
  "version": "20261028.1320",
  "base": "https://raw.githubusercontent.com/Ningzi0606/nz-client/main/dist/",
  "files": {
    "使用说明.txt": { "sha256": "…", "size": 1001 },
    "game/config/CustomSkinLoader/CustomSkinLoader.json": { "sha256": "…", "size": 640 }
  },
  "remove": []
}
```

- `version`：随便什么字符串，变了就会触发检查；
- `files`：相对客户端根目录的路径 → sha256 + 大小；
- `remove`：要从玩家机器上删掉的文件。

## 三、发版（三步）

1. 改好客户端目录里的文件（只发改动的那几个）；
2. 双击 `C:\大肥鱼\一键发布.bat`（= 跑 `发布.py` → 生成 release/ → 复制进本地仓库 → commit → push）；
3. 完事。玩家下次打开客户端自动更新。

`发布.py` 只扫 `INCLUDE` 里列的文件：

```
凝紫客户端(主程序).exe, logo.png, app.ico, manifest.json,
使用说明.txt, 更新说明.txt,
game/config/CustomSkinLoader/CustomSkinLoader.json,
game/CustomSkinLoader/CustomSkinLoader.json,
game/mods/Quick Skin - Fabric - 26.3-3.1.1.jar,
game/mods/architectury-fabric-22.0.5.jar
```

要加文件就往 `INCLUDE` 里加一行；**不要**把 `config.ini`（玩家名/密码）、`game/saves`、`game/options.txt`、`game/logs`、`游戏资源-assets.zip` 放进去。

## 四、注意

- GitHub raw 有 CDN 缓存（几秒到几分钟），刚 push 完立刻测可能还是旧清单，正常；
- 单个文件别超过 ~50MB（raw 限制 100MB，仓库也不该塞大文件）；
- 回滚：把 `dist/` 里的文件换回旧版、`update.json` 的 version 改一个新的，再 push；
- 玩家端排错看 `客户端目录\updater.log`，只有几行，一看就懂。

## 五、首次升级（老玩家）

v4 的启动器没有可用的更新逻辑，所以老玩家需要装一次 `凝紫客户端-自动更新升级包.zip`：

解压到客户端目录 → 双击 `一键升级.bat` → 它把旧启动器改名成 `凝紫客户端(主程序).exe`，再把更新器放到 `凝紫客户端.exe`。

之后就不用再发大包了。

---

## 相关文档

- `CHANGELOG.md` — v5 更新日志（这次做了什么、为什么这么做）
- `HANDOVER.md` — 交接文档（环境、路径、服务器命令、发布流程、待办）
