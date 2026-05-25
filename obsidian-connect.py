"""
Obsidian API 连接管理器
- 持久化存储 API 凭证
- 一键检测连接状态
- 工具间共享配置

用法:
  python obsidian-connect.py check     # 检查连接
  python obsidian-connect.py config    # 查看当前配置
"""

import json, ssl, sys, os
from urllib.request import Request, urlopen
from urllib.parse import quote

# ===== 配置路径（可通过环境变量覆盖） =====
CONFIG_DIR = os.environ.get("OBSIDIAN_CONNECT_DIR", os.path.join(os.path.expanduser("~"), ".obsidian-connect"))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# ===== 默认配置（占位，首次运行需配置） =====
DEFAULT_CONFIG = {
    "host": "https://localhost:27124",
    "token": "your-obsidian-api-token-here",
    "vault": "your-vault-name-here",
    "last_verified": None
}


def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    """保存配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"✅ 配置已保存: {CONFIG_FILE}")


def check_connection(cfg):
    """测试 Obsidian API 连接"""
    host = cfg["host"]
    token = cfg["token"]
    
    # 跳过 SSL 验证（本地自签名证书）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        # 测试根路径 → 获取插件信息
        req = Request(f"{host}/")
        req.add_header("Authorization", f"Bearer {token}")
        resp = urlopen(req, context=ctx, timeout=5)
        data = json.loads(resp.read().decode())
        
        version = data.get("manifest", {}).get("version", "unknown")
        authenticated = data.get("authenticated", False)
        
        # 测试 vault 根目录 → 自动发现
        req2 = Request(f"{host}/vault/")
        req2.add_header("Authorization", f"Bearer {token}")
        resp2 = urlopen(req2, context=ctx, timeout=5)
        vault_data = json.loads(resp2.read().decode())
        file_count = len(vault_data.get("files", []))
        
        print(f"""
╔══════════════════════════════════╗
║   Obsidian API 连接状态         ║
╠══════════════════════════════════╣
║  状态: ✅ 已连接                ║
║  验证: {"✅ 通过" if authenticated else "❌ 失败":<19}║
║  插件: v{version:<23}║
║  目录: {file_count:<4} 个根目录           ║
║  Token: {token[:8]}...{'':>19}║
╚══════════════════════════════════╝
""")
        
        # 更新验证时间
        from datetime import datetime
        cfg["last_verified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_config(cfg)
        
        return True
        
    except Exception as e:
        print(f"""
╔══════════════════════════════════╗
║   Obsidian API 连接状态         ║
╠══════════════════════════════════╣
║  状态: ❌ 未连接                ║
║  错误: {str(e)[:30]:<21}║
║  排查:                          ║
║  1. Obsidian 是否已打开？       ║
║  2. Local REST API 插件启用？   ║
║  3. Token 是否匹配？            ║
╚══════════════════════════════════╝
""")
        return False


def show_config(cfg):
    """显示当前配置"""
    print(f"""
╔══════════════════════════════════╗
║   Obsidian 连接配置             ║
╠══════════════════════════════════╣
║  地址: {cfg['host']:<25}║
║  Token: {cfg['token'][:8]}...{'':>19}║
║  Vault: {cfg['vault']:<22}║
║  上次验证: {str(cfg.get('last_verified','从未')):<18}║
║  配置文件:                     ║
║  {CONFIG_FILE:<34}║
╚══════════════════════════════════╝
""")
    print("其他工具读取此文件即可获得连接信息。")


def main():
    cfg = load_config()
    
    if len(sys.argv) < 2:
        print("用法: python obsidian-connect.py [check|config]")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "check" or cmd == "test":
        check_connection(cfg)
    elif cmd == "config" or cmd == "status":
        show_config(cfg)
    else:
        print(f"未知命令: {cmd}")
        print("可用: check, config")


if __name__ == "__main__":
    main()
