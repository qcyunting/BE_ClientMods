#!/usr/bin/env python3
"""扫描本地目录并输出审核用行为包/资源包目录（不压缩）。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
import time


TARGET_BEHAVIOR = "behavior_packs"
TARGET_RESOURCE = "resource_packs"
VALID_TYPES = {"data": TARGET_BEHAVIOR, "resources": TARGET_RESOURCE}
REMOVABLE_SUFFIXES = {".zip", ".mcp"}


def _rmtree_force(path: Path) -> None:
    def _onerror(func, target_path: Path, exc_info):
        try:
            os.chmod(target_path, stat.S_IWRITE)
            func(target_path)
        except OSError:
            raise

    shutil.rmtree(path, onerror=_onerror)


def _safe_unlink(file_path: Path) -> bool:
    try:
        file_path.unlink()
        return True
    except PermissionError:
        try:
            os.chmod(file_path, stat.S_IWRITE)
            file_path.unlink()
            return True
        except (PermissionError, OSError):
            return False
    except OSError:
        return False


def _ensure_empty_output_dir(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return

    for child in path.iterdir():
        if child.is_dir():
            _rmtree_force(child)
        else:
            if not _safe_unlink(child):
                raise RuntimeError(f"无法清理旧输出目录（可能被占用）：{child}")


def _prepare_clean_audit_root(root: Path, audit_root: Path) -> tuple[Path, Path]:
    audit_root_resolved = audit_root.resolve()
    root_resolved = root.resolve()
    if audit_root_resolved == root_resolved:
        raise RuntimeError(f"审核目录不能和扫描根目录相同：{audit_root_resolved}")
    if audit_root_resolved == audit_root_resolved.anchor:
        raise RuntimeError(f"审核目录不能是盘符根目录：{audit_root_resolved}")
    if not audit_root_resolved.is_relative_to(root_resolved):
        raise RuntimeError(f"审核目录必须在扫描根目录下：{audit_root_resolved}")

    behavior_dir = audit_root / TARGET_BEHAVIOR
    resource_dir = audit_root / TARGET_RESOURCE
    audit_root.mkdir(parents=True, exist_ok=True)
    _ensure_empty_output_dir(behavior_dir)
    _ensure_empty_output_dir(resource_dir)
    return behavior_dir, resource_dir


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
    has_resources = any(
        isinstance(module, dict) and module.get("type") == "resources"
        for module in modules
    )

    if has_data and has_resources:
        return None
    if has_data:
        return "data"
    if has_resources:
        return "resources"
    return None


def copy_pack(pack_dir: Path, output_root: Path, used_names: set[str]) -> Path:
    base_name = pack_dir.name
    dest_name = base_name
    if dest_name in used_names:
        index = 1
        while f"{base_name}_{index}" in used_names:
            index += 1
        dest_name = f"{base_name}_{index}"
    used_names.add(dest_name)
    dest_dir = output_root / dest_name
    if dest_dir.exists():
        _rmtree_force(dest_dir)
    shutil.copytree(pack_dir, dest_dir)
    return dest_dir


def remove_zip_and_mcp_files(root: Path) -> tuple[int, list[Path]]:
    removed = 0
    failed: list[Path] = []
    for item in root.rglob("*"):
        if item.is_file() and item.suffix.lower() in REMOVABLE_SUFFIXES:
            if _safe_unlink(item):
                removed += 1
            else:
                failed.append(item)
    return removed, failed


def collect_pack_dirs(root: Path) -> list[Path]:
    pack_dirs: list[Path] = []
    for mod_dir in sorted(root.iterdir()):
        if not mod_dir.is_dir() or is_hidden_dir(mod_dir):
            continue

        for pack_dir in sorted(mod_dir.iterdir()):
            if not pack_dir.is_dir() or is_hidden_dir(pack_dir):
                continue
            if (pack_dir / "manifest.json").is_file():
                pack_dirs.append(pack_dir)
    return pack_dirs


def build_review_package(root: Path, audit_root: Path) -> None:
    start_time = time.perf_counter()
    behavior_dir, resource_dir = _prepare_clean_audit_root(root, audit_root)
    behavior_used_names: set[str] = set()
    resource_used_names: set[str] = set()

    pack_dirs = collect_pack_dirs(root)
    packaged = []
    behavior_count = 0
    resource_count = 0
    skipped = []

    for pack_dir in pack_dirs:
        pack_type = read_pack_type(pack_dir / "manifest.json")
        if pack_type not in VALID_TYPES:
            skipped.append((str(pack_dir), "manifest modules 无效或未识别"))
            continue

        target_dir = behavior_dir if pack_type == "data" else resource_dir
        used_names = behavior_used_names if pack_type == "data" else resource_used_names
        copy_pack(pack_dir, target_dir, used_names)
        packaged.append((pack_dir.name, pack_type))
        if pack_type == "data":
            behavior_count += 1
        else:
            resource_count += 1

    removed_count, failed_files = remove_zip_and_mcp_files(audit_root)

    if packaged:
        print("复制完成：")
        for name, pack_type in packaged:
            print(f"- {name} -> {pack_type}")
    else:
        print("未发现可打包包。")
    print(f"总计：行为包 {behavior_count} 个，资源包 {resource_count} 个")
    print(f"已清理 .zip/.mcp 文件：{removed_count} 个")
    if failed_files:
        print("以下文件未能删除（可能被占用）：")
        for file_path in failed_files:
            print(f"- {file_path}")
    elapsed = time.perf_counter() - start_time
    print(f"输出目录：{audit_root}")
    print(f"用时：{elapsed:.2f} 秒")
    if skipped:
        print("跳过：")
        for name, reason in skipped:
            print(f"- {name}: {reason}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="扫描本地目录并按类型输出行为包/资源包"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="要扫描的根目录（默认当前目录）",
    )
    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=Path.cwd() / ".review_output",
        help="审核输出目录（默认当前目录/.review_output）",
    )
    args = parser.parse_args()

    build_review_package(args.root.resolve(), args.audit_dir.resolve())


if __name__ == "__main__":
    main()
