#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 1:37
@File  : image_utils.py
'''
import os

import cv2
import numpy as np
from time import sleep
from random import randint

from selenium.webdriver.common.action_chains import ActionChains

from saf import WebDriver, By, DdddOcr, WebElement
from saf.utils.ElementUtils import find_element

def image2str(driver: WebDriver = None, by: str = By.XPATH,value: str = ''):
    '''
    图片验证码识别工具
    :param driver   : 浏览器驱动
    :param by       : 定位方法
    :param value    : 定位表达式
    :return         : 返回验证码图片中识别的字符串
    '''
    return DdddOcr(show_ad=False).classification(find_element(driver, by, value=value).screenshot_as_base64)

def checkSlider(driver: WebDriver = None, target_element: WebElement = None, background_element: WebElement = None,
                button_element: WebElement = None, fail_retry: bool = False, times: int = 3):
    '''
    滑块验证码识别工具，基于openCV识别图片及图片二次处理
    :param driver               : 浏览器驱动
    :param target_element       : 目标图片（小图）
    :param background_element   : 背景图片（大图）
    :param button_element       : 滑块按钮
    :param fail_retry           : 失败重试
    :return:
    '''
    cur_url = driver.current_url
    ''' 获取验证码的小图与背景图 '''
    dd = DdddOcr(show_ad=False, det=False, ocr=False)

    # 目标图（滑动的小图）
    target_element.screenshot('target.png')
    with open('target.png', 'rb') as f:
        target = f.read()

    # 背景图（不能滑动的大图）
    background_element.screenshot('background.png')

    '''  因为背景图是直接截图的所以匹配的结果是不准确的，需要去除  '''
    # 读取大图和小图
    img = cv2.imread('background.png')
    template = cv2.imread('target.png')

    # 使用 TM_CCOEFF_NORMED 方法进行模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 设置匹配阈值
    threshold = 0.8

    # 获取匹配结果的位置信息
    loc = np.where(res >= threshold)

    # 遍历匹配结果，将小图在大图上抹掉
    w, h = template.shape[:-1]
    for pt in zip(*loc[::-1]):
        img[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 0

    # 保存处理后的图像
    cv2.imwrite('background_new.png', img)

    sleep(2)

    ''' 在处理之后的图片中进行查询坐标的操作 '''
    with open('background_new.png', 'rb') as f:
        background = f.read()

    # 背景图搜索目标图的位置
    result = dd.slide_match(target_bytes=target, background_bytes=background, simple_target=True)
    Xoff = result['target'][0]

    # 滑动移动的距离就是 目标图 在 背景图中所在的位置 使用鼠标事件
    # 创建鼠标对象
    action = ActionChains(driver)
    action.click_and_hold(on_element=button_element).pause(0.5)
    # 鼠标 将 滑块按钮 向右滑动
    action.move_by_offset(xoffset=50, yoffset=0).pause(0.1)
    action.move_by_offset(xoffset=Xoff-45, yoffset=0).pause(0.1)
    action.move_by_offset(xoffset=-7, yoffset=0).pause(0.15)
    action.move_by_offset(xoffset=2, yoffset=0).pause(0.1)
    action.release().perform()

    for _ in range(times):
        if fail_retry and cur_url == driver.current_url:
            try:
                checkSlider(driver, target_element, background_element, button_element, fail_retry, 0)
            except Exception:
                pass
        else:
            break

    ''' 验证码通过之后，打扫战场，删除图片文件 '''
    os.remove('target.png')
    os.remove('background.png')
    os.remove('background_new.png')