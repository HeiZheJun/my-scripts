#!/bin/bash
# 简单检查进程可执行文件的脚本
# 作用：显示进程对应的可执行文件的地址，判断是否是正常进程
# 后续：链接病毒库，根据文件路径，文件校验码判断是否是木马进程


# 全局变量声明
file_path=""

help_info() {
    # 彩色定义
    local GREEN="\033[32m"
    local YELLOW="\033[33m"
    local BLUE="\033[34m"
    local RED="\033[31m"
    local RESET="\033[0m"
    echo -e "${GREEN}🛠️ 使用方法:${RESET}"
    echo -e "  ${YELLOW}$0 [选项]${RESET}"
    echo
    echo -e "${GREEN}📌 功能说明:${RESET}"
    echo -e "  这是一个自动化脚本，用于实现查看进程可执行文件，用于判断进程是否是木马进程"
    echo
    echo -e "${GREEN}⚙️ 选项:${RESET}"
    echo -e "  ${BLUE}-f, --file${RESET}    显示查看进程可执行文件对应的文件地址，默认是所有地址文件都显示"
    echo -e "  ${BLUE}-h, --help${RESET}    显示本帮助信息"
    echo
    echo -e "${GREEN}📝 示例:${RESET}"
    echo -e "  ${YELLOW}$0 -f /path/to/config${RESET}"
    echo -e "  ${YELLOW}$0 --help${RESET}"
}

check_args() {
    if [[ $# -eq 0 ]]; then
        file_path="/*"
    elif [[ $# -gt 2 ]]; then
        help_info
        exit 1
    elif [[ "$1" == "-f" || "$1" == "--file" ]]; then
        file_path="$2"
    elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
        help_info
        exit 0
    else
        help_info
        exit 1
    fi
}

check_exe_readline_path() {
    if [[ "$file_path" == "/*" ]]; then
        echo -e "[🔍] 检查所有进程可执行文件路径..."
        echo -e "----------------------------------------"
    elif [[ -f "$file_path" ]]; then
        echo -e "[🔍] 检查可执行文件为${file_path}的进程..."
        echo -e "----------------------------------------"
    elif [[ -d "$file_path" ]]; then
        echo -e "[🔍] 检查可执行路径为${file_path}的进程..."
        echo -e "----------------------------------------"
        file_path="${file_path}/*"
    else
        echo -e "[❌] 错误：${file_path} 不存在！"
        exit 1
    fi
}

check_pid() {
    # 进程计数器    
    local count=0

    # 遍历 /proc 下的所有数字目录（即进程 PID）
    for pid in $(ls /proc | grep -P '^\d+$'); do
        # 获取进程的二进制执行文件路径
        exe_path=$(readlink -f "/proc/${pid}/exe" 2>/dev/null)

        # 检查进程执行文件路径是否匹配
        if [[ -n "$exe_path" ]]; then
            case "$file_path" in
                "/*")
                    # 显示所有进程
                    print_process_info "$pid" "$exe_path"
                    ((count++))
                    ;;
                *)
                    # 检查路径是否匹配
                    if [[ "$exe_path" == "$file_path" || "$exe_path" == "$file_path"* ]]; then
                        print_process_info "$pid" "$exe_path"
                        ((count++))
                    fi
                    ;;
            esac
        fi
    done

    if [[ $count -eq 0 ]]; then
        echo -e "✅ 没有发现任何进程关联到 ${file_path} 的可执行文件"
    else
        echo -e "⚠️ 共发现 \033[1;31m${count}\033[0m 个进程关联到 ${file_path} 的可执行文件！"
    fi
}

print_process_info() {
    local pid=$1
    local exe_path=$2
    local process_name=$(cat "/proc/${pid}/comm" 2>/dev/null)
    
    echo -e "🟢 PID: \033[1;35m${pid}\033[0m"
    echo -e "   ├─ 进程名: \033[1;33m${process_name}\033[0m"
    echo -e "   └─ 可执行文件: \033[1;36m${exe_path}\033[0m"
    echo -e "----------------------------------------"
}

# 主执行流程
check_args "$@"
check_exe_readline_path
check_pid
