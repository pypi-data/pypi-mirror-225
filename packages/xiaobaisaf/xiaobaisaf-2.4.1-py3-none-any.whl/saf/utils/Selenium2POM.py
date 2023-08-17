#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/12 22:48
@File  : selenium2POM.py
'''
import re
import logging
from time import sleep
from os import path, mkdir, remove
from bs4 import BeautifulSoup
from lxml import etree
from pypinyin import lazy_pinyin
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchWindowException


class PageListener:
    def __init__(self, start_url: str = 'https://www.baidu.com', dirname: str = '.', rewrite: bool = True):
        '''
        基于Selenium基础操作过程中将每页内容转为POM
        :param start_url   : 首页地址
        :param dirname     : 目录
        :param rewrite     : 是否覆盖目录
        :return
        '''
        self.PY_FILE_NAME_LIST = []
        if rewrite and path.exists(f'{dirname}/Pages'):
            try:
                remove(f'{dirname}/Pages')
            except PermissionError as e:
                pass
        if not path.exists(f'{dirname}/Pages'):
            mkdir('Pages')
        if not path.exists(f'{dirname}/Pages/__init__.py'):
            with open(f'{dirname}/Pages/__init__.py', 'w', encoding='UTF-8') as f:
                f.write('''#! /usr/bin/env python
                
#********************************#
#    欢迎使用自动生成POM代码工具      #
#      Auther:xiaobaiTser        #
#********************************#

import logging
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(ChromeDriverManager(log_level=logging.CRITICAL).install())
                ''')
                f.close()

        self.driver = webdriver.Chrome(ChromeDriverManager(log_level=logging.CRITICAL).install())
        self.driver.get(start_url)
        self.driver.implicitly_wait(30)
        new_title = ''.join(re.findall('\w+', self.driver.title))
        filename = "_".join(lazy_pinyin(new_title)).title()
        new_filename = filename if self.PY_FILE_NAME_LIST.count(
            filename) == 0 else f'{filename}_{self.PY_FILE_NAME_LIST.count(filename)}'
        self.PY_FILE_NAME_LIST.append(filename)
        self.code2file(
            code=self.identify_inputs_and_buttons(self.driver.current_url, self.driver.page_source),
            filename=f'{dirname}/Pages/{new_filename}.py')
        # 监视浏览器URL变化、标签页变化
        self.PageUrls = {self.driver.current_url}
        self.PageHandles = self.driver.window_handles
        while True:
            sleep(0.2)
            try:
                cur_url = self.driver.current_url
                cur_handles = self.driver.window_handles
                if cur_url not in self.PageUrls:
                    self.PageUrls.add(cur_url)
                    new_title = ''.join(re.findall('\w+', self.driver.title))
                    filename = "_".join(lazy_pinyin(new_title)).title()
                    new_filename = filename if self.PY_FILE_NAME_LIST.count(
                        filename) == 0 else f'{filename}_{self.PY_FILE_NAME_LIST.count(filename)}'
                    self.PY_FILE_NAME_LIST.append(filename)
                    self.code2file(
                        code=self.identify_inputs_and_buttons(self.driver.current_url, self.driver.page_source),
                        filename=f'{dirname}/Pages/{new_filename}.py')
                if cur_handles != self.PageHandles:
                    for handle in cur_handles:
                        self.driver.switch_to.window(handle)
                        if self.driver.current_url not in self.PageUrls:
                            self.PageUrls.add(self.driver.current_url)
                            new_title = ''.join(re.findall('\w+', self.driver.title))
                            filename = "_".join(lazy_pinyin(new_title)).title()
                            new_filename = filename if self.PY_FILE_NAME_LIST.count(
                                filename) == 0 else f'{filename}_{self.PY_FILE_NAME_LIST.count(filename)}'
                            self.PY_FILE_NAME_LIST.append(filename)
                            self.code2file(
                                code=self.identify_inputs_and_buttons(self.driver.current_url, self.driver.page_source),
                                filename=f'{dirname}/Pages/{new_filename}.py')
                    self.PageHandles = self.driver.window_handles
            except KeyboardInterrupt as e:
                exit(-1)
            except NoSuchWindowException as e:
                exit(-2)

    def code2file(self, code: str, filename: str = None):
        '''
        将代码写入文件
        :param code:
        :param filename:
        :return:
        '''
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(code)
            f.close()
            del f

    def identify_inputs_and_buttons(self, url, html):
        '''
        1、解析HTML获取输入框与按钮并获取xpath表达式
        2、将输入框与按钮转为POM代码，一个页面单独一个脚本，一个脚本单独一个类
        :param url:
        :param html:
        :return:
        '''
        soup = BeautifulSoup(html, 'html.parser')
        find_all_input = soup.find_all(['input', 'textarea'])
        find_all_button = soup.find_all('button')
        find_all_button.extend(soup.find_all('a'))
        find_all_button.extend(soup.find_all('select'))
        find_all_button.extend(soup.find_all('optgroup'))
        find_all_button.extend(soup.find_all('option'))
        find_all_button.extend(soup.find_all('input', attrs={'type': ['button', 'submit']}))
        input_list = []
        button_list = []
        for input_tag in find_all_input:
            if input_tag not in soup.find_all('input', attrs={'type': ['button', 'submit', 'hidden']}):
                input_name = input_tag.get('name') or input_tag.name
                input_xpath = self.get_xpath(input_tag)
                if input_name:
                    input_list.append({'tag': input_tag, 'name': input_name, 'xpath': input_xpath})
        for button_tag in find_all_button:
            button_name = button_tag.get('name') or button_tag.text.strip() or button_tag.name
            button_xpath = self.get_xpath(button_tag)
            button_list.append({'tag': button_tag, 'name': button_name, 'xpath': button_xpath})
        title = '_'.join(lazy_pinyin(soup.select("title")[0].text)).upper()
        title = ''.join(re.findall('[0-9a-zA-Z_]+', title))
        return self.converter(page_name=title, url=url,
                              input_list=input_list, button_list=button_list)

    def get_xpath(self, element):
        '''
        获取xpath表达式
        :param element:
        :return:
        '''
        components = []
        child = element
        while child is not None:
            siblings = child.find_previous_siblings()
            index = len(siblings) + 1
            if child.name == 'html':
                components.insert(0, '/html')
                break
            if child.name == 'body':
                components.insert(0, '/body')
                break
            else:
                element_attrs_dict = child.attrs
                for k, v in element_attrs_dict.items():
                    if k in element_attrs_dict.keys() and '' != element_attrs_dict[k]:
                        html = etree.HTML(self.driver.page_source)
                        query_result = html.xpath(f'//{child.name}[@{k}="{element_attrs_dict[k]}"]')
                        if len(query_result) == 1:
                            components.insert(0, f'/{child.name}[@{k}="{element_attrs_dict[k]}"]')
                            xpath = ''.join(components)
                            xpath = xpath if xpath.startswith('/html') else '/' + xpath
                            return xpath
                        else:
                            continue
            components.insert(0, f'/{child.name}[{index}]')
            child = child.parent
        xpath = ''.join(components)
        xpath = xpath if xpath.startswith('/html') else '/' + xpath
        return xpath

    def converter(self, page_name: str, url: str, input_list: list, button_list: list):
        '''
        将输入框与按钮等转为POM代码
        :param page_name:
        :param url:
        :param input_list:
        :param button_list:
        :return:
        '''
        function_strings = []
        function_names = []
        function_strings.append('#! /usr/bin/env python')
        function_strings.append(f'')
        function_strings.append('#********************************#')
        function_strings.append('#    欢迎使用自动生成POM代码工具      #')
        function_strings.append('#      Auther:xiaobaiTser        #')
        function_strings.append('#********************************#')
        function_strings.append(f'')
        function_strings.append('from selenium.webdriver.common.by import By')
        function_strings.append(f'')
        function_strings.append(f'class {page_name}:')
        function_strings.append('\tdef __init__(self, driver):')
        function_strings.append(f'\t\t# 当前页面URL: {url}')
        function_strings.append('\t\tself.driver = driver')
        function_strings.append(f'')
        for input_item in input_list:
            function_name = "_".join(lazy_pinyin(input_item['name']))
            function_name = ''.join(re.findall('[0-9a-zA-Z_]+', function_name))
            new_function_name = function_name if function_names.count(function_name) == 0 else \
                f'{function_name}_{function_names.count(function_name)}'
            function_names.append(function_name)
            xpath = input_item['xpath']
            function_strings.append(f'\tdef send_{new_function_name}(self, data):')
            function_strings.append("\t\t'''")
            function_strings.append('\t\t当前元素：')
            input_item['tag'] = str(input_item['tag']).replace('\n', '\n\t\t')
            function_strings.append(f"\t\t{input_item['tag']}")
            function_strings.append("\t\t'''")
            function_strings.append(f'\t\tself.driver.find_element(By.XPATH, \'{xpath}\').send_keys(data)')
            function_strings.append(f'')
        for button_item in button_list:
            function_name = "_".join(lazy_pinyin(button_item['name']))
            function_name = ''.join(re.findall('[0-9a-zA-Z_]+', function_name))
            new_function_name = function_name if function_names.count(function_name) == 0 else \
                f'{function_name}_{function_names.count(function_name)}'
            function_names.append(function_name)
            xpath = button_item['xpath']
            function_strings.append(f'\tdef click_{new_function_name}(self):')
            function_strings.append("\t\t'''")
            function_strings.append('\t\t当前元素：')
            button_item['tag'] = str(button_item['tag']).replace('\n', '\n\t\t')
            function_strings.append(f"\t\t{button_item['tag']}")
            function_strings.append("\t\t'''")
            function_strings.append(f'\t\tself.driver.find_element(By.XPATH, \'{xpath}\').click()')
            function_strings.append(f'')
        return '\n'.join(function_strings)

# if __name__ == '__main__':
#     PageListener(start_url='http://192.168.0.240:9800/login')