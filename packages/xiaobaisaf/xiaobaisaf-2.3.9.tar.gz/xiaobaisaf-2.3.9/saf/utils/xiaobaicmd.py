#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/24 2:26
@File  : xiaobaicmd.py
'''
import os.path
from shutil import copytree
import click
from saf.utils.Selenium2POM import PageListener
from saf.utils.FlushDNSUtils import flushDNS
from saf.utils.MonitorAndroidPackageGUI import gui
from saf.utils.MonitorAndroidPackageCLI import cli
from saf.utils.MonitorAndroidDeviceGUI import MonitorDevice
from saf.utils.MonitorAndroidPackagePower import power


@click.command()
@click.option('--template', '-t', type=click.Choice(['web', 'api', 'app']), nargs=1, help='创建自动化项目模板')
@click.option('--dirname', '-d', default='.', type=str, nargs=1, help='创建自动化项目模板存放的目录')
@click.option('--domains', type=str, nargs=1, help='用户提供多域名使用","分割自动获取DNS解析结果并写入HOSTS文件，例如：--domains github.com,raw.githubusercontent.com')
@click.option('--url', '-u', type=str, nargs=1, help='自动生成PageObject代码的首个URL')
@click.option('--rewrite', '-r', default=1, type=int, nargs=1, help='自动生成PageObject是否重写')
@click.option('--monitor', '-m', type=click.Choice(['gui', 'cli', 'power', 'memory']), nargs=1, help='监控自动识别APP页面点击/滑动的Xpath表达式与坐标信息或者监控设备电量与APP内存使用率')
@click.option('--device', '-e', type=int, nargs=1, help='监控设备的界面图像，从1开始计算设备序号，暂无其他功能')
def main(template, dirname, domains, url, rewrite, monitor, device):
    if template:
        if "web" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\web'),
                     os.path.join(os.path.abspath(dirname), 'web')
                     )
        elif "api" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\api'),
                     os.path.join(os.path.abspath(dirname), 'api')
                     )
        elif "app" == template.lower():
            copytree(os.path.join(os.path.dirname(os.path.abspath(__file__)), r'..\app'),
                     os.path.join(os.path.abspath(dirname), 'app')
                     )
        else:
            raise ("您输入的数据有误，有效范围：web 或 api 或 app")
    elif url:
        if rewrite:
            PageListener(start_url=url, dirname=dirname, rewrite=True)
        else:
            PageListener(start_url=url, dirname=dirname, rewrite=False)
    elif monitor == "gui":
        gui()
    elif monitor == "cli":
        cli()
    elif monitor == "power":
        power()
    elif monitor == "memory":
        power()
    elif device:
        MonitorDevice(device - 1)
    elif domains:
        flushDNS(domains)
