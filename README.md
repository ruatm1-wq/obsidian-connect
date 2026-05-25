<!-- markdownlint-disable MD033 MD041 -->

<h1 align="center">🔗 Obsidian Connect</h1>

<p align="center">
  <em>轻量级 Obsidian Local REST API 连接管理器 · Lightweight connection manager for Obsidian's Local REST API</em>
</p>

<p align="center">
  <b>中文</b> · <a href="#english">English</a>
</p>

---

<div id="chinese">

## 中文说明

### 这是什么？

Obsidian Connect 是一个命令行工具，用于快速检测和连接 Obsidian 的 Local REST API 插件。

**适用场景：** AI Agent（如 Hermes、Claude Code、Codex 等）需要读写 Obsidian 笔记时，通过此工具统一管理连接配置，无需每次手动输入 API Token。

### 安装

```bash
git clone https://github.com/ruatm1-wq/obsidian-connect.git
cd obsidian-connect
```

### 配置

1. Obsidian 中安装 [Local REST API](obsidian://show-plugin?id=obsidian-local-rest-api) 插件并启用
2. 在插件设置中复制你的 **API Token**
3. 创建配置文件：

```bash
mkdir -p ~/.obsidian-connect
cp config.template.json ~/.obsidian-connect/config.json
```

4. 编辑 `~/.obsidian-connect/config.json`，填入你的 Token 和 Vault 名称：

```json
{
  "host": "https://localhost:27124",
  "token": "你的-token-粘贴到这里",
  "vault": "你的-vault-名称"
}
```

> 可通过环境变量 `OBSIDIAN_CONNECT_DIR` 自定义配置目录。

### 用法

```bash
# 检查默认 vault 连接状态
python obsidian-connect.py check

# 检查指定 vault
python obsidian-connect.py check 工作台

# 列出所有 vault
python obsidian-connect.py list

# 查看当前配置
python obsidian-connect.py config

# 添加新 vault（交互式）
python obsidian-connect.py add <vault名字>

# 删除 vault
python obsidian-connect.py remove <vault名字>

# 设置默认 vault
python obsidian-connect.py default <vault名字>
```

### 输出示例

```
╔══════════════════════════════════╗
║   Obsidian API 连接状态         ║
╠══════════════════════════════════╣
║  状态: ✅ 已连接                ║
║  验证: ✅ 通过                  ║
║  插件: v4.0.3                   ║
║  目录: 9 个根目录               ║
╚══════════════════════════════════╝
```

### 多工具共享配置

Hermes、Reasonix Code、OpenCode 等 AI Agent 工具可以通过读取 `~/.obsidian-connect/config.json` 获取连接信息，实现一次配置、到处可用。

</div>

---

<hr>

<div id="english">

## <span id="english">English</span>

### What is this?

Obsidian Connect is a CLI tool that quickly checks and manages connections to Obsidian's Local REST API plugin.

**Use case:** AI agents (Hermes, Claude Code, Codex, etc.) need to read/write Obsidian notes. This tool manages connection config centrally so you don't have to enter the API token every time.

### Setup

1. Install and enable [Local REST API](obsidian://show-plugin?id=obsidian-local-rest-api) in Obsidian
2. Copy your **API Token** from the plugin settings
3. Create your config file:

```bash
mkdir -p ~/.obsidian-connect
cp config.template.json ~/.obsidian-connect/config.json
```

4. Edit `~/.obsidian-connect/config.json` with your token and vault name:

```json
{
  "host": "https://localhost:27124",
  "token": "paste-your-token-here",
  "vault": "your-vault-name"
}
```

> You can override the config directory with the `OBSIDIAN_CONNECT_DIR` environment variable.

### Usage

```bash
# Check default vault
python obsidian-connect.py check

# Check specific vault
python obsidian-connect.py check my-vault

# List all vaults
python obsidian-connect.py list

# View config
python obsidian-connect.py config

# Add vault (interactive)
python obsidian-connect.py add <vault-name>

# Remove vault
python obsidian-connect.py remove <vault-name>

# Set default vault
python obsidian-connect.py default <vault-name>
```

### Sample Output

```
╔══════════════════════════════════╗
║   Obsidian API Status           ║
╠══════════════════════════════════╣
║  Status: ✅ Connected           ║
║  Auth:   ✅ Passed              ║
║  Plugin: v4.0.3                 ║
║  Dirs:   9 root folders         ║
╚══════════════════════════════════╝
```

### Sharing Config Across AI Tools

Hermes, Reasonix Code, OpenCode and other AI agents can all read `~/.obsidian-connect/config.json` — configure once, use everywhere.

</div>

---

## License

MIT
