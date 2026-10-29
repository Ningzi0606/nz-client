# v5 / v5.1 更新日志

> 2026-10-28｜凝紫服（Minecraft 26.3 / Fabric）
> 服务器：`play.simpfun.cn:14039`｜客户端清单版本：`20261028.2341`（v5.1）

---

## 零、v5.1（2026-10-28 晚）：修「启动卡在 检查 mod N/18」

**症状**：点「启动游戏」后进度条停在 `检查 mod 10/18`，一直不动，游戏永远起不来；
关掉重开还是一样。日志特征：`launcher.log` 最后一行是 `玩家名: xxx` 就没了，
`game\java-launcher.log` 的时间戳不更新（说明 java 根本没启动过）。

**原因**：主程序（`Launcher.cs` 的 `UpdateMods()`）在启动游戏前，会拿 `manifest.json` 里的 18 个 mod
逐个请求 `api.modrinth.com`，用的是 `new WebClient()`、**没有设任何超时**。
实测查到第 10 个左右时那次 HTTPS 请求不再返回（TCP 没断、就是不回数据），WebClient 就一直等着——
后面的「解压游戏资源」「启动 java」永远轮不到。更新器本身没问题，锅在主程序（v5 里它是“一行没改”的原启动器）。

**处理**（只动主程序，更新器 / 清单格式 / 其余文件都不变）：

1. 新增 `TimeoutWebClient`：连接、读取各 12 秒超时；7 处 `new WebClient()` 全部替换，
   网络不响应就直接放弃，不再无限挂住；
2. `game\mods` 里的 jar 数 ≥ 清单里的 mod 数时，直接跳过联网检查；
   想强制检查一次：`config.ini` 里加一行 `modupdate=1`。

**验证**：同机复现 → 打补丁 → 日志变成
`mod 已齐全（20 个，清单 18 个），跳过联网检查` → `发现资源包，开始解压` → `正在启动 Minecraft…` → 正常进服。
并且拿旧 v5 客户端真跑了一次更新：`updater.log` 记录
`已更新 凝紫客户端(主程序).exe (272896 字节)`、`更新完成，版本 20261028.2341`，主程序 sha256 = `73ed457b…`。

> 玩家侧不用做任何事：下次打开 `凝紫客户端.exe` 会自动换掉主程序。

---

## 一、客户端：新增自动更新器

**问题**：v4 客户端自带的"自更新"是残的——实测只会拉清单、比版本、写 `.clientver`、按 `remove` 删文件，
**从不下载 `files` 里的任何文件**（本地起 HTTP 服务器抓包验证，换几种清单写法都一样）。

**方案**：新写一个 30KB 的更新器，顶替 `凝紫客户端.exe` 作为入口：

```
玩家双击 凝紫客户端.exe（更新器）
  → 读 updater.ini 的 url=
  → GET update.json（GitHub raw）
  → 逐文件比对 sha256
  → 只下载变化的 → 校验 → 覆盖
  → 启动 凝紫客户端(主程序).exe（原启动器，界面/登录不变）
```

- 原启动器改名为 `凝紫客户端(主程序).exe`，一行没改；
- 断网 / GitHub 抽风：记一行 `updater.log`，照常启动游戏，不阻塞；
- 修了一个 .NET 的坑：`WebRequest` 连 GitHub 报 `未能创建 SSL/TLS 安全通道`，改为显式 TLS1.2/1.3 + 关闭代理 + 证书回调；
- 更新器自身不在清单里（运行中的 exe 覆盖不了自己），要改更新器得单独发包。

**老玩家过渡**：`凝紫客户端v5升级器.exe`（20KB）双击即完成改名 + 装更新器；实测通过。

---

## 二、白名单：改成按名字判定

**问题**：离线服里 `/whitelist add` 会先去 Mojang 查正版档案，名字在正版库存在时会把**正版 UUID** 写进白名单，
玩家用离线 UUID 登录时对不上，直接被踢。实测 `dsh_test_001` 触发 404 回退离线 UUID 才成功。

**处理**：

1. 关服跑 `Migrate` 把残留的正版 UUID 全部换成离线 UUID（`Verify` 的 `whitelist stale uuid` 从 3 归 0）；
2. 服务端装 **EasyWhitelist 1.1.4**，白名单/OP/封禁全部改成**按名字**判定，`easywhitelist add 名字` 立即生效，不用重启；
3. `start.sh` 里目前仍保留 Migrate（每次启动自动纠偏），可留可删。

---

## 三、皮肤：Quick Skin + SkinRestorer（服务端同步）

**问题**：离线模式协议上没有皮肤数据，客户端请求 Mojang 会话服务器失败（日志里 `Connection reset`），
结果要么默认皮肤，要么撞正版名显示别人的皮肤。

**采用方案（C）**：

- 服务端：**SkinRestorer 2.11.0**（命令设皮肤，所有人可见）+ **Quick Skin 3.1.1** + **Architectury 22.0.5**（图形界面 + 服务端同步）；
- 客户端：同样三个 mod（fabric-api 已有）；
- 玩家：游戏内 **Esc → Change Skin**，导入本地 PNG / 拖拽 / 切 Classic·Slim / 换披风，服务端同步给别人；
- 旧的 CustomSkinLoader 保留（LittleSkin 优先），但皮肤以 Quick Skin 为准。

> 为什么不自己写：Fabric Loom/Gradle 工具链 + 26.3 映射从零搭，周期长风险高；Quick Skin 功能更全。

---

## 四、v5 完整包

- 文件：`凝紫客户端-完整版-v5.zip`
- 大小：**661.8 MB / 447 个文件**，完整性校验 OK
- SHA-256：`3ead9ec47bb6757af5f61dd9ead919fd764b71a9259b0c5ca09c866914bfd25b`
- 内容：更新器 + 原启动器 + 21 个 mod（含 Quick Skin）+ 资源 zip + 内置 Java 25 + 新说明书
- 排除：游戏存档、Xaero 地图缓存、日志、`game/assets`（首次启动自动解压）

---

## 五、仓库在发什么

`Ningzi0606/nz-client`（main）：

| 文件 | 说明 |
|---|---|
| `update.json` | 更新清单（version / base / files{sha256,size} / remove） |
| `dist/**` | 清单里文件的镜像（主程序、logo、说明书、CSL 配置、2 个皮肤 mod） |
| `v5升级器.exe` | 老玩家一次性升级工具 |
| `README.md` | 发布说明 |
| `CHANGELOG.md` | 本文件 |
| `HANDOVER.md` | 交接文档（给下一个 DSH / 管理员） |

当前清单版本 `20261028.1350`，10 个文件，含
`game/mods/Quick Skin - Fabric - 26.3-3.1.1.jar`、`game/mods/architectury-fabric-22.0.5.jar`。

---

## 六、文档与产物

| 产物 | 位置 |
|---|---|
| Windows 完整包 | `C:\大肥鱼\凝紫客户端-完整版-v5.zip`（桌面有副本） |
| 老玩家升级器 | `C:\大肥鱼\build\凝紫客户端v5升级器.exe`（仓库里也有） |
| Mac 客户端 | `C:\大肥鱼\凝紫客户端-Mac.zip`（33.6MB，桌面有副本） |
| Mac 教程 | `凝紫服-Mac玩家进服教程.md/.txt`（桌面） |
| Windows 教程 | `凝紫服-进服教程-v5.md` |
| 模组包 | `凝紫v5-模组包.zip`（21 个 jar + 清单，桌面） |

---

## 七、已知问题 / 待办

- [ ] **Mac 包未真机验证**：`凝紫启动器.command` 依赖 `curl` / `shasum` / `osascript`，Prism 的 `--launch` 参数也要实测；第一个 Mac 玩家跑完收集 `启动器日志.txt`；
- [ ] `start.sh` 里 Migrate 每次启动都跑（会重写 whitelist/usercache/ops），可择机删掉；
- [ ] `SkinRestorer` 的 `/skin set web` 走 MineSkin，没有 API key（有频率限制），需要的话去 account.mineskin.org 申请；
- [ ] 服务端 `config/quickskin-server.json` 可调纹理上限、是否把皮肤共享给原版客户端（`shareAccountSkinWithVanillaClients`）；
- [ ] 旧存档里的模组物品（旅行背包/深暗/农夫乐事）在 26.3 无法解码，属于内容模组缺失，尚未清理。
