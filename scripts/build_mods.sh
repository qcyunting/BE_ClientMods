#!/bin/bash

set -e

MODS_DIR="${MODS_DIR:-/data/mods}"
OUTPUT_DIR="${OUTPUT_DIR:-/data/modszip}"
PACK_TYPES=("BehaviorPacks" "ResourcePacks" "OptionalResourcePacks")

log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $1" >&2
}

log_info "开始打包流程"
log_info "源目录: $MODS_DIR"
log_info "输出目录: $OUTPUT_DIR"

log_info "清理输出目录: $OUTPUT_DIR"
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

if [ ! -d "$MODS_DIR" ]; then
    log_error "源目录不存在: $MODS_DIR"
    exit 1
fi

for mod_dir in "$MODS_DIR"/*/; do
    if [ ! -d "$mod_dir" ]; then
        continue
    fi
    
    mod_name=$(basename "$mod_dir")
    log_info "处理 Mod: $mod_name"
    
    for pack_type in "${PACK_TYPES[@]}"; do
        pack_path="$mod_dir$pack_type"
        
        if [ ! -d "$pack_path" ]; then
            log_error "目录不存在，跳过: $pack_path"
            continue
        fi
        
        if [ -z "$(ls -A "$pack_path" 2>/dev/null)" ]; then
            log_error "目录为空，跳过: $pack_path"
            continue
        fi
        
        output_file="$OUTPUT_DIR/${mod_name}_${pack_type}.zip"
        log_info "压缩: $pack_path -> $output_file"
        
        if (cd "$pack_path" && zip -r "$output_file" .); then
            log_info "成功: $output_file"
        else
            log_error "压缩失败: $pack_path"
        fi
    done
done

log_info "打包完成，输出文件列表:"
ls -lh "$OUTPUT_DIR"
