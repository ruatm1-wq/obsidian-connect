# Obsidian Connect

轻量级 Obsidian Local REST API 连接管理器。

一键检测 Obsidian API 连接状态，共享配置给 AI Agent 工具使用。

## 安装

```bash
# 克隆
git clone https://github.com/你的用户名/obsidian-connect.git
cd obsidian-connect

# 复制配置模板并填入你的信息
cp config.template.json ~/.obsidian-connect/config.json
# 编辑 ~/.obsidian-connect/config.json 填入你的 token
```

## 用法

```bash
# 检查连接
python obsidian-connect.py check

# 查看配置
python obsidian-connect.py config
```

## 配置

1. Obsidian 中安装 [Local REST API](obsidian://show-plugin?id=obsidian-local-rest-api) 插件
2. 插件设置中复制你的 API Token
3. 填入 `~/.obsidian-connect/config.json`

## 环境变量

- `OBSIDIAN_CONNECT_DIR` — 自定义配置目录（默认 `~/.obsidian-connect`）
