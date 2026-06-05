#!/usr/bin/env python3
"""扫描本地目录并输出审核用/服务器用行为包和资源包。"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import stat
import time

# ===== 可配置项 =====
ARCHIVE_TEMPLATE_DIR = Path(".py2mcp")
MCP_DIR = Path(".py2mcp") / "mcp"
OUTPUT_DIR = Path(".review_output")
REVIEW_DIR_NAME = "review"
SERVER_DIR_NAME = "server"
BUILD_REVIEW_OUTPUT = True
BUILD_SERVER_OUTPUT = True
OUTPUT_ARCHIVE_INCLUDE_ROOT_DIR = False

REVIEW_TEMPLATE_ITEMS = ("db", "level.dat", "level.dat_old", "level.old_dat", "levelname.txt")
REVIEW_TARGET_BEHAVIOR = "behavior_packs"
REVIEW_TARGET_RESOURCE = "resource_packs"
SERVER_TARGET_BEHAVIOR = "BehaviorPacks"
SERVER_TARGET_RESOURCE = "ResourcePacks"
VALID_TYPES = {"data", "resources"}
REMOVABLE_SUFFIXES = {".zip", ".mcp"}
MCP_SUFFIX = ".mcp"
MCP_ARCHIVE_SUFFIX = ".zip"
PACK_ARCHIVE_SUFFIX = ".mcpack"


def resolve_config_path(root: Path, path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (root / path).resolve()


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
        elif not _safe_unlink(child):
            raise RuntimeError(f"无法清理旧输出目录（可能被占用）：{child}")


def _validate_output_root(root: Path, output_root: Path) -> None:
    output_root_resolved = output_root.resolve()
    root_resolved = root.resolve()
    if output_root_resolved == root_resolved:
        raise RuntimeError(f"输出目录不能和扫描根目录相同：{output_root_resolved}")
    if output_root_resolved == output_root_resolved.anchor:
        raise RuntimeError(f"输出目录不能是盘符根目录：{output_root_resolved}")
    if not output_root_resolved.is_relative_to(root_resolved):
        raise RuntimeError(f"输出目录必须在扫描根目录下：{output_root_resolved}")


def prepare_output_dirs(root: Path, output_root: Path) -> dict[str, Path]:
    _validate_output_root(root, output_root)
    _ensure_empty_output_dir(output_root)

    output_dirs: dict[str, Path] = {}
    if BUILD_REVIEW_OUTPUT:
        review_root = output_root / REVIEW_DIR_NAME
        output_dirs["review_root"] = review_root
        output_dirs["review_behavior"] = review_root / REVIEW_TARGET_BEHAVIOR
        output_dirs["review_resource"] = review_root / REVIEW_TARGET_RESOURCE

    if BUILD_SERVER_OUTPUT:
        server_root = output_root / SERVER_DIR_NAME
        output_dirs["server_root"] = server_root
        output_dirs["server_behavior"] = server_root / SERVER_TARGET_BEHAVIOR
        output_dirs["server_resource"] = server_root / SERVER_TARGET_RESOURCE

    for output_dir in output_dirs.values():
        output_dir.mkdir(parents=True, exist_ok=True)
    return output_dirs


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


def make_unique_name(base_name: str, used_names: set[str]) -> str:
    dest_name = base_name
    if dest_name not in used_names:
        used_names.add(dest_name)
        return dest_name

    index = 1
    while f"{base_name}_{index}" in used_names:
        index += 1
    dest_name = f"{base_name}_{index}"
    used_names.add(dest_name)
    return dest_name


def copy_pack_dir(
    pack_dir: Path,
    output_root: Path,
    used_names: set[str],
) -> tuple[Path, int, list[Path], str]:
    dest_name = make_unique_name(pack_dir.name, used_names)
    dest_dir = output_root / dest_name
    if dest_dir.exists():
        _rmtree_force(dest_dir)
    shutil.copytree(pack_dir, dest_dir)

    removed_count, failed_files = remove_zip_and_mcp_files(dest_dir)
    return dest_dir, removed_count, failed_files, dest_name


def archive_pack_dir(
    pack_dir: Path,
    output_root: Path,
    archive_name: str,
    archive_suffix: str,
) -> Path:
    archive_path = output_root / f"{archive_name}{archive_suffix}"
    if archive_path.exists() and not _safe_unlink(archive_path):
        raise RuntimeError(f"无法覆盖旧压缩包（可能被占用）：{archive_path}")

    zip_path = Path(shutil.make_archive(str(output_root / archive_name), "zip", root_dir=pack_dir))
    if zip_path != archive_path:
        if archive_path.exists() and not _safe_unlink(archive_path):
            raise RuntimeError(f"无法覆盖旧压缩包（可能被占用）：{archive_path}")
        zip_path.replace(archive_path)
    _rmtree_force(pack_dir)
    return archive_path


def archive_output_dir(output_dir: Path) -> Path:
    archive_path = output_dir.parent / f"{output_dir.name}.zip"
    if archive_path.exists() and not _safe_unlink(archive_path):
        raise RuntimeError(f"无法覆盖输出压缩包（可能被占用）：{archive_path}")

    if not OUTPUT_ARCHIVE_INCLUDE_ROOT_DIR:
        return Path(
            shutil.make_archive(
                str(archive_path.with_suffix("")),
                "zip",
                root_dir=output_dir,
            )
        )

    zip_path = Path(
        shutil.make_archive(
            str(archive_path.with_suffix("")),
            "zip",
            root_dir=output_dir.parent,
            base_dir=output_dir.name,
        )
    )
    return zip_path


def collect_script_dirs(behavior_pack_dir: Path) -> list[Path]:
    script_dirs: list[Path] = []
    for child in sorted(behavior_pack_dir.iterdir()):
        if not child.is_dir() or is_hidden_dir(child):
            continue
        if (child / "modMain.py").is_file():
            script_dirs.append(child)
    return script_dirs


def replace_script_dirs_with_mcp(behavior_pack_dir: Path, mcp_dir: Path) -> list[Path]:
    replaced_mcps: list[Path] = []
    if not mcp_dir.is_dir():
        return replaced_mcps

    for script_dir in collect_script_dirs(behavior_pack_dir):
        source_mcp = mcp_dir / f"{script_dir.name}{MCP_SUFFIX}"
        if not source_mcp.is_file():
            continue

        _rmtree_force(script_dir)
        target_mcp = behavior_pack_dir / source_mcp.name
        if target_mcp.exists() and not _safe_unlink(target_mcp):
            raise RuntimeError(f"无法覆盖旧 .mcp 文件（可能被占用）：{target_mcp}")
        shutil.copy2(source_mcp, target_mcp)
        replaced_mcps.append(target_mcp)
    return replaced_mcps


def copy_review_template(template_root: Path, review_root: Path) -> list[Path]:
    copied_items: list[Path] = []
    if not template_root.is_dir():
        return copied_items

    for item_name in REVIEW_TEMPLATE_ITEMS:
        source = template_root / item_name
        if not source.exists():
            continue

        target = review_root / item_name
        if source.is_dir():
            if target.exists():
                _rmtree_force(target)
            shutil.copytree(source, target)
        else:
            if target.exists() and not _safe_unlink(target):
                raise RuntimeError(f"无法覆盖审核模板文件（可能被占用）：{target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        copied_items.append(target)
    return copied_items


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


def build_review_package(
    root: Path,
    output_root: Path,
    archive_template_dir: Path,
    mcp_dir: Path,
) -> None:
    start_time = time.perf_counter()
    output_dirs = prepare_output_dirs(root, output_root)
    review_behavior_used_names: set[str] = set()
    review_resource_used_names: set[str] = set()
    server_behavior_used_names: set[str] = set()
    server_resource_used_names: set[str] = set()

    pack_dirs = collect_pack_dirs(root)
    review_packaged = []
    server_packaged = []
    behavior_count = 0
    resource_count = 0
    skipped = []
    removed_count = 0
    failed_files: list[Path] = []
    replaced_mcps: list[Path] = []
    copied_review_template: list[Path] = []
    output_archives: list[Path] = []

    if BUILD_REVIEW_OUTPUT:
        copied_review_template = copy_review_template(archive_template_dir, output_dirs["review_root"])

    for pack_dir in pack_dirs:
        pack_type = read_pack_type(pack_dir / "manifest.json")
        if pack_type not in VALID_TYPES:
            skipped.append((str(pack_dir), "manifest modules 无效或未识别"))
            continue

        if BUILD_REVIEW_OUTPUT:
            review_target_dir = (
                output_dirs["review_behavior"]
                if pack_type == "data"
                else output_dirs["review_resource"]
            )
            review_used_names = (
                review_behavior_used_names
                if pack_type == "data"
                else review_resource_used_names
            )
            review_output_path, pack_removed_count, pack_failed_files, _review_name = copy_pack_dir(
                pack_dir,
                review_target_dir,
                review_used_names,
            )
            removed_count += pack_removed_count
            failed_files.extend(pack_failed_files)
            review_packaged.append((pack_dir.name, pack_type, review_output_path.name))

        if BUILD_SERVER_OUTPUT:
            server_target_dir = (
                output_dirs["server_behavior"]
                if pack_type == "data"
                else output_dirs["server_resource"]
            )
            server_used_names = (
                server_behavior_used_names
                if pack_type == "data"
                else server_resource_used_names
            )
            server_pack_dir, pack_removed_count, pack_failed_files, server_name = copy_pack_dir(
                pack_dir,
                server_target_dir,
                server_used_names,
            )
            removed_count += pack_removed_count
            failed_files.extend(pack_failed_files)

            archive_suffix = PACK_ARCHIVE_SUFFIX
            if pack_type == "data":
                pack_replaced_mcps = replace_script_dirs_with_mcp(server_pack_dir, mcp_dir)
                replaced_mcps.extend(pack_replaced_mcps)
                if pack_replaced_mcps:
                    archive_suffix = MCP_ARCHIVE_SUFFIX
            server_output_path = archive_pack_dir(
                server_pack_dir,
                server_target_dir,
                server_name,
                archive_suffix,
            )
            server_packaged.append((pack_dir.name, pack_type, server_output_path.name))

        if pack_type == "data":
            behavior_count += 1
        else:
            resource_count += 1

    if BUILD_REVIEW_OUTPUT:
        output_archives.append(archive_output_dir(output_dirs["review_root"]))
    if BUILD_SERVER_OUTPUT:
        output_archives.append(archive_output_dir(output_dirs["server_root"]))

    if review_packaged:
        print("审核用打包完成：")
        for name, pack_type, output_name in review_packaged:
            print(f"- {name} -> {pack_type}: {output_name}")
    elif BUILD_REVIEW_OUTPUT:
        print("审核用未发现可打包包。")

    if server_packaged:
        print("服务器用打包完成：")
        for name, pack_type, output_name in server_packaged:
            print(f"- {name} -> {pack_type}: {output_name}")
    elif BUILD_SERVER_OUTPUT:
        print("服务器用未发现可打包包。")

    if not BUILD_REVIEW_OUTPUT and not BUILD_SERVER_OUTPUT:
        print("未启用审核用或服务器用输出。")

    print(f"总计：行为包 {behavior_count} 个，资源包 {resource_count} 个")
    print(f"已清理 .zip/.mcp 文件：{removed_count} 个")
    print(f"服务器用已替换 .mcp 文件：{len(replaced_mcps)} 个")
    print(f"审核用已复制存档模板项：{len(copied_review_template)} 个")
    if output_archives:
        print("已生成输出压缩包：")
        for archive_path in output_archives:
            print(f"- {archive_path}")
    if failed_files:
        print("以下文件未能删除（可能被占用）：")
        for file_path in failed_files:
            print(f"- {file_path}")
    elapsed = time.perf_counter() - start_time
    print(f"输出目录：{output_root}")
    print(f"用时：{elapsed:.2f} 秒")
    if skipped:
        print("跳过：")
        for name, reason in skipped:
            print(f"- {name}: {reason}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="扫描本地目录并按类型输出审核用/服务器用行为包和资源包"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="要扫描的根目录（默认当前目录）",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"输出目录（默认 {OUTPUT_DIR}）",
    )
    parser.add_argument(
        "--archive-template-dir",
        type=Path,
        default=ARCHIVE_TEMPLATE_DIR,
        help=f"审核用存档模板目录（默认 {ARCHIVE_TEMPLATE_DIR}）",
    )
    parser.add_argument(
        "--mcp-dir",
        type=Path,
        default=MCP_DIR,
        help=f".mcp 文件目录（默认 {MCP_DIR}）",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    build_review_package(
        root,
        resolve_config_path(root, args.output_dir),
        resolve_config_path(root, args.archive_template_dir),
        resolve_config_path(root, args.mcp_dir),
    )


if __name__ == "__main__":
    main()
