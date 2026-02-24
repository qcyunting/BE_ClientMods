#!/bin/bash

REMOTE_HOST="${REMOTE_HOST}"
REMOTE_USER="${REMOTE_USER}"
REMOTE_PORT="${REMOTE_PORT:-22}"
REMOTE_PATH="/home/fuzhu/vc/plugins/Geyser-Velocity/git"
SSH_PASSPHRASE="${SSH_PASSPHRASE}"

LOG_FILE="deploy.log"

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" | tee -a "$LOG_FILE"
}

log_info() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1"
}

SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_rsa}"

ssh_exec() {
    expect -c "
    set timeout 60
    spawn ssh -o StrictHostKeyChecking=no -i $SSH_KEY -p $REMOTE_PORT $REMOTE_USER@$REMOTE_HOST \"\$1\"
    expect {
        \"passphrase\" {
            send \"${SSH_PASSPHRASE}\r\"
            expect {
                \"#\" { send \"exit\r\" }
                \"$\" { send \"exit\r\" }
            }
        }
        \"#\" { send \"exit\r\" }
        \"$\" { send \"exit\r\" }
    }
    expect eof
    "
}

log_info "开始部署流程"

log_info "清理远程目录: $REMOTE_PATH"
ssh_exec "rm -rf $REMOTE_PATH/*" || log_error "清理远程目录失败"

log_info "同步代码到远程服务器"
rsync -avz -e "ssh -o StrictHostKeyChecking=no -i $SSH_KEY -p $REMOTE_PORT" --exclude '.git' ./ "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/" || {
    log_error "代码同步失败"
    exit 1
}

log_info "创建modszip目录结构"
ssh_exec "mkdir -p $REMOTE_PATH/modszip/packs/BehaviorPacks $REMOTE_PATH/modszip/packs/ResourcePacks"

MOD_DIRS=("LobbyMod" "XiGuaNPCMod" "CommonMod" "HyperClashMod" "ShadowMod" "HongBaoMod" "LobbyMod_old")

for mod_dir in "${MOD_DIRS[@]}"; do
    mod_path="$REMOTE_PATH/$mod_dir"
    
    if ssh_exec "[ ! -d $mod_path/behavior_packs ]" 2>/dev/null; then
        log_error "$mod_dir: behavior_packs目录不存在"
        continue
    fi
    
    bp_count=$(ssh_exec "ls -1 $mod_path/behavior_packs/ 2>/dev/null | wc -l")
    if [ "$bp_count" -eq 0 ]; then
        log_error "$mod_dir: behavior_packs目录为空"
        continue
    fi
    
    for bp_subdir in $(ssh_exec "ls -1 $mod_path/behavior_packs/"); do
        bp_full_path="$mod_path/behavior_packs/$bp_subdir"
        if ssh_exec "[ ! -d $bp_full_path ]"; then
            log_error "$mod_dir/behavior_packs/$bp_subdir: 不是有效目录"
            continue
        fi
        
        log_info "压缩 $mod_dir/behavior_packs/$bp_subdir -> BehaviorPacks/$bp_subdir.zip"
        ssh_exec "cd $bp_full_path && zip -r $REMOTE_PATH/modszip/packs/BehaviorPacks/$bp_subdir.zip ./*" || {
            log_error "压缩 $mod_dir/behavior_packs/$bp_subdir 失败"
        }
    done
    
    if ssh_exec "[ ! -d $mod_path/resource_packs ]" 2>/dev/null; then
        log_error "$mod_dir: resource_packs目录不存在"
        continue
    fi
    
    rp_count=$(ssh_exec "ls -1 $mod_path/resource_packs/ 2>/dev/null | wc -l")
    if [ "$rp_count" -eq 0 ]; then
        log_error "$mod_dir: resource_packs目录为空"
        continue
    fi
    
    for rp_subdir in $(ssh_exec "ls -1 $mod_path/resource_packs/"); do
        rp_full_path="$mod_path/resource_packs/$rp_subdir"
        if ssh_exec "[ ! -d $rp_full_path ]"; then
            log_error "$mod_dir/resource_packs/$rp_subdir: 不是有效目录"
            continue
        fi
        
        log_info "压缩 $mod_dir/resource_packs/$rp_subdir -> ResourcePacks/$rp_subdir.zip"
        ssh_exec "cd $rp_full_path && zip -r $REMOTE_PATH/modszip/packs/ResourcePacks/$rp_subdir.zip ./*" || {
            log_error "压缩 $mod_dir/resource_packs/$rp_subdir 失败"
        }
    done
done

log_info "部署完成"
