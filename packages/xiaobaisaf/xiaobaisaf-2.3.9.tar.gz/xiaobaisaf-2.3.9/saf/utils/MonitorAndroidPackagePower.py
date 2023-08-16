#! /usr/bin/env python
'''
@Author: xiaobaiTser
@email : 807447312@qq.com
@Time  : 2023/6/28 20:41
@File  : MonitorAndroidPackagePowser.py
'''
import os
import re
import tkinter as tk
import subprocess
import threading
import time
from tkinter import filedialog, messagebox

import matplotlib.pyplot as plt
import csv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App:
    def __init__(self, master):
        CUR_PATH = os.path.dirname(os.path.abspath(__file__))
        self.master = master
        master.title('Android设备监控')
        master.geometry('700x500')
        master.iconbitmap(CUR_PATH + '\\..\\data\\favicon.ico')

        self.device_id = None
        self.power_data = []
        self.is_running = False

        # 创建开始、停止、导出按钮
        self.start_button = tk.Button(master, text='开始', command=self.start)
        self.start_button.pack(side='left', padx=10, pady=10)

        self.stop_button = tk.Button(master, text='停止', command=self.stop)
        self.stop_button.pack(side='left', padx=10, pady=10)

        self.export_button = tk.Button(master, text='导出', command=self.export)
        self.export_button.pack(side='left', padx=10, pady=10)

        # 创建tkinter标签，用于显示最新的电量数据
        self.label_power = tk.Label(master, text='设备当前电量：')
        self.label_power.pack(side='bottom', padx=2, pady=2)
        # 创建tkinter标签，用于显示最新的内存数据
        self.label_memory_rate = tk.Label(master, text='内存使用率：')
        self.label_memory_rate.pack(side='bottom', padx=2, pady=2)
        # 创建tkinter标签，用于显示最新的CPU数据
        self.label_cpu_rate = tk.Label(master, text='CPU使用率：')
        self.label_cpu_rate.pack(side='bottom', padx=2, pady=2)
        # 创建tkinter标签，用于显示最新的FPS数据
        self.label_fps_rate = tk.Label(master, text='FPS刷新率：')
        self.label_fps_rate.pack(side='bottom', padx=2, pady=2)

        # 创建matplotlib图形区域
        self.fig = plt.figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Time(s)')
        self.ax.set_ylabel('Rate(%)')
        self.ax.set_xlim(0, 30)
        self.ax.set_ylim(0, 100)

        # 创建tkinter绘图区域
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    def start(self):
        self.start_time = time.time()
        if not self.is_running:
            self.is_running = True
            self.device_id = subprocess.check_output(['adb', 'devices']).decode('utf-8').split('\n')[1].split('\t')[0]
            self.total_memory = \
                subprocess.check_output(['adb', 'shell', 'cat', '/proc/meminfo', '|', 'grep', '"MemTotal"']).decode(
                    'utf-8').split()[1]
            self.power_data = []
            self.app_memory_data = []
            self.app_cpu_data = []
            self.app_fps_data = []

            # 在后台启动一个线程来获取数据
            self.power_thread = threading.Thread(target=self.get_data)
            self.power_thread.start()

    def stop(self):
        self.is_running = False

    def export(self):
        # 弹出文件对话框，获取用户选择的文件名和存储位置
        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=(("CSV文件", "*.csv"),))
        if file_path:
            try:
                # 合并数据
                merged_list = [(a[0], a[1], b[0], b[1], c, d) for a, b, c, d in zip(self.power_data,
                                                                                 self.app_memory_data,
                                                                                 self.app_cpu_data,
                                                                                 self.app_fps_data)]
                # 导出电量数据到CSV文件
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows([('运行时间（秒）', '设备电量（%）', '应用程序包名', '内存使用率（%）', 'CPU使用率（%）',
                                       'FPS（帧/秒）')])
                    writer.writerows(merged_list)
                messagebox.showinfo("小白提醒：", "数据已经保存完成！")
            except PermissionError:
                messagebox.showerror("小白提示：", "文件无法访问！文件是否打开？请先关闭后重新尝试！")

    def get_data(self):
        while self.is_running:
            # 电量
            power_output = subprocess.check_output(['adb', '-s', self.device_id, 'shell', 'dumpsys', 'battery', '|',
                                                    'grep', 'level']).decode('utf-8').strip()
            power_level = int(power_output.split(':')[1])
            self.power_data.append((int(time.time()-self.start_time), power_level))

            package_name = \
                subprocess.check_output(['adb', 'shell', 'dumpsys', 'window', '|', 'grep', 'mCurrentFocus']).decode(
                    'utf-8')
            if 'mCurrentFocus=null' in package_name:
                status = messagebox.askyesno("小白提示：", "存在熄屏或者切换APP的行为！获取数据期间尽量不要切换或者熄屏！")
                if status:
                    try:
                        subprocess.check_output(['adb', 'shell', 'settings', 'put', 'system', 'screen_off_timeout',
                                                 '-1'])
                    except Exception:
                        messagebox.showerror('小白错误提示：', '设置失败！')
                else:

                    exit(0)
            else:
                package_name = package_name.split()[2].split('/')[0]
                package_pid = subprocess.check_output(['adb', 'shell', 'ps', '|', 'grep', package_name]).decode(
                        'utf-8')
                app_package_pid = ''
                for pid in package_pid.split('\r\n'):
                    if package_name in pid.split():
                        app_package_pid = pid.split()[1]
                        break

                # 内存
                result = subprocess.run(['adb', 'shell', 'dumpsys', 'meminfo', app_package_pid], capture_output=True,
                                        text=True)
                memory_output = result.stdout
                # 解析输出，获取当前打开的APP的内存使用情况
                lines = memory_output.split('\n')
                for line in lines:
                    if 'TOTAL' in line:
                        app_memory_usage = line.split()[1]
                        self.app_memory_data.append(
                            (package_name, round(int(app_memory_usage) * 100 / int(self.total_memory), 1)))
                        break

                # CPU
                output = subprocess.check_output(["adb", "shell", "top", "-n", "1", "-d", "1", "-p",
                                                  app_package_pid]).decode("utf-8")
                lines = output.strip().split("\n")
                if len(lines) >= 2:
                    # 提取CPU使用率数据
                    cpu_line = lines[-1]
                    try:
                        self.app_cpu_data.append(float(cpu_line.split()[8]))
                    except Exception as e:
                        self.app_cpu_data.append(0.0)

                # 获取FPS数据
                output = subprocess.check_output(
                    ["adb", "shell", "dumpsys", "gfxinfo", package_name, "framestats"]).decode("utf-8")
                lines = output.strip().split("\r\n")
                janky_frames_line = [x for x in lines if 'Janky frames:' in x][0] \
                    if len([x for x in lines if 'Janky frames:' in x]) > 0 \
                    else '(0.0%)'
                janky_frames = float(re.findall('\((.*?)%\)', janky_frames_line)[0])
                self.app_fps_data.append(int(60 * (1 - janky_frames / 100)))

                # 其他数据...

                self.update_data()
                time.sleep(1)

    def update_data(self):
        # 更新图表数据和电量标签
        if self.power_data:
            self.ax.clear()
            self.ax.set_xlabel('Time(s)')
            self.ax.set_ylabel('Rate(%)')
            if self.power_data[-1][0] > 30:
                self.ax.set_xlim(max(0, self.power_data[-1][0] - 30), self.power_data[-1][0] + 1)
            else:
                self.ax.set_xlim(0, 30)
            self.ax.set_ylim(0, 100)

            if len(self.ax.lines) > 0:
                self.ax.lines.pop(0)
            if self.power_data[-1][0] > 30:
                self.ax.plot([t for t, _ in self.power_data[-30:]], [p for _, p in self.power_data[-30:]])
                self.ax.plot([t for t, _ in self.power_data[-30:]], [p for _, p in self.app_memory_data[-30:]])
                self.ax.plot([t for t, _ in self.power_data[-30:]], [p for p in self.app_cpu_data[-30:]])
                self.ax.plot([t for t, _ in self.power_data[-30:]], [p for p in self.app_fps_data[-30:]])
            else:
                self.ax.plot([t for t, _ in self.power_data], [p for _, p in self.power_data])
                self.ax.plot([t for t, _ in self.power_data], [p for _, p in self.app_memory_data])
                self.ax.plot([t for t, _ in self.power_data], [p for p in self.app_cpu_data])
                self.ax.plot([t for t, _ in self.power_data], [p for p in self.app_fps_data])
            self.canvas.draw()
            # 更新电量标签
            current_power = self.power_data[-1][1]
            current_memory_rate = self.app_memory_data[-1][1]
            current_cpu_rate = self.app_cpu_data[-1]
            current_fps_rate = self.app_fps_data[-1]
            self.label_power.config(text=f'设备当前电量[蓝线]：{current_power}%')
            self.label_memory_rate.config(text=f'内存使用率[橙线]：{current_memory_rate}%')
            self.label_cpu_rate.config(text=f'CPU使用率[绿线]：{current_cpu_rate}%')
            self.label_fps_rate.config(text=f'FPS刷新率[红线]：{current_fps_rate}/s')

def power():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# if __name__ == '__main__':
#     power()