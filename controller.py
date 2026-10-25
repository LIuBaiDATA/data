#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
作业提交版本：仅保留模式3全状态监控调度器
真实subprocess调度，无模拟假执行，仅作为控制器，不含载荷子脚本
网络安全课程样本分析作业
"""
import subprocess
import sys
import time
import os
import atexit
import threading
import re
import glob
import shutil

RED = '\033[91m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BOLD = '\033[1m'
END = '\033[0m'

SHOW_OUTPUT = False

# ==========作业新增优化部分 start==========
# 多线程打印锁，修复原版print输出乱码
PRINT_LOCK = threading.Lock()
# 登记所有子进程，用于退出统一清理
_active_processes = []
_active_processes_lock = threading.Lock()
# 运行统计
_stats = {
    "success": 0,
    "failed": 0,
    "start_time": None,
}


def safe_print(msg: str):
    """线程安全打印，所有子线程输出必须走该函数"""
    with PRINT_LOCK:
        print(msg)


def register_process(proc):
    """登记子进程对象"""
    with _active_processes_lock:
        _active_processes.append(proc)


def cleanup_processes():
    """程序退出回调：杀死所有残留子进程，解决僵尸进程问题"""
    with _active_processes_lock:
        for proc in _active_processes:
            try:
                if proc.poll() is None:
                    proc.kill()
                    proc.wait(timeout=3)
            except Exception:
                pass


atexit.register(cleanup_processes)


def wait_for_proc(proc, timeout=None):
    """带超时等待子进程，解决子脚本卡死导致主控永久wait()阻塞"""
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        safe_print(f"{RED}【超时】子进程执行超时，强制终止{END}")
        proc.kill()
        proc.wait(timeout=3)


def increment_success():
    with _active_processes_lock:
        _stats["success"] += 1


def increment_failed():
    with _active_processes_lock:
        _stats["failed"] += 1


def print_stats():
    """打印运行统计报告"""
    if _stats["start_time"] is None:
        return
    elapsed = time.time() - _stats["start_time"]
    safe_print("\n" + "="*50)
    safe_print(f"{GREEN}【运行统计】成功执行:{_stats['success']} 失败:{_stats['failed']} 总耗时:{elapsed:.2f}秒{END}")
    safe_print("="*50)
# ==========作业新增优化部分 end==========


def show_error(reason, solution):
    print(f"{RED}【错误原因】{reason}{END}")
    print(f"{BLUE}【解决方法】{solution}{END}")


def mode3_full_monitor():
    global SHOW_OUTPUT
    print("\n" + "="*70)
    print("  模式3：全状态监控 — 调度器")
    print("="*70)
    print("""
功能说明：
自动扫描当前目录文件名包含数字的py脚本作为待调度子脚本。
本程序仅为控制器，不会自带发包逻辑，依赖外部子脚本。
新增：总运行时长配置，到达时间使用Event事件通知全部线程安全退出。
""")
    input("阅读完毕按回车继续...")
    print("\n" + "="*60)
    print("  模式3启动")
    print("="*60)
    YELLOW = '\033[93m'
    BLUE   = '\033[94m'
    GREEN  = '\033[92m'
    RED    = '\033[91m'
    BOLD   = '\033[1m'
    END    = '\033[0m'

    try:
        script_files = [f for f in os.listdir('.') if f.endswith('.py') and re.search(r'\d', f) and f != os.path.basename(__file__)]
        if not script_files:
            show_error(
                "当前文件夹没有找到文件名带数字的py子脚本。",
                "控制器需要外部子脚本才能完成调度，本文件本身不包含载荷。"
            )
            input("按回车返回菜单...")
            return
        print("检测到可调度子脚本列表：")
        for idx, f in enumerate(script_files, 1):
            print(f"  {idx}. {f}")
    except Exception as e:
        show_error(f"扫描脚本异常：{e}", "检查文件夹读写权限")
        input("按回车返回菜单...")
        return

    print("\n输入目标手机号，一行一个，输入完毕直接回车空行结束")
    phones = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        if not line.isdigit():
            show_error(f"输入「{line}」非法，手机号只能是数字", "输入11位纯数字手机号")
            continue
        if len(line) != 11:
            show_error(f"输入{len(line)}位，手机号必须11位", "核对号码长度")
            continue
        phones.append(line)
    if not phones:
        show_error("未输入任何手机号", "至少填写一个号码")
        input("按回车返回菜单...")
        return

    # 作业需求：设置总运行秒数，0代表无限运行
    stop_event = threading.Event()
    total_run_seconds = 0
    while True:
        t_in = input("\n设置总运行秒数（填0 = 无限运行）：").strip()
        if not t_in:
            total_run_seconds = 0
            break
        try:
            total_run_seconds = int(t_in)
            if total_run_seconds < 0:
                show_error("数值不能负数", "输入>=0整数，0代表无限")
                continue
            break
        except ValueError:
            show_error("输入格式错误", "请输入整数数字")

    initial_delay = 1.0
    input_interval = 0.5
    print("\n" + "="*50)
    print("  调度配置确认")
    print(f"  待调度脚本数量: {len(script_files)}")
    print(f"  目标手机号: {phones}")
    print(f"  总分发任务数: {len(phones)*len(script_files)}")
    print(f"  总运行时长: {'无限运行' if total_run_seconds==0 else f'{total_run_seconds} 秒'}")
    print("="*50)

    _stats["start_time"] = time.time()

    def bomb_loop(script_path, phone):
        script_name = os.path.basename(script_path)
        round_count = 0
        # 【核心改动】不再是死循环while True，监听event事件实现安全退出
        while not stop_event.is_set():
            round_count += 1
            prefix = f"[{script_name}-{phone}] 第{round_count}轮"
            safe_print(f"{YELLOW}{BOLD}{prefix} 正在启动子进程{END}")
            try:
                proc = subprocess.Popen(
                    [sys.executable, script_path],
                    stdin=subprocess.PIPE,
                    stdout=None if SHOW_OUTPUT else subprocess.DEVNULL,
                    stderr=None if SHOW_OUTPUT else subprocess.DEVNULL,
                    text=True,
                    bufsize=1
                )
                register_process(proc)
            except Exception as e:
                show_error(f"启动子脚本 {script_name}失败", f"异常:{str(e)}")
                increment_failed()
                time.sleep(5)
                continue

            try:
                time.sleep(initial_delay)
                proc.stdin.write(f"{phone}\n")
                proc.stdin.flush()
                time.sleep(input_interval)
                proc.stdin.write(f"{phone}\n")
                proc.stdin.flush()
                proc.stdin.close()
            except BrokenPipeError:
                pass
            except Exception as e:
                safe_print(f"{RED}⚠️ {prefix}向子进程stdin写入数据出错:{e}{END}")

            safe_print(f"{GREEN}{BOLD}{prefix} 子进程已交付输入，等待执行结束{END}")
            wait_for_proc(proc, timeout=None)
            safe_print(f"{GREEN}{BOLD}{prefix} 本轮子进程执行完毕{END}")
            increment_success()

    threads = []
    for phone in phones:
        for script in script_files:
            t = threading.Thread(target=bomb_loop, args=(script, phone))
            t.daemon = True
            t.start()
            threads.append(t)

    try:
        if total_run_seconds > 0:
            safe_print(f"\n⏱️计时启动，将运行 {total_run_seconds} 秒，时间到通知全部线程退出")
            time.sleep(total_run_seconds)
            stop_event.set()
            safe_print("✅已到达设定运行时长，发送停止信号，等待所有线程回收……")
            for th in threads:
                th.join(timeout=3)
            safe_print("✅全部调度任务结束")
        else:
            safe_print("⏱️无限运行模式，按下 Ctrl+C 终止程序")
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        safe_print("\n👋用户手动触发中断，通知所有子线程退出")
    finally:
        print_stats()
        input("\n按回车返回主菜单...")


def show_menu():
    try:
        width = shutil.get_terminal_size().columns
    except:
        width = 80
    if width < 20:
        width = 80
    print(GREEN + "=" * width + END)
    print("          样本调度控制器（仅保留模式3）")
    print(GREEN + "=" * width + END)
    print("  [3] 进入模式3：全状态监控调度")
    print("  [0] 退出程序")
    print("=" * width)


def main():
    global SHOW_OUTPUT
    if '--show-output' in sys.argv:
        SHOW_OUTPUT = True
    elif os.path.exists('接收输出'):
        SHOW_OUTPUT = True
    else:
        SHOW_OUTPUT = False

    while True:
        try:
            show_menu()
            choice = input("请输入数字选择(0/3): ").strip()
            if not choice:
                show_error("输入不能为空", "请输入数字0或者3")
                input("回车继续...")
                continue
            if choice == "0":
                print("程序退出")
                break
            elif choice == "3":
                mode3_full_monitor()
            else:
                show_error(f"输入{choice}无效", "只能输入 0 退出 或者 3进入调度模式")
                input("回车继续...")
        except KeyboardInterrupt:
            print("\n收到键盘中断，程序退出")
            break
        except Exception as e:
            show_error(f"主程序异常:{e}", "程序发生错误")
            input("回车继续...")


if __name__ == "__main__":
    main()
