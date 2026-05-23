#!/usr/bin/env python3
"""收集行为包脚本目录到 .py2mcp/ExampleBehavior，并回填同名 .mcp 文件。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import time


TARGET_BEHAVIOR = "data"


def is_hidden_dir(path: Path) -> bool:
    return path.name.startswith(".")


def read_pack_type(manifest_path: Path) -> str | None:
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    modules = data.get("modules")
    if not isinstance(modules, list):
        return None

    has_data = any(
        isinstance(module, dict) and module.get("type") == "data"
        for module in modules
    )
    if has_data:
        return "data"
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


def copy_script_dir(script_dir: Path, example_behavior_dir: Path) -> Path:
    target_dir = example_behavior_dir / script_dir.name
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(script_dir, target_dir)
    return target_dir


def copy_mcp_back_if_exists(script_name: str, example_behavior_dir: Path, behavior_pack_dir: Path) -> Path | None:
    source_mcp = example_behavior_dir / f"{script_name}.mcp"
    if not source_mcp.is_file():
        return None
    target_mcp = behavior_pack_dir / source_mcp.name
    if target_mcp.exists():
        target_mcp.unlink()
    shutil.move(source_mcp, target_mcp)
    return target_mcp


def run(root: Path, example_behavior_dir: Path) -> None:
    start_time = time.perf_counter()
    example_behavior_dir.mkdir(parents=True, exist_ok=True)

    behavior_packs = collect_behavior_pack_dirs(root)
    copied_scripts: list[tuple[Path, Path]] = []
    copied_mcps: list[tuple[Path, Path]] = []

    for behavior_pack_dir in behavior_packs:
        for script_dir in collect_script_dirs(behavior_pack_dir):
            target_script_dir = copy_script_dir(script_dir, example_behavior_dir)
            copied_scripts.append((script_dir, target_script_dir))

            copied_mcp = copy_mcp_back_if_exists(
                script_dir.name, example_behavior_dir, behavior_pack_dir
            )
            if copied_mcp is not None:
                copied_mcps.append(
                    (example_behavior_dir / copied_mcp.name, copied_mcp)
                )

    if copied_scripts:
        print("已复制脚本目录：")
        for source_dir, target_dir in copied_scripts:
            print(f"- {source_dir} -> {target_dir}")
    else:
        print("未发现包含 modMain.py 的脚本目录。")

    if copied_mcps:
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
        description="复制行为包脚本目录到 .py2mcp/ExampleBehavior，并回填同名 .mcp"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="扫描根目录（默认当前目录）",
    )
    parser.add_argument(
        "--example-behavior-dir",
        type=Path,
        default=Path.cwd() / ".py2mcp" / "ExampleBehavior",
        help="ExampleBehavior 目录（默认当前目录/.py2mcp/ExampleBehavior）",
    )
    args = parser.parse_args()

    run(args.root.resolve(), args.example_behavior_dir.resolve())


if __name__ == "__main__":
    main()
