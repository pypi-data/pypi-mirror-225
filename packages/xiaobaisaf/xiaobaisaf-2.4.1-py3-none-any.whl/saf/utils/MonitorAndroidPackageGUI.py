#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/12 0:46
@File  : MonitorDriver.py
'''
import getpass
import os
import re
import subprocess
import copy
from lxml import etree
import tkinter as tk
import threading
import time
from adbutils import adb

USERHOMEDIR = f'C:\\Users\\{getpass.getuser()}'

UI_DUMP_FILE = f'{USERHOMEDIR}\\window_dump.xml'

class App:
    def __init__(self, master):
        self.master = master
        self.device_var = tk.StringVar()
        self.app_var = tk.StringVar()
        self.text_var = tk.StringVar()
        self.create_widgets()
        self.start_threads()
        self.master.protocol("WM_DELETE_WINDOW", self.stop_threads)


    def create_widgets(self):
        # 创建下拉框
        self.device_label = tk.Label(self.master, text="设备号:")
        self.device_label.grid(row=0, column=0)
        devices = adb.device_list()
        device_list = [d.serial for d in devices]
        self.device_var.set(device_list[0])
        self.device_option = tk.OptionMenu(self.master, self.device_var, *device_list)
        self.device_option.grid(row=0, column=1)

        # 创建标签
        self.app_label = tk.Label(self.master, text="APP信息:")
        self.app_label.grid(row=1, column=0)
        self.app_info = tk.Entry(self.master, textvariable=self.app_var, width=len(self.app_var.get()))
        self.app_info.grid(row=1, column=1)

        # 创建多行输入框
        self.text_label = tk.Label(self.master, text="点击页面:")
        self.text_label.grid(row=2, column=0)
        self.text_box = tk.Text(self.master, height=30, width=60)
        self.text_box.grid(row=2, column=1)
        self.text_box.insert('1.0', '开始点击你的APP界面吧!')
        self.scrollbar = tk.Scrollbar(self.master, command=self.text_box.yview)
        self.scrollbar.grid(row=2, column=2, sticky="nsew")
        self.text_box.config(yscrollcommand=self.scrollbar.set)

    def start_threads(self):

        # 启动线程
        self.device_thread = threading.Thread(target=self.update_device)
        self.device_thread.start()
        self.app_thread = threading.Thread(target=self.update_app)
        self.app_thread.start()
        self.text_thread = threading.Thread(target=self.update_text)
        self.text_thread.start()
        self.lock = threading.Lock()

    def stop_threads(self):
        # 停止线程
        self.device_thread.do_run = False
        self.app_thread.do_run = False
        self.text_thread.do_run = False
        self.master.destroy()

    def update_device(self):
        self.device_thread.do_run = True
        while self.device_thread.do_run:
            # 获取设备号并更新下拉框
            devices = adb.device_list()
            device_list = [d.serial for d in devices]
            self.device_option['menu'].delete(0, 'end')
            for device in device_list:
                self.device_option['menu'].add_command(label=device, command=tk._setit(self.device_var, device))
            time.sleep(0.5)

    def update_app(self):
        self.app_thread.do_run = True
        while self.app_thread.do_run:
            # 获取APP信息并更新标签
            self.device = adb.device(self.device_var.get())
            self.app = self.device.app_current()
            self.package_name = getattr(self.app, 'package')
            self.activity_name = getattr(self.app, 'activity')
            app_info = f"{self.package_name}/{self.activity_name}"
            self.app_var.set(app_info)
            time.sleep(0.5)
    def update_text(self):
        self.text_thread.do_run = True
        while self.text_thread.do_run:
            # 获取点击页面的内容并更新多行输入框
            device = adb.device(self.device_var.get())
            self.monitor_device(device=device, output_type='appium')

    def find_smallest_bounds_index(self, target, bounds_list):
        """
        查找包含目标点的最小边界的索引。

        参数：
            target (tuple): 目标点格式为 (x, y)。
            bounds_list (list): 边界列表，格式为 [[x0, y0, x1, y1], ...]。

        返回值：
            int: 包含目标点的最小边界的索引。
        """
        smallest_area = float('inf')
        smallest_index = None

        for i, bounds in enumerate(bounds_list):
            x0, y0, x1, y1 = bounds
            if x0 < target[0] < x1 and y0 < target[1] < y1:
                area = (x1 - x0) * (y1 - y0)
                if area < smallest_area:
                    smallest_area = area
                    smallest_index = i

        return smallest_index

    def generate_xpath_with_attributes(self, element):
        if element is None:
            return ''
        if element.tag == 'hierarchy':
            class_value = element.get('class', '')
        else:
            class_value = element.get('class') if element.get('class') != '' else '*'
        resource_id = element.get('resource-id')
        text = element.get('text')

        if text:
            return f'//{class_value}[@text="{text}"]'
        elif resource_id:
            return f'//{class_value}[@resource_id="{resource_id}"]'
        else:
            parent = element.getparent()
            parent_xpath = self.generate_xpath_with_attributes(parent)
            return f'{parent_xpath}/{class_value}'

    # 实时监控设备
    def monitor_device(self, device, output_type: str = 'appium'):
        '''
        监控设备并输入指定类型的数据
        :param driverName: 设备名
        :param output_type: data or appium
        :return:
        '''
        device = adb.device(device.serial)
        app = device.app_current()
        package_name = getattr(app, 'package')
        activity_name = getattr(app, 'activity')
        print(f'''#! /usr/bin/env python

from appium import webdriver

caps = {{
    'automationName': 'UiAutomator2',
    'platformName': 'Android',
    'platformVersion': {device.shell(['getprop', 'ro.build.version.release']).strip()},
    'deviceName': {device.serial},
    'appPackage': {package_name},
    'appActivity': {activity_name},
    # 'noReset': True,
    # 'allowClearUserData': 'true',
    # 'fullReset': "false",
    # 'exported': "true",
    'unicodeKeyboard': True,
    'resetKeyboard': True
}}

app = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)

# 下面为定位表达式
        ''')
        deviceName = device.serial
        # 启动getevent命令
        event_cmd = f"adb -s {deviceName} shell getevent -lt /dev/input/event1"
        process = subprocess.Popen(event_cmd, stdout=subprocess.PIPE, shell=True)
        x = 0
        y = 0
        dx = copy.copy(x)
        dy = copy.copy(y)
        sj = ''
        status = [None, None]
        down_time = float(0)

        device = adb.device(device.serial)
        app = device.app_current()
        package_name = getattr(app, 'package')
        activity_name = getattr(app, 'activity')
        code_header = "#! /usr/bin/env python\n" + \
                      "\n" + \
                      "from appium import webdriver\n" + \
                      "\n" + \
                      "caps = {\n" + \
                      "\t'automationName': 'uiautomator2',\n" + \
                      "\t'platformName': 'Android',\n" + \
                      f"\t'platformVersion': '{device.shell(['getprop', 'ro.build.version.release']).strip()}',\n" + \
                      f"\t'deviceName': '{device.serial}',\n" + \
                      "\t# 'noReset': True,\n" + \
                      "\t# 'allowClearUserData': 'true',\n" + \
                      "\t# 'fullReset': \"false\",\n" + \
                      "\t# 'exported': \"true\",\n" + \
                      f"\t'appPackage': '{package_name}',\n" + \
                      f"\t'appActivity': '{activity_name}',\n" + \
                      "\t'unicodeKeyboard': True,\n" + \
                      "\t'resetKeyboard': True\n" + \
                      "}\n" + \
                      "\n" + \
                      "app = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)\n" + \
                      "\n" + \
                      "# 以下内容为您当前触屏事件内容：\n"
        self.text_box.delete('1.0', 'end')
        self.text_box.insert('1.0', code_header)

        # 解析事件流
        while deviceName == device.serial:
            # 读取一行事件
            line = process.stdout.readline().decode().strip()
            # 获取x坐标
            if 'POSITION_X' in line:
                parts = line.split()
                x = int(parts[4], 16)

            if 'POSITION_Y' in line:
                parts = line.split()
                y = int(parts[4], 16)

            # 如果是点击事件
            if "BTN_TOUCH" in line and "DOWN" in line:
                down_time = time.time()
                status[0] = 'DOWN'
                # 记录点下时的坐标
                dx = copy.copy(x)
                dy = copy.copy(y)

                # 生成 XML 文件
                # os.popen('adb shell uiautomator dump')
                device.shell(['uiautomator', 'dump'])

            # 如果是点击事件
            if "BTN_TOUCH" in line and "UP" in line:
                hold_time = round(time.time() - down_time, 3)  # 秒
                status[1] = 'UP'
                # 记录点下时的坐标
                ux = copy.copy(x)
                uy = copy.copy(y)

                self.lock.acquire()
                os.popen(f'adb pull /sdcard/window_dump.xml {UI_DUMP_FILE}')
                # device.shell(['pull', '/sdcard/window_dump.xml', UI_DUMP_FILE])
                self.lock.release()
                while not os.path.exists(UI_DUMP_FILE) or os.path.getsize(UI_DUMP_FILE) == 0:
                    if os.path.exists(UI_DUMP_FILE):
                        self.lock.acquire()
                        os.remove(UI_DUMP_FILE)
                        self.lock.release()
                    self.lock.acquire()
                    # 将 XML 文件保存到本地
                    os.popen(f'adb pull /sdcard/window_dump.xml {UI_DUMP_FILE}')
                    # device.shell(['pull', '/sdcard/window_dump.xml', UI_DUMP_FILE])
                    self.lock.release()
                self.lock.acquire()
                # 解析 XML 文档
                tree = etree.parse(UI_DUMP_FILE)
                self.lock.release()  # 在代码块结束后释放锁
                elements = tree.xpath('//node')
                bounds = [[int(num) for num in re.findall(r'\d+', s)] for s in tree.xpath('//node/@bounds')]
                # 防止点击页面以外的坐标，限制x与y的最大值与最小值
                x_page_max = bounds[0][2]
                y_page_max = bounds[0][3]
                ux = x_page_max-1 if ux > x_page_max else ux
                uy = y_page_max-1 if uy > y_page_max else uy
                dx = x_page_max-1 if dx > x_page_max else dx
                dy = y_page_max-1 if dy > y_page_max else dy
                ux = 1 if ux < 0 else ux
                uy = 1 if uy < 0 else uy
                dx = 1 if dx < 0 else dx
                dy = 1 if dy < 0 else dy
                up_index = self.find_smallest_bounds_index((ux, uy), bounds)
                down_index = self.find_smallest_bounds_index((dx, dy), bounds)

                if status == ['DOWN', 'UP']:
                    if up_index == down_index:
                        if output_type == 'data':
                            sj = {
                            'platformName': 'Android',
                            'platformVersion': device.shell(['getprop', 'ro.build.version.release']).strip(),
                            'deviceName': device.serial,
                            'appPackage': getattr(device.app_current, 'package'),
                            'appActivity': getattr(device.app_current, 'activity'),
                            'action': 'click',
                            'xpath': self.generate_xpath_with_attributes(elements[up_index]),
                            'bounds': [dx, dy, ux, uy],
                            'hold_time': hold_time
                        }
                        elif output_type == 'appium':
                            sj = f'app.find_element(By.XPATH, value="{self.generate_xpath_with_attributes(elements[up_index])}").click()\n'
                        else:
                            sj = '暂不支持此类型\n'
                    else:
                        if output_type == 'data':
                            sj = {
                                'platformName': 'Android',
                                'platformVersion': device.shell(['getprop', 'ro.build.version.release']).strip(),
                                'deviceName': device.serial,
                                'appPackage': getattr(device.app_current, 'package'),
                                'appActivity': getattr(device.app_current, 'activity'),
                                'action': 'swipe',
                                'xpath': None,
                                'bounds': [dx, dy, ux, uy],
                                'hold_time': hold_time
                            }
                        elif output_type == 'appium':
                            sj = f'app.swipe({dx}, {dy}, {ux}, {uy}, {int(hold_time*1000)})\n'
                        else:
                            sj = '暂不支持此类型\n'
                    status = [None, None]
                    line_count = int(self.text_box.index('end-1c').split('.')[0])
                    self.text_box.insert(f'{line_count + 1}.0', sj)
            time.sleep(0.1)
        self.monitor_device(device=device.serial)

def gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()