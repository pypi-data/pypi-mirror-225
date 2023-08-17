#!/usr/bin/python3
import tkinter as tk
from tkinter import filedialog, simpledialog, Checkbutton, IntVar,ttk
import os
import glob
import subprocess
import paramiko
import time
import threading

# 创建窗口
window = tk.Tk()
window.title("测试工具")

# 创建标签
label = tk.Label(window, text="请输入设备序列号（SN）:")
label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

# 创建输入框
entry = tk.Entry(window)
entry.grid(row=0, column=1, padx=10, pady=10)

# 浏览按钮点击事件
def browse_sn_file():
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)
# 创建浏览按钮
browse_button = tk.Button(window, text="浏览", command=browse_sn_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

# 查看测试日志按钮点击事件
def view_log():
    # 获取当前目录中所有符合特定模式的文件
    log_files = glob.glob("summary_report_*.txt")

    # 根据文件创建时间对文件进行排序
    log_files.sort(key=os.path.getctime, reverse=True)
    # 获取最新的日志文件名
    if log_files:
        latest_log_file = log_files[0]
        subprocess.run(["mousepad", latest_log_file])  # 使用 vim 打开日志文件
    else:
        print("未找到日志文件")

# 创建查看日志按钮
view_log_button = tk.Button(window, text="查看测试日志", command=view_log)
view_log_button.grid(row=2, column=0, padx=10, pady=10)

# 终止测试按钮点击事件
test_process = None

def stop_tests():
    global test_process
    if test_process:
        test_process.terminate()
        progress.stop()  # 停止进度条加载
        print("终止测试按钮被点击")

# 创建终止测试按钮
stop_button = tk.Button(window, text="终止测试", command=stop_tests)
stop_button.grid(row=1, column=1, padx=10, pady=10)

# 创建进度条
#progress = ttk.Progressbar(window, orient="horizontal", length=300, mode="determinate")
# 布局进度条
#progress.grid(row=5, column=0, columnspan=3, padx=10, pady=10)


# 运行测试按钮点击事件
def run_tests():
    global test_process
    #def update_progress():
     #   while test_process.poll() is None:  # 循环直到子进程结束
        # 读取测试脚本的输出并解析进度值
      #      line = test_process.stdout.readline().decode("utf-8").strip()
       #     if line.startswith("Progress:"):
        #        progress_value = int(line.split(":")[1])
         #       progress["value"] = progress_value
          #      window.update_idletasks()  # 刷新窗口
           # time.sleep(0.1)  # 模拟进度更新的延迟
    sn = entry.get()
    # 获取所选的网络接口
    selected_interfaces = [interface_types[i] for i, var in enumerate(interface_vars) if var.get() == 1]

    # 构建运行测试命令，同时传递选择的网络接口作为参数
    command = ["./sum_test_pro.sh", sn] + selected_interfaces
    test_process = subprocess.Popen(command)

    # 在后台运行更新进度的循环
    #threading.Thread(target=update_progress).start()

    print("运行测试，SN:", sn, "选择的接口类型:", selected_interfaces)

# 创建运行按钮
run_button = tk.Button(window, text="运行测试", command=run_tests)
run_button.grid(row=1, column=0, padx=10, pady=10)

# 创建上传至 NAS 按钮点击事件
def upload_to_nas():
    # 创建一个弹窗
    nas_dialog = tk.Toplevel(window)
    nas_dialog.title("NAS信息")

    # 添加标签和输入框用于填写 NAS 信息
    tk.Label(nas_dialog, text="NAS IP地址:").grid(row=0, column=0, padx=10, pady=10)
    nas_ip_entry = tk.Entry(nas_dialog)
    nas_ip_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(nas_dialog, text="用户名:").grid(row=1, column=0, padx=10, pady=10)
    nas_user_entry = tk.Entry(nas_dialog)
    nas_user_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(nas_dialog, text="密码:").grid(row=2, column=0, padx=10, pady=10)
    nas_password_entry = tk.Entry(nas_dialog, show="*")
    nas_password_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(nas_dialog, text="目标路径:").grid(row=3, column=0, padx=10, pady=10)
    nas_destination_entry = tk.Entry(nas_dialog)
    nas_destination_entry.grid(row=3, column=1, padx=10, pady=10)

    # 创建确认按钮点击事件
    def confirm_upload():
        nas_ip = nas_ip_entry.get()
        nas_user = nas_user_entry.get()
        nas_password = nas_password_entry.get()
        nas_destination = nas_destination_entry.get()

        nas_dialog.destroy()  # 关闭弹窗

        # 在此执行上传至 NAS 的操作
        if nas_ip and nas_user and nas_password and nas_destination:
            # 获取最新的日志文件名
            log_files = glob.glob("summary_report_*.txt")
            log_files.sort(key=os.path.getctime, reverse=True)
            if log_files:
                newest_log_file = log_files[0]
            else:
                print("未找到日志文件")
                return

            # 使用SSH客户端连接至NAS
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(nas_ip, username=nas_user, password=nas_password)

            # 创建SFTP客户端
            sftp = ssh.open_sftp()

            try:
                # 将日志文件上传至NAS
                sftp.put(newest_log_file, os.path.join(nas_destination, newest_log_file))
                print("日志文件上传至NAS成功")
            except Exception as e:
                print("日志文件上传至NAS失败:", e)
            finally:
                # 关闭SFTP连接
                sftp.close()

            # 关闭SSH连接
            ssh.close()

    # 创建确认按钮
    confirm_button = tk.Button(nas_dialog, text="确认", command=confirm_upload)
    confirm_button.grid(row=4, columnspan=2, padx=10, pady=10)


# 创建上传至 NAS 按钮
upload_button = tk.Button(window, text="上传至 NAS", command=upload_to_nas)
upload_button.grid(row=2, column=1, padx=10, pady=10)

# 提示选择网络接口类型
interface_label = tk.Label(window, text="请选择网络接口类型:")
interface_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)

# 创建多选框列表
interface_types = ["eth0", "eth1", "wlan0", "enp2s0"]
interface_vars = [tk.IntVar() for _ in interface_types]
checkboxes = [Checkbutton(window, text=interface_types[i], variable=interface_vars[i]) for i in range(len(interface_types))]

# 布局多选框
for i, checkbox in enumerate(checkboxes):
    checkbox.grid(row=4, column=i, padx=10, pady=5)

# 运行窗口
window.mainloop()
