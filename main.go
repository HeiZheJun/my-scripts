package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"flag"
)


// 进程参数
type PidInfo struct {
	Pid				int   	//进程id
	ProcessName		string	//进程名称
	ExeLink  		string	//对应的可执行文件
}

// 接收参数
type Config struct {
	SearchPath string
	SearchFile string
}


func getArgs() Config {
	var cfg Config
	var showHelp bool

	// 1. 覆盖默认的 flag.Usage，自定义输出格式
	flag.Usage = func() {
		execName := os.Args[0]
		fmt.Println("🔍 查找特定路径的进程")
		fmt.Println()
		fmt.Printf("Usage: %s [options]\n", execName)
		fmt.Println()
		fmt.Println("Options:")
		fmt.Println("  -p, --path string   只显示 exe 文件在指定目录下的进程")
		fmt.Println("  -f, --file string   只显示 exe 文件是指定文件的进程")
		fmt.Println("  -h, --help          显示帮助信息")
		fmt.Println()
		fmt.Println("示例:")
		fmt.Printf("  %s -p /usr/bin\n", execName)
		fmt.Printf("  %s -f /bin/bash\n", execName)
	}

	// 2. 将短参数与长参数同时绑定到同一个变量
	flag.StringVar(&cfg.SearchPath, "p", "", "只显示 exe 文件在指定目录下的进程")
	flag.StringVar(&cfg.SearchPath, "path", "", "只显示 exe 文件在指定目录下的进程")

	flag.StringVar(&cfg.SearchFile, "f", "", "只显示 exe 文件是指定文件的进程")
	flag.StringVar(&cfg.SearchFile, "file", "", "只显示 exe 文件是指定文件的进程")

	flag.BoolVar(&showHelp, "h", false, "显示帮助信息")
	flag.BoolVar(&showHelp, "help", false, "显示帮助信息")

	flag.Parse()

	// 3. 如果用户传了 -h 或 --help，打印帮助信息并退出程序
	if showHelp {
		flag.Usage()
		os.Exit(0)
	}

	return cfg
}

// 获取所有pid
func getPids() ([]int, error) {
	driect, err := os.ReadDir("/proc")
	
	var pids []int
	if err != nil {
		return nil, fmt.Errorf("获取失败: %w", err)
	}
	for _, entry := range driect {
		if entry.IsDir() {
			// strconv.Atoi 返回 int 类型
			if pid, err := strconv.Atoi(entry.Name()); err == nil {
				pids = append(pids, pid)
			}
		}
	}
	return pids, nil
}

// 获取pid的可执行文件连接，程序名称
func getExeLink() ([]PidInfo, error) {
    pids, err := getPids()
    if err != nil {
        return nil, fmt.Errorf("获取PID列表失败: %v", err)
    }

    var pidInfos []PidInfo
    for _, pid := range pids {
        // 读取进程名
        commBytes, err := os.ReadFile(fmt.Sprintf("/proc/%d/comm", pid))
        if err != nil {
            continue // 忽略无法读取的进程
        }
		processName := strings.TrimSpace(string(commBytes))

        // 读取exe链接
        exe := fmt.Sprintf("/proc/%d/exe", pid)
        link, err := os.Readlink(exe)
        if err != nil {
            // 如果无法读取exe链接，标记错误信息
            link = ""
        }

        pidInfos = append(pidInfos, PidInfo{
            Pid:        pid,
            ProcessName: processName,
            ExeLink:    link,
        })
    }
    return pidInfos, nil
}



func BeautyPrint( info PidInfo) {
	fmt.Printf("🟢 PID: \033[1;35m%d\033[0m\n", info.Pid)
	fmt.Printf("   ├─ 进程名: \033[1;33m%s\033[0m\n", info.ProcessName)
	fmt.Printf("   └─ 可执行文件: \033[1;36m%s\033[0m\n", info.ExeLink)
	fmt.Println("\033[22----------------------------------------\033[0m")

}


func main() {
	cfg := getArgs()

	infos ,err := getExeLink() 
	if err != nil {
		fmt.Errorf("获取PID列表失败: %v", err)
		return
	}
	if cfg.SearchPath == "" &&  cfg.SearchFile == "" {
		for _ ,info  :=  range infos {
			BeautyPrint(info)
		}
	}

}
