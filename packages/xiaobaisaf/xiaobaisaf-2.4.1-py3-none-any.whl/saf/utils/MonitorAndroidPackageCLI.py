#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/15 0:22
@File  : MonitorDriver2.py
'''
import os
import re
import subprocess
import copy
import time
import getpass
from lxml import etree
from adbutils import adb

USERHOMEDIR = f'C:\\Users\\{getpass.getuser()}'

UI_DUMP_FILE = f'{USERHOMEDIR}\\window_dump.xml'

def find_smallest_bounds_index(target, bounds_list):
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

def generate_xpath_with_attributes(element):
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
        parent_xpath = generate_xpath_with_attributes(parent)
        return f'{parent_xpath}/{class_value}'


# 实时监控设备
def monitor_device(device, output_type: str = 'appium'):
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
    # 'dontStopAppOnReset': True,
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

            os.popen(f'adb pull /sdcard/window_dump.xml {UI_DUMP_FILE}')
            # device.shell(['pull', 'sdcard/window_dump.xml', UI_DUMP_FILE])
            while not os.path.exists(UI_DUMP_FILE) or os.path.getsize(UI_DUMP_FILE) == 0:
                try:
                    if os.path.exists(UI_DUMP_FILE):  os.remove(UI_DUMP_FILE)
                except PermissionError as e:
                    print('数据处理异常，正在重新尝试！')
                    # 将 XML 文件保存到本地
                    os.popen(f'adb pull /sdcard/window_dump.xml {UI_DUMP_FILE}')
                    continue
                finally:
                    # 将 XML 文件保存到本地
                    os.popen(f'adb pull /sdcard/window_dump.xml {UI_DUMP_FILE}')
            try:
                # 解析 XML 文档
                tree = etree.parse(UI_DUMP_FILE)
            except Exception as e:
                print('数据加载异常，正在重新尝试！')
                continue
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
            up_index = find_smallest_bounds_index((ux, uy), bounds)# 查看是否再一个元素内，如果再就是点击
            down_index = find_smallest_bounds_index((dx, dy), bounds)

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
                            'xpath': generate_xpath_with_attributes(elements[up_index]),
                            'bounds': [dx, dy, ux, uy],
                            'hold_time': hold_time
                        }
                    elif output_type == 'appium':
                        # sj = f'app.find_element(By.XPATH, value="{elements[up_index].getroottree().getpath(elements[up_index])}").click()'      # /hierarchy/node/node[2]/node[2]/node/node/node/node/node/node[3]/node/node[1]/node[2]/node[1]
                        sj = f'app.find_element(By.XPATH, value="{generate_xpath_with_attributes(elements[up_index])}").click()'                                # /hierarchy/node/node[2]/node[2]/node/node/node/node/node/node[3]/node/node[1]/node[2]
                    else:
                        sj = '暂不支持此类型'
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
                        sj = f'app.swipe({dx}, {dy}, {ux}, {uy}, {int(hold_time*1000)})'
                    else:
                        sj = '暂不支持此类型'
                status = [None, None]
                print(sj)

def cli():
    devices = []
    try:
        while not len(devices):
            print('等待设备连接中' + '.'*(int(time.time()) % 4), end='')
            devices = adb.device_list()
            time.sleep(1)
            print('', end='\r')
        monitor_device(devices[0], output_type='appium')
    except KeyboardInterrupt:
        pass
