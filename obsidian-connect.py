"""
Obsidian API 连接管理器
- 持久化存储 API 凭证
- 支持多 Vault 切换
- 一键检测连接状态
- 工具间共享配置

用法:
  python obsidian-connect.py check                    # 检查默认 vault
  python obsidian-connect.py check 工作台             # 检查指定 vault
  python obsidian-connect.py list                     # 列出所有 vault
  python obsidian-connect.py config                   # 查看当前配置
  python obsidian-connect.py add <名字>                # 交互式添加 vault
"""

import json, ssl, sys, os
from urllib.request import Request, urlopen

# ===== 配置路径（可通过环境变量覆盖） =====
CONFIG_DIR = os.environ.get("OBSIDIAN_CONNECT_DIR", os.path.join(os.path.expanduser("~"), ".obsidian-connect"))
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# ===== 默认配置 =====
DEFAULT_CONFIG = {
    "default_host": "https://localhost:27124",
    "default_token": "your-obsidian-api-token-here",
    "default": None,   # 默认 vault 名字
    "vaults": {},
    "last_verified": None
}


def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            try:
                cfg = json.load(f)
                # 保证字段存在
                cfg.setdefault("vaults", {})
                return cfg
            except:
                pass
    return dict(DEFAULT_CONFIG)


def save_config(cfg):
    """保存配置"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


def get_vault_config(cfg, name=None):
    """获取指定 vault 的连接配置"""
    name = name or cfg.get("default")
    if name and name in cfg.get("vaults", {}):
        v = cfg["vaults"][name]
        return {
            "host": v.get("host", cfg["default_host"]),
            "token": v.get("token", cfg["default_token"]),
            "name": name,
            "desc": v.get("desc", ""),
            "vault": v.get("vault", "")
        }
    # 没有指定 vault，用默认连接
    return {
        "host": cfg["default_host"],
        "token": cfg["default_token"],
        "name": name or "(default)",
        "desc": "",
        "vault": ""
    }


def check_connection(vcfg):
    """测试 Obsidian API 连接"""
    host = vcfg["host"]
    token = vcfg["token"]
    name = vcfg["name"]

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = Request(f"{host}/")
        req.add_header("Authorization", f"Bearer {token}")
        resp = urlopen(req, context=ctx, timeout=5)
        data = json.loads(resp.read().decode())

        version = data.get("manifest", {}).get("version", "unknown")
        authenticated = data.get("authenticated", False)

        req2 = Request(f"{host}/vault/")
        req2.add_header("Authorization", f"Bearer {token}")
        resp2 = urlopen(req2, context=ctx, timeout=5)
        vault_data = json.loads(resp2.read().decode())
        file_count = len(vault_data.get("files", []))

        status = "✅" if authenticated else "❌"
        print(f"""
╔══════════════════════════════════╗
║   Obsidian API · {name:<20}║
╠══════════════════════════════════╣
║  状态: {status} {'已连接' if authenticated else '未验证':<18}║
║  插件: v{version:<23}║
║  目录: {file_count:<4} 个根目录           ║
╚══════════════════════════════════╝
""")
        return True

    except Exception as e:
        print(f"""
╔══════════════════════════════════╗
║   Obsidian API · {name:<20}║
╠══════════════════════════════════╣
║  状态: ❌ 连接失败              ║
║  原因: {str(e)[:28]:<21}║
╚══════════════════════════════════╝
""")
        return False


def cmd_check(cfg, args):
    """检查连接"""
    name = args[0] if args else cfg.get("default")
    if name:
        vcfg = get_vault_config(cfg, name)
        if vcfg["token"] == "your-obsidian-api-token-here":
            print(f"❌ 未配置 {name} 的 token，请编辑 {CONFIG_FILE}")
            return
        check_connection(vcfg)
    else:
        print("❌ 未设置默认 vault，请先添加：")
        print("   python obsidian-connect.py add <名字>")
        print(f"   或编辑 {CONFIG_FILE}")


def cmd_list(cfg):
    """列出所有 vault"""
    vaults = cfg.get("vaults", {})
    default = cfg.get("default")

    print(f"""
╔══════════════════════════════════╗
║   Obsidian Vault 列表           ║
╠══════════════════════════════════╣""")

    if not vaults:
        print("║  (无 vault 配置)                    ║")
    else:
        for name, v in vaults.items():
            mark = " ⭐" if name == default else "   "
            host = v.get("host", cfg["default_host"])
            port = host.split(":")[-1]
            desc = v.get("desc", "")
            print(f"║{mark} {name:<22}║")
            if desc:
                print(f"║    {desc:<27}║")
            print(f"║    端口 {port:<12}vault: {v.get('vault','?')[:15]:<15}║")

    print(f"""
╚══════════════════════════════════╝
配置: {CONFIG_FILE}
""")


def cmd_config(cfg):
    """显示当前配置"""
    vaults = cfg.get("vaults", {})
    default = cfg.get("default")

    print(f"""
╔══════════════════════════════════╗
║   Obsidian 连接配置             ║
╠══════════════════════════════════╣
║  默认 host: {cfg['default_host']:<25}║
║  默认 vault: {str(default):<25}║
║  已配置 vault: {len(vaults):<4} 个                ║""")

    for name in vaults:
        mark = " ⭐" if name == default else "   "
        print(f"║{mark} {name:<33}║")

    print(f"""║                                   ║
║  配置文件:                       ║
║  {CONFIG_FILE:<34}║
╚══════════════════════════════════╝
""")
    print("其他工具读取此文件即可获得连接信息。")


def cmd_add(cfg, args):
    """交互式添加 vault"""
    if not args:
        print("用法: python obsidian-connect.py add <vault名字>")
        return

    name = args[0]
    vaults = cfg.setdefault("vaults", {})

    if name in vaults:
        print(f"⚠️  vault '{name}' 已存在，覆盖？(y/n)")
        # 非交互式直接覆盖

    print(f"添加 vault: {name}")
    host = input(f"  host [{cfg['default_host']}]: ").strip() or cfg["default_host"]
    token = input(f"  token: ").strip() or input("  token (必填): ").strip()
    vpath = input(f"  vault 路径（可选）: ").strip()
    desc = input(f"  描述（可选）: ").strip()

    if not token:
        print("❌ token 不能为空")
        return

    vaults[name] = {
        "host": host,
        "token": token,
        "vault": vpath,
        "desc": desc
    }

    if cfg.get("default") is None:
        cfg["default"] = name

    save_config(cfg)
    print(f"✅ 已添加 vault '{name}'")
    print(f"   设为默认: {'是' if cfg.get('default') == name else '否'}")
    print(f"   编辑配置: {CONFIG_FILE}")


def cmd_remove(cfg, args):
    """删除 vault"""
    if not args:
        print("用法: python obsidian-connect.py remove <vault名字>")
        return

    name = args[0]
    vaults = cfg.get("vaults", {})
    if name in vaults:
        del vaults[name]
        if cfg.get("default") == name:
            cfg["default"] = next(iter(vaults.keys())) if vaults else None
        save_config(cfg)
        print(f"🗑️  已删除 vault '{name}'")
    else:
        print(f"❌ 未找到 vault '{name}'")


def cmd_set_default(cfg, args):
    """设置默认 vault"""
    if not args:
        print("用法: python obsidian-connect.py default <vault名字>")
        return

    name = args[0]
    if name in cfg.get("vaults", {}):
        cfg["default"] = name
        save_config(cfg)
        print(f"⭐ 已将 '{name}' 设为默认 vault")
    else:
        print(f"❌ 未找到 vault '{name}'")


def main():
    cfg = load_config()

    if len(sys.argv) < 2:
        print("用法: python obsidian-connect.py <命令> [参数]")
        print("")
        print("命令:")
        print("  check [名字]   检查连接（不指定则检查默认 vault）")
        print("  list           列出所有 vault")
        print("  config         查看当前配置")
        print("  add <名字>     添加 vault")
        print("  remove <名字>  删除 vault")
        print("  default <名字> 设置默认 vault")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    cmds = {
        "check": cmd_check,
        "test": cmd_check,
        "list": cmd_list,
        "ls": cmd_list,
        "config": cmd_config,
        "status": cmd_config,
        "add": cmd_add,
        "remove": cmd_remove,
        "rm": cmd_remove,
        "default": cmd_set_default,
    }

    f = cmds.get(cmd)
    if f:
        f(cfg, args)
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: check, list, config, add, remove, default")


if __name__ == "__main__":
    main()
