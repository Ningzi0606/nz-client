# 凝紫客户端 更新日志（v5 → v5.3）

> 凝紫服（Minecraft 26.3 / Fabric）｜服务器：`play.simpfun.cn:14039`
> 当前客户端清单版本：`20261102.1350`

| 版本 | 日期 | 清单版本 | 一句话 |
|---|---|---|---|
| **v5.3.1** | 2026-11-02 | `20261102.1350` | 白名单停用，使用说明与三份教程同步校准 |
| **v5.3** | 2026-10-29 | `20261102.1310` | 干净整包重发 + 更新器换代（进度条 / 主程序最后写 / 支持 remove） |
| **v5.2** | 2026-10-29 | `20261029.1149` | 加语音 mod、清单与更新地址改走 gh-proxy 镜像、修哈希一致性 |
| **v5.1** | 2026-10-28 晚 | `20261028.2341` | 修「启动卡在 检查 mod N/18」 |
| **v5** | 2026-10-28 | `20261028.1350` | 自动更新器 / 白名单按名字 / 皮肤服务端同步 |

---

## v5.3.1（2026-11-02）：白名单停用，文档校准

服务器侧改动：**白名单不再需要**。玩家填好名字、进服注册登录即可；`server.properties` 的
`white-list` / `enforce-whitelist` 置为 `false`，EasyAuth 继续把关。EasyWhitelist 插件仍装着，
但不参与放行，`easywhitelist add/remove` 留着备用。

文档侧（这次真改了的东西）：

- `dist/使用说明.txt`：删掉「把准确名字发给管理员加白名单」，换成「三、进服不需要申请」；
  顺手把标题的 v5 改成 v5.3、补了进度条和 `/login` 提示；
- `docs/凝紫服-新玩家入服指南.md`：开头说明、群公告第 7 条、FAQ 那一行、管理员检查清单全部改成
  「已停用」，原 `easywhitelist` 命令归到「历史参考」；
- `docs/凝紫服-进服教程-v5.md`：群公告第 5 条、第四节白名单段、FAQ、管理端备忘四处的命令标注「已停用」；
- `docs/凝紫服-Mac玩家进服教程.md`：群公告第 6 条、第五/六节、FAQ 同步；
- `HANDOVER.md` 与 `docs/HANDOVER.md`：配置项改成 `white-list=false`，命令表标注已停用；
- 三份教程里过期的「凝紫客户端-完整版-v4/v5.zip」一并换成 `凝紫启动器-v5.3-干净版.zip`。

清单版本升到 `20261102.1350`（只有 `使用说明.txt` 的哈希变了）。

---

## v5.3（2026-10-29）：整包重发 + 更新器换代

**背景**：v5.2 发完之后更新日志停在 v5.1，玩家看到的 `更新说明.txt` 停在 v5，版本口径一度有三套（日志 5.1 / 清单 5.2 / 包名 5.3）。本次把三者对齐。

**更新器**：`凝紫客户端.exe`，13,312 B，内部名 `updater_new.exe`，源码 `src/updater.cs`。

1. 加了进度条窗口「凝紫客户端 · 正在更新」，逐文件显示 `正在更新 3/7`；
2. 下载顺序把 `凝紫客户端(主程序).exe` 排到最后——它最容易被占用，失败也不拖累其它文件；
3. 支持清单里的 `remove` 字段，能主动删掉旧文件名（v5.2 用它清了旧的 `voicechat-fabric-…`）；
4. 路径按段 `Uri.EscapeDataString`，带空格/中文的 mod 文件名不再 404；
5. 拉清单 15 秒、下载 30 秒超时；任何一步失败只记 `updater.log`，照常启动游戏。

> 更新器自身不在清单里（运行中的 exe 覆盖不了自己），只能随整包下发。
> **所以老玩家的更新器不会被自动替换，必须重下整包。**

**整包**：`凝紫启动器-v5.3.zip`，1.16 GB / 5874 个条目（含内置 Java 与 403 MB 资源 zip）。

**已知打包缺陷（下次修）**：

- 包里混进了 `config.ini`（含玩家名）、`.clientver`、`launcher.log` / `error.log` / `updater.log`、
  `game/logs` 13 个、`game/temp` 16 个、`game/xaero` 缓存 196 个；
- `游戏资源-assets.zip`（403 MB）与已解压的 `game/assets`（5147 个对象）同时存在，包体翻倍；
- 两个 exe 的 FileVersion 均为 `0.0.0.0`，只能靠 `.clientver` 判断版本；无代码签名，首启会被 SmartScreen 提示。

## v5.2（2026-10-29）：语音 + 国内镜像 + 哈希一致性

1. **Simple Voice Chat**：`game/mods/voicechat-2.6.27-mc26.3.jar`（5.6 MB），服务端装同名 mod，靠近即语音；
   旧文件名写入 `remove`，玩家侧自动清理，不用手动删；
2. **清单改走国内镜像**：`base` 换成 `https://gh-proxy.com/https://raw.githubusercontent.com/…/dist/`，
   `updater.ini` 里的 `url=` 同样走代理，解决国内直连 raw 超时；
3. **`updater.ini` 纳入清单**：清单地址能自愈到快镜像，不用玩家手动改；
4. **哈希一致性**：关掉 `.gitattributes` 的 EOL 转换、按 dist 重算 sha、归一化后再次重算
   ——修的就是 `updater.log` 里那串 `校验失败: updater.ini` 死循环（镜像缓存与 raw 内容不一致 → sha 对不上 →
   跳过并每次重试）；
5. 顺带把 `修复说明`、`使用说明.txt` 纳入下发。

**仍待解决**：`updater.log` 显示 10:21 / 11:48 / 11:50 三次 `校验失败`，说明发版后没在干净目录自测；
另有一次 `UnauthorizedAccessException`（主程序运行中被覆盖），需要"先退游戏再更新"或加重试。

---

## v5.1（2026-10-28 晚）：修「启动卡在 检查 mod N/18」

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

当前清单版本 `20261102.1310`，13 个文件：主程序、`updater.ini`、`app.ico`、`logo.png`、`manifest.json`、
`使用说明.txt`、`更新说明.txt`、`修复说明-v5.1.txt`、2 份 CustomSkinLoader 配置、
`architectury-fabric-22.0.5.jar`、`Quick Skin - Fabric - 26.3-3.1.1.jar`、`voicechat-2.6.27-mc26.3.jar`。

> 注意：**更新器 `凝紫客户端.exe` 不在清单里**，改它必须重发整包，老玩家不会自动拿到新更新器。

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

- [ ] **整包白名单**：整包是直接拷目录打出来的，绕过了 `发布.py` 的 INCLUDE，才把 `config.ini`、日志、`game/temp`、xaero 缓存一起打进去；`发布.py` 需要一份显式 EXCLUDE，并让 `--pack` 走同一份规则；
- [ ] **资源双份**：`游戏资源-assets.zip` 与解压后的 `game/assets` 二选一，现在包体 1.16 GB；
- [ ] **exe 版本信息**：两个 exe 的 FileVersion 还是 `0.0.0.0`，编译时带上版本号才能排查问题；
- [ ] **发版自测**：每次发完在干净目录跑一次，确认 `updater.log` 里没有 `校验失败` 再放玩家；
- [ ] **Mac 包未真机验证**：`凝紫启动器.command` 依赖 `curl` / `shasum` / `osascript`，Prism 的 `--launch` 参数也要实测；第一个 Mac 玩家跑完收集 `启动器日志.txt`；
- [ ] `start.sh` 里 Migrate 每次启动都跑（会重写 whitelist/usercache/ops），可择机删掉；
- [ ] `SkinRestorer` 的 `/skin set web` 走 MineSkin，没有 API key（有频率限制），需要的话去 account.mineskin.org 申请；
- [ ] 服务端 `config/quickskin-server.json` 可调纹理上限、是否把皮肤共享给原版客户端（`shareAccountSkinWithVanillaClients`）；
- [ ] 旧存档里的模组物品（旅行背包/深暗/农夫乐事）在 26.3 无法解码，属于内容模组缺失，尚未清理。
