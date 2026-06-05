#!/usr/bin/env python3
"""收集行为包脚本目录，并回填同名 .mcp 文件。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time


# ===== 可配置项 =====
SCRIPT_OUTPUT_DIR = Path(".py2mcp") / "behavior_packs" / "mcp"
MCP_DIR = Path(".py2mcp") / "mcp"
FILL_BACK_MCP = True

TARGET_BEHAVIOR = "data"


def resolve_config_path(root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (root / path).resolve()


def is_hidden_dir(path: Path) -> bool:
    return path.name.startswith(".")


def read_pack_type(manifest_path: Path) -> str | None:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None

    modules = data.get("modules")
    if not isinstance(modules, list):
        return None

    has_data = any(
        isinstance(module, dict) and module.get("type") == TARGET_BEHAVIOR
        for module in modules
    )
    if has_data:
        return TARGET_BEHAVIOR
    return None


def collect_behavior_pack_dirs(root: Path) -> list[Path]:
    behavior_packs: list[Path] = []
    for mod_dir in sorted(root.iterdir()):
        if not mod_dir.is_dir() or is_hidden_dir(mod_dir):
            continue

        for pack_dir in sorted(mod_dir.iterdir()):
            if not pack_dir.is_dir() or is_hidden_dir(pack_dir):
                continue
            manifest_path = pack_dir / "manifest.json"
            if not manifest_path.is_file():
                continue
            if read_pack_type(manifest_path) == TARGET_BEHAVIOR:
                behavior_packs.append(pack_dir)
    return behavior_packs


def collect_script_dirs(behavior_pack_dir: Path) -> list[Path]:
    script_dirs: list[Path] = []
    for child in sorted(behavior_pack_dir.iterdir()):
        if not child.is_dir() or is_hidden_dir(child):
            continue
        if (child / "modMain.py").is_file():
            script_dirs.append(child)
    return script_dirs


def copy_script_dir(script_dir: Path, script_output_dir: Path) -> Path:
    target_dir = script_output_dir / script_dir.name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(script_dir, target_dir)
    return target_dir


def copy_mcp_back_if_exists(
    script_name: str,
    mcp_dir: Path,
    behavior_pack_dir: Path,
) -> Path | None:
    source_mcp = mcp_dir / f"{script_name}.mcp"
    if not source_mcp.is_file():
        return None

    target_mcp = behavior_pack_dir / source_mcp.name
    if target_mcp.exists():
        target_mcp.unlink()
    shutil.copy2(source_mcp, target_mcp)
    return target_mcp


def run(root: Path, script_output_dir: Path, mcp_dir: Path) -> None:
    start_time = time.perf_counter()
    script_output_dir.mkdir(parents=True, exist_ok=True)

    behavior_packs = collect_behavior_pack_dirs(root)
    copied_scripts: list[tuple[Path, Path]] = []
    copied_mcps: list[tuple[Path, Path]] = []

    for behavior_pack_dir in behavior_packs:
        for script_dir in collect_script_dirs(behavior_pack_dir):
            target_script_dir = copy_script_dir(script_dir, script_output_dir)
            copied_scripts.append((script_dir, target_script_dir))

            if not FILL_BACK_MCP:
                continue

            copied_mcp = copy_mcp_back_if_exists(
                script_dir.name,
                mcp_dir,
                behavior_pack_dir,
            )
            if copied_mcp is not None:
                copied_mcps.append((mcp_dir / copied_mcp.name, copied_mcp))

    if copied_scripts:
        print("已复制脚本目录：")
        for source_dir, target_dir in copied_scripts:
            print(f"- {source_dir} -> {target_dir}")
    else:
        print("未发现包含 modMain.py 的脚本目录。")

    if not FILL_BACK_MCP:
        print("已关闭 .mcp 文件回填。")
    elif copied_mcps:
        print("已回填 .mcp 文件：")
        for source_mcp, target_mcp in copied_mcps:
            print(f"- {source_mcp} -> {target_mcp}")
    else:
        print("未发现可回填的同名 .mcp 文件。")

    print(f"行为包数量：{len(behavior_packs)}")
    print(f"脚本目录数量：{len(copied_scripts)}")
    print(f"用时：{time.perf_counter() - start_time:.2f} 秒")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="复制行为包脚本目录，并回填同名 .mcp"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="扫描根目录（默认当前目录）",
    )
    parser.add_argument(
        "--script-output-dir",
        type=Path,
        default=SCRIPT_OUTPUT_DIR,
        help=f"脚本目录输出目录（默认 {SCRIPT_OUTPUT_DIR}）",
    )
    parser.add_argument(
        "--mcp-dir",
        type=Path,
        default=MCP_DIR,
        help=f".mcp 文件目录（默认 {MCP_DIR}）",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    run(
        root,
        resolve_config_path(root, args.script_output_dir),
        resolve_config_path(root, args.mcp_dir),
    )


if __name__ == "__main__":
    main()
