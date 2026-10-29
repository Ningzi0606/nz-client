# 凝紫服 · Mac 玩家进服教程

> 服务器：**play.simpfun.cn:14039**｜Minecraft **26.3**（Fabric）｜离线（免正版）服  
> Mac **不能**用群里那个 `凝紫客户端-完整版-v5.zip`（那是 Windows 的 exe + Windows 版 Java），  
> Mac 用单独的 **`凝紫客户端-Mac.zip`**。

---

## 一、群公告版（直接复制发群）

```
【Mac 玩家进服】

1. 先装 Java 25：adoptium.net/temurin/releases/?version=25
   M 芯片选 aarch64，Intel 选 x64
2. 装 Prism Launcher（macOS 版）：prismlauncher.org/download/macOS
3. 群文件下载「凝紫客户端-Mac.zip」，解压到「文稿」或桌面
4. 双击「凝紫启动器.command」
   - 第一次被系统拦：右键 → 打开 → 仍要打开
   - 它会自动装好「凝紫服」实例、检查更新、启动游戏
5. 进服后：
   /register 你的密码 你的密码
   /login 你的密码
   /autologin set 你的密码   （可选，自动登录）
6. 提示 You are not white-listed = 白名单没加，把准确名字发管理

以后每次玩：只双击「凝紫启动器.command」就行（会自动更新）
皮肤：进游戏按 Esc → Change Skin
```

---

## 二、为什么 Mac 要单独一套

| | Windows | macOS |
|---|---|---|
| 客户端 | 凝紫客户端-完整版-v5.zip | 凝紫客户端-Mac.zip |
| 启动方式 | 双击 凝紫客户端.exe | 双击 凝紫启动器.command |
| 自动更新 | 更新器内置 | 脚本检查 GitHub 清单，增量同步 mod |
| 启动器 | 自带 | 需要 Prism Launcher |

Windows 那个 exe 是 C# 写的、还带了 Windows 版 Java，macOS 上跑不起来，不是配置问题。

---

## 三、准备（一次性）

1. **Java 25**
   - 地址：<https://adoptium.net/temurin/releases/?version=25>
   - Apple 芯片（M1/M2/M3/M4）选 **aarch64 / arm64**
   - Intel 芯片选 **x64**
   - 装完不用配环境变量

2. **Prism Launcher**
   - 地址：<https://prismlauncher.org/download/macOS>
   - 第一次打开会问 Java，选刚装的 Java 25

---

## 四、安装客户端

1. 群文件下载 **凝紫客户端-Mac.zip**（约 34MB），解压到桌面或「文稿」；
2. **第一次打开被拦是正常的**，两种解法：
   - 右键点 `凝紫启动器.command` → **打开** → 弹窗里再点「打开」；
   - 或打开「终端」，执行：
     ```
     chmod +x ~/Desktop/凝紫客户端-Mac/凝紫启动器.command
     ```
3. 双击 `凝紫启动器.command`，它会：
   - 把 `凝紫服` 实例装进 Prism 的 instances 目录；
   - 从 GitHub 拉更新清单，比对 sha256，只下载变化的 mod/配置；
   - 自动启动游戏。
4. 所有过程会写进同目录的 **`启动器日志.txt`**，出问题发这个文件。

---

## 五、进服

1. 游戏启动后 → 多人游戏 → 服务器列表里已有「凝紫服」（`play.simpfun.cn:14039`）；
2. **白名单**：没加会提示 `You are not white-listed on this server!`  
   把准确名字（大小写一致）发管理，管理执行 `easywhitelist add 名字`，立刻生效；
3. 第一次进服会被定住，依次输入：
   ```
   /register 密码 密码      ← 注册（两遍）
   /login 密码              ← 登录
   /autologin set 密码      ← 可选，以后自动登录
   ```
4. 登录成功即可正常游玩。

---

## 六、皮肤

进游戏按 **Esc** → **Change Skin**：

- 导入 64×64 PNG（Import，或直接把图片拖进窗口）；
- 选 Classic（粗手臂）/ Slim（细手臂）；
- 选披风（支持 GIF 动图）。

服务器装了皮肤同步，换完别人立刻能看到（对方也用本客户端的前提下）。

---

## 七、以后更新

**只双击 `凝紫启动器.command`** 就行：它会先同步最新 mod/配置，再启动游戏。  
不需要重新下载整个包（除非服务端换了大版本，我会在群里说）。

---

## 八、常见问题

| 现象 | 原因 | 处理 |
|---|---|---|
| 双击 .command 没反应 / 被拦 | Gatekeeper | 右键 → 打开；或终端 `chmod +x` |
| 提示找不到 Java | 没装 / 版本不对 | 装 Java 25，Prism 里重新选 Java |
| 双击后只打开 Prism，不自动进游戏 | Prism 版本不支持命令行启动 | 在 Prism 里点「凝紫服」→ 启动 |
| 启动器日志里「拉取清单失败」 | 连不上 GitHub | 挂代理后再开，或忽略（照常进游戏） |
| `You are not white-listed` | 白名单没加 | 把准确名字发管理 |
| 进服不能动 | 没登录 | `/login 密码` |
| 游戏很卡 | 内存/渲染设置 | Prism 实例设置里内存调到 4–6G；光影在 macOS 上支持有限 |
| 皮肤没变化 | 没选 / 没同步 | Esc → Change Skin 重新选 |

日志位置：
- 启动器：`凝紫客户端-Mac/启动器日志.txt`
- 游戏：`~/Library/Application Support/PrismLauncher/instances/凝紫服/.minecraft/logs/latest.log`

---

## 九、给管理员

- Mac 包的更新走**同一个** `update.json`：路径 `game/mods/...`、`game/config/...` 会被脚本映射到实例的 `.minecraft/mods`、`.minecraft/config`，其它文件放实例根目录；
- 发版流程不变：改 Windows 客户端 → 双击 `一键发布.bat`；
- Mac 玩家换新版本时：脚本会自动增量更新，不需要重发包；
- 如果 Mac 玩家反馈脚本报错，看 `启动器日志.txt` 里的 `curl` / `shasum` 行。
