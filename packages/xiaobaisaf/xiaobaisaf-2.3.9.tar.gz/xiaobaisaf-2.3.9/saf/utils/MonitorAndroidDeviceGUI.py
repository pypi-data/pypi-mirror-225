#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/19 22:01
@File  : MonitorAndroidDeviceGUI.py
'''

import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from adbutils import adb
import os

class MonitorAndroid:
    def __init__(self, device):
        CUR_PATH = os.path.dirname(os.path.abspath(__file__))
        # 创建Tkinter界面
        self.root = tk.Tk()
        self.root.iconbitmap(CUR_PATH + '\\..\\data\\favicon.ico')

        # 获取设备的分辨率并设置Tkinter界面的大小
        self.device = device
        width, height = device.window_size()
        self.root.geometry(f'{width // 5}x{height // 5}')
        self.root.resizable(False, False)
        # 标题
        self.root.title(device.serial)

        self.label = tk.Label(self.root)
        self.label.pack()
        # 开始更新图片
        self.device_screenshot()
        self.root.mainloop()

    def device_screenshot(self):
        # 获取Android设备的屏幕截图
        screenshot = self.device.screenshot()

        # 将截图转换为字节流
        byte_stream = BytesIO()
        screenshot.save(byte_stream, format='PNG')
        screenshot_byte = byte_stream.getvalue()

        # 将字节流转换为Tkinter可以使用的格式
        image = Image.open(BytesIO(screenshot_byte))
        new_size = (image.width // 5, image.height // 5)
        resized_image = image.resize(new_size)
        photo = ImageTk.PhotoImage(resized_image)

        # 更新Tkinter界面的图片
        self.label.config(image=photo)
        self.label.image = photo

        # 每100毫秒更新一次图片
        self.label.after(100, self.device_screenshot)

def MonitorDevice(index: int = 0):
    devices = adb.device_list()
    print(f'设备列表：{devices}，您选择的是第{index+1}个')
    if len(devices) > 0 and index < len(devices):
        MonitorAndroid(device=devices[index])
    else:
        print('您选择了无效的序号！')