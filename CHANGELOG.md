# v5 更新日志

> 2026-10-28｜凝紫服（Minecraft 26.3 / Fabric）
> 服务器：`play.simpfun.cn:14039`｜客户端清单版本：`20261028.1350`

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
